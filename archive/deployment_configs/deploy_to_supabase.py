#!/usr/bin/env python3
"""
Supabase Deployment Script
Banco Insights 2.0 - Deploy schema and data to Supabase

This script deploys the complete database schema and runs the ETL pipeline
to populate your Supabase instance with BACEN financial data.
"""

import os
import sys
import subprocess
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import pandas as pd
from datetime import datetime

# Supabase Configuration
SUPABASE_CONFIG = {
    'host': 'db.uwoxkycxkidipgbptsgx.supabase.co',
    'port': 6543,  # Supabase uses port 6543 for external connections
    'database': 'postgres',
    'user': 'postgres.uwoxkycxkidipgbptsgx',  # Supabase user format
    'password': 'En9QmRQaw14nhwxL'
}

def test_supabase_connection():
    """Test connection to Supabase database"""
    print("🔌 Testing Supabase connection...")
    
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to Supabase PostgreSQL: {version}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def deploy_schema_to_supabase():
    """Deploy database schema to Supabase"""
    print("\n📋 Deploying schema to Supabase...")
    
    # Read the original schema file with Supabase features
    schema_file = Path('database/schema/001_initial_schema.sql')
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        return False
        
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
    
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            print("📝 Executing schema deployment...")
            cursor.execute(schema_sql)
            
        print("✅ Schema deployed successfully to Supabase!")
        
        # Test schema deployment
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
            table_count = cursor.fetchone()[0]
            print(f"📊 Created {table_count} tables")
            
            cursor.execute("SELECT COUNT(*) FROM pg_matviews WHERE schemaname = 'public'")
            view_count = cursor.fetchone()[0]  
            print(f"📈 Created {view_count} materialized views")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Schema deployment to Supabase failed: {e}")
        return False

def load_institutions_to_supabase():
    """Load institutions data to Supabase"""
    print("\n🏦 Loading institutions to Supabase...")
    
    try:
        # Load institutions from file
        institutions_file = Path('bacen_project_v1/data/consolidated_institutions.json')
        if not institutions_file.exists():
            print(f"❌ Institutions file not found: {institutions_file}")
            return False
            
        institutions_df = pd.read_json(institutions_file)
        print(f"📁 Found {len(institutions_df)} institutions to load")
        
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            loaded_count = 0
            for i, row in institutions_df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO institutions (
                            cod_inst, cnpj, name, short_name, type, segment, 
                            control_type, region, city, status
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active'
                        ) ON CONFLICT (cod_inst) DO NOTHING
                    """, (
                        str(row['CodInst']).zfill(8),
                        f"{i:014d}",  # Generate unique CNPJ using index
                        row['NomeInstituicao'],
                        row['NomeInstituicao'][:50],  # Short name
                        'Instituição Financeira',      # Type
                        'S1',                         # Segment (default)
                        'Privado Nacional',           # Control type (default)
                        'SP',                         # Region (default)
                        'São Paulo'                   # City (default)
                    ))
                    loaded_count += 1
                except Exception as e:
                    print(f"⚠️ Error loading institution {row['CodInst']}: {e}")
                    continue
        
        print(f"✅ Loaded {loaded_count} institutions to Supabase")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to load institutions: {e}")
        return False

def run_etl_pipeline_supabase(test_mode=True):
    """Run ETL pipeline against Supabase"""
    print(f"\n⚙️ Running ETL pipeline ({'TEST' if test_mode else 'FULL'} mode)...")
    
    # Change to bacen_project_v1 directory
    os.chdir('bacen_project_v1')
    
    # Build command
    cmd = [
        'python', 'run_etl_pipeline.py',
        '--db-host=db.uwoxkycxkidipgbptsgx.supabase.co',
        '--db-port=5432',
        '--db-name=postgres',
        '--db-user=postgres',
        f'--db-password={SUPABASE_CONFIG["password"]}',
        '--validate'
    ]
    
    if test_mode:
        cmd.append('--test-mode')
    else:
        cmd.append('--full-run')
    
    try:
        print(f"🚀 Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
        
        print("\n📊 ETL Pipeline Output:")
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️ ETL Pipeline Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ ETL pipeline completed successfully!")
            return True
        else:
            print(f"❌ ETL pipeline failed with exit code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ ETL pipeline timed out after 30 minutes")
        return False
    except Exception as e:
        print(f"❌ ETL pipeline execution failed: {e}")
        return False
    finally:
        # Change back to original directory
        os.chdir('..')

def validate_supabase_deployment():
    """Validate the Supabase deployment"""
    print("\n🔍 Validating Supabase deployment...")
    
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Check core data counts
            cursor.execute("SELECT COUNT(*) as count FROM institutions")
            institutions_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM financial_data")
            financial_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM time_periods")
            periods_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM metrics")
            metrics_count = cursor.fetchone()['count']
            
            print(f"📊 Supabase Data Summary:")
            print(f"  🏦 Institutions: {institutions_count:,}")
            print(f"  💰 Financial Records: {financial_count:,}")
            print(f"  📅 Time Periods: {periods_count}")
            print(f"  📈 Metrics: {metrics_count}")
            
            # Test a sample query
            cursor.execute("""
                SELECT 
                    i.name as institution,
                    COUNT(*) as record_count,
                    SUM(fd.valor) as total_value
                FROM financial_data fd
                JOIN institutions i ON fd.institution_id = i.id
                GROUP BY i.id, i.name
                ORDER BY total_value DESC
                LIMIT 3
            """)
            
            top_institutions = cursor.fetchall()
            if top_institutions:
                print(f"\n🏆 Top Institutions by Value:")
                for inst in top_institutions:
                    print(f"  {inst['institution'][:40]:40} | {inst['record_count']:,} records | R$ {inst['total_value']:,.2f}")
            
            # Test materialized views
            cursor.execute("SELECT COUNT(*) FROM market_share_view")
            market_view_count = cursor.fetchone()['count']
            print(f"\n📈 Materialized Views:")
            print(f"  Market Share View: {market_view_count:,} records")
        
        conn.close()
        print(f"\n✅ Supabase deployment validation successful!")
        return True
        
    except Exception as e:
        print(f"❌ Supabase validation failed: {e}")
        return False

def generate_supabase_connection_info():
    """Generate connection information for frontend"""
    print("\n📋 Supabase Connection Information:")
    print("=" * 60)
    print(f"🌐 Project URL: https://uwoxkycxkidipgbptsgx.supabase.co")
    print(f"🔑 Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    print(f"🗄️ Database: Direct PostgreSQL connection available")
    print(f"📊 Dashboard: https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx")
    
    # Save connection details to file
    connection_info = {
        "project_name": "banco-insights-db",
        "project_url": "https://uwoxkycxkidipgbptsgx.supabase.co",
        "anon_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU",
        "database_url": f"postgresql://postgres:{SUPABASE_CONFIG['password']}@{SUPABASE_CONFIG['host']}:{SUPABASE_CONFIG['port']}/{SUPABASE_CONFIG['database']}",
        "deployment_date": datetime.now().isoformat()
    }
    
    with open('supabase_connection_info.json', 'w') as f:
        json.dump(connection_info, f, indent=2)
    
    print(f"📝 Connection details saved to: supabase_connection_info.json")
    print("=" * 60)

def main():
    """Main deployment process"""
    print("🚀 BANCO INSIGHTS 2.0 - SUPABASE DEPLOYMENT")
    print("=" * 80)
    print("This script will deploy your complete banking database to Supabase")
    print("=" * 80)
    
    # Step 1: Test connection
    if not test_supabase_connection():
        print("\n💥 Cannot continue without Supabase connection")
        sys.exit(1)
    
    # Step 2: Deploy schema
    if not deploy_schema_to_supabase():
        print("\n💥 Schema deployment failed")
        sys.exit(1)
    
    # Step 3: Load institutions
    if not load_institutions_to_supabase():
        print("\n💥 Institution loading failed")
        sys.exit(1)
    
    # Step 4: Ask about ETL mode
    print("\n🤔 ETL Pipeline Options:")
    print("1. Test Mode (sample data, ~5 minutes)")
    print("2. Full Mode (complete historical data, ~60 minutes)")
    
    choice = input("\nChoose mode (1 for test, 2 for full): ").strip()
    test_mode = choice != "2"
    
    # Step 5: Run ETL pipeline
    if not run_etl_pipeline_supabase(test_mode):
        print("\n💥 ETL pipeline failed")
        sys.exit(1)
    
    # Step 6: Validate deployment
    if not validate_supabase_deployment():
        print("\n💥 Deployment validation failed")
        sys.exit(1)
    
    # Step 7: Generate connection info
    generate_supabase_connection_info()
    
    print("\n" + "=" * 80)
    print("🎉 SUPABASE DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("Your Banco Insights 2.0 database is now live on Supabase!")
    print("Frontend developers can now connect using the generated connection info.")
    print("=" * 80)

if __name__ == "__main__":
    main()