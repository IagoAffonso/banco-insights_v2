#!/usr/bin/env python3
"""
Database Schema Deployment Script
Banco Insights 2.0 - Deploy schema to PostgreSQL database
"""

import psycopg2
import sys
from pathlib import Path

def deploy_schema():
    """Deploy the database schema"""
    
    # Database connection
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'banco_insights',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    # Read schema file
    schema_file = Path('schema/001_initial_schema.sql')
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        return False
        
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
        
    # Remove Supabase-specific commands for local deployment
    supabase_lines_to_remove = [
        'ALTER TABLE institutions ENABLE ROW LEVEL SECURITY;',
        'ALTER TABLE financial_data ENABLE ROW LEVEL SECURITY;',
        'CREATE POLICY "Allow read access to authenticated users"',
        'CREATE POLICY "Allow read access to financial data"',
        'CREATE POLICY "Allow admin write access"', 
        'CREATE POLICY "Allow admin write access to financial data"',
        'FOR SELECT TO authenticated USING (true);',
        'FOR SELECT TO authenticated USING (true);',
        'FOR ALL TO authenticated',
        'USING (auth.jwt() ->> \'role\' = \'admin\');',
        'USING (auth.jwt() ->> \'role\' = \'admin\');'
    ]
    
    # Filter out Supabase RLS policies
    sql_lines = schema_sql.split('\n')
    filtered_lines = []
    skip_policy = False
    
    for line in sql_lines:
        line_stripped = line.strip()
        
        # Skip RLS and policy lines
        if any(pattern in line_stripped for pattern in [
            'ENABLE ROW LEVEL SECURITY',
            'CREATE POLICY',
            'FOR SELECT TO authenticated',
            'FOR ALL TO authenticated',
            'auth.jwt()'
        ]):
            skip_policy = True
            continue
            
        # End of policy block
        if skip_policy and line_stripped.endswith(';'):
            skip_policy = False
            continue
            
        if not skip_policy:
            filtered_lines.append(line)
    
    schema_sql = '\n'.join(filtered_lines)
    
    try:
        # Connect and execute schema
        print("🔌 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            print("📝 Executing schema deployment...")
            cursor.execute(schema_sql)
            
        print("✅ Database schema deployed successfully!")
        
        # Test basic queries
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
            table_count = cursor.fetchone()[0]
            print(f"📊 Created {table_count} tables")
            
            cursor.execute("SELECT COUNT(*) FROM pg_matviews WHERE schemaname = 'public'")
            view_count = cursor.fetchone()[0]  
            print(f"📈 Created {view_count} materialized views")
            
            cursor.execute("SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public'")
            index_count = cursor.fetchone()[0]
            print(f"🚀 Created {index_count} indexes")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Schema deployment failed: {e}")
        return False

if __name__ == "__main__":
    print("🏦 Banco Insights 2.0 - Database Schema Deployment")
    print("=" * 60)
    
    success = deploy_schema()
    if success:
        print("\n🎉 Schema deployment completed successfully!")
        print("Ready to run ETL pipeline.")
    else:
        print("\n💥 Schema deployment failed!")
        sys.exit(1)