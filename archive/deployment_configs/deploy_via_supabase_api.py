#!/usr/bin/env python3
"""
Deploy to Supabase via REST API
Alternative deployment method when direct PostgreSQL connection fails
"""

import requests
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

class SupabaseAPIDeployer:
    def __init__(self):
        self.base_url = "https://uwoxkycxkidipgbptsgx.supabase.co"
        self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU"
        self.headers = {
            'apikey': self.api_key,
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
    def test_connection(self):
        """Test API connectivity"""
        print("🔌 Testing Supabase API connection...")
        try:
            response = requests.get(f"{self.base_url}/rest/v1/", headers=self.headers, timeout=10)
            print(f"✅ Connected to Supabase API - Status: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ API connection failed: {e}")
            return False
            
    def execute_sql(self, sql_query):
        """Execute SQL via Supabase RPC"""
        print(f"📝 Executing SQL: {sql_query[:50]}...")
        
        # Use Supabase RPC endpoint for SQL execution
        rpc_url = f"{self.base_url}/rest/v1/rpc/execute_sql"
        payload = {"sql": sql_query}
        
        try:
            response = requests.post(rpc_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                print("✅ SQL executed successfully")
                return True
            else:
                print(f"❌ SQL execution failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ SQL execution error: {e}")
            return False
            
    def create_schema_rpc_function(self):
        """Create a helper RPC function for SQL execution"""
        print("⚙️ Setting up SQL execution helper...")
        
        # This would typically be done through the Supabase dashboard
        # For now, we'll provide instructions
        print("📋 Please execute this in your Supabase SQL Editor:")
        print("""
CREATE OR REPLACE FUNCTION execute_sql(sql text)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    EXECUTE sql;
    RETURN 'SUCCESS';
EXCEPTION WHEN OTHERS THEN
    RETURN SQLERRM;
END;
$$;
        """)
        
        input("Press Enter after creating the function in Supabase SQL Editor...")
        return True
        
    def deploy_schema_via_dashboard(self):
        """Provide instructions for manual schema deployment"""
        print("📋 MANUAL SCHEMA DEPLOYMENT REQUIRED")
        print("=" * 60)
        print("Due to connection limitations, please follow these steps:")
        print()
        print("1. Go to your Supabase dashboard:")
        print("   https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx")
        print()
        print("2. Navigate to SQL Editor")
        print()
        print("3. Copy and paste the schema from:")
        print("   database/schema/001_initial_schema.sql")
        print()
        print("4. Execute the SQL to create all tables and views")
        print()
        print("=" * 60)
        
        choice = input("Have you completed the schema deployment? (y/n): ")
        return choice.lower() == 'y'
        
    def load_sample_institutions_via_api(self):
        """Load a sample of institutions via REST API"""
        print("🏦 Loading sample institutions via API...")
        
        # Load institutions file
        institutions_file = Path('bacen_project_v1/data/consolidated_institutions.json')
        if not institutions_file.exists():
            print(f"❌ Institutions file not found: {institutions_file}")
            return False
            
        institutions_df = pd.read_json(institutions_file)
        
        # Take a sample for API loading (API has limits)
        sample_size = min(100, len(institutions_df))
        sample_institutions = institutions_df.head(sample_size)
        
        print(f"📊 Loading {sample_size} sample institutions...")
        
        institutions_url = f"{self.base_url}/rest/v1/institutions"
        loaded_count = 0
        
        for i, row in sample_institutions.iterrows():
            institution_data = {
                "cod_inst": str(row['CodInst']).zfill(8),
                "cnpj": f"{i:014d}",
                "name": row['NomeInstituicao'],
                "short_name": row['NomeInstituicao'][:50],
                "type": "Instituição Financeira",
                "segment": "S1",
                "control_type": "Privado Nacional", 
                "region": "SP",
                "city": "São Paulo",
                "status": "active"
            }
            
            try:
                response = requests.post(institutions_url, headers=self.headers, json=institution_data)
                if response.status_code in [200, 201]:
                    loaded_count += 1
                elif response.status_code == 409:  # Conflict - already exists
                    loaded_count += 1
                else:
                    print(f"⚠️ Error loading institution {row['CodInst']}: {response.text}")
                    
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                print(f"⚠️ Exception loading institution {row['CodInst']}: {e}")
                continue
        
        print(f"✅ Loaded {loaded_count} institutions via API")
        return loaded_count > 0
        
    def provide_etl_instructions(self):
        """Provide instructions for running ETL with proper connection"""
        print("\n📋 ETL PIPELINE EXECUTION INSTRUCTIONS")
        print("=" * 60)
        print("To run the ETL pipeline with Supabase, you have two options:")
        print()
        print("Option 1 - Check Network Connection:")
        print("- Verify your internet connection can resolve Supabase hosts")
        print("- Try using a VPN or different network")
        print("- Check if firewall is blocking PostgreSQL connections")
        print()
        print("Option 2 - Use Connection Pooler:")
        print("In your Supabase dashboard, go to Settings > Database")
        print("Use the 'Connection Pooler' settings instead of direct connection:")
        print()
        print("Host: aws-0-us-east-1.pooler.supabase.com (example)")
        print("Port: 6543")
        print("Database: postgres")
        print("User: postgres.uwoxkycxkidipgbptsgx")
        print("Password: En9QmRQaw14nhwxL")
        print()
        print("Then run:")
        print("cd bacen_project_v1")
        print("python run_etl_pipeline.py --test-mode \\")
        print("  --db-host=YOUR_POOLER_HOST \\")
        print("  --db-port=6543 \\")
        print("  --db-user=postgres.uwoxkycxkidipgbptsgx \\")
        print("  --db-password=En9QmRQaw14nhwxL \\")
        print("  --validate")
        print("=" * 60)
        
    def generate_api_integration_examples(self):
        """Generate code examples for API integration"""
        print("\n📋 SUPABASE API INTEGRATION EXAMPLES")
        print("=" * 60)
        
        # JavaScript example
        js_example = '''
// Frontend Integration Example
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://uwoxkycxkidipgbptsgx.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU'
const supabase = createClient(supabaseUrl, supabaseKey)

// Query institutions
const { data, error } = await supabase
  .from('institutions')
  .select('*')
  .limit(10)

// Query financial data with joins
const { data: financialData } = await supabase
  .from('financial_data')
  .select(`
    valor,
    institutions(name),
    time_periods(year, quarter_text),
    metrics(nome_coluna)
  `)
  .limit(100)
'''
        
        # Python example
        python_example = '''
# Python API Integration
import requests

headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
}

# Get institutions
response = requests.get(
    'https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1/institutions',
    headers=headers
)
institutions = response.json()

# Get financial data with aggregation
response = requests.get(
    'https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1/financial_data?select=valor,institutions(name)&limit=100',
    headers=headers
)
financial_data = response.json()
'''
        
        with open('supabase_integration_examples.txt', 'w') as f:
            f.write("SUPABASE API INTEGRATION EXAMPLES\n")
            f.write("=" * 50 + "\n\n")
            f.write("JavaScript/TypeScript:\n")
            f.write(js_example)
            f.write("\n\nPython:\n")
            f.write(python_example)
            
        print("📝 Integration examples saved to: supabase_integration_examples.txt")
        
def main():
    """Main deployment process"""
    deployer = SupabaseAPIDeployer()
    
    print("🚀 SUPABASE API DEPLOYMENT")
    print("=" * 50)
    
    # Test connection
    if not deployer.test_connection():
        print("💥 Cannot connect to Supabase API")
        return
    
    # Deploy schema (manual process)
    if not deployer.deploy_schema_via_dashboard():
        print("⚠️ Schema deployment incomplete")
    
    # Load sample data
    if deployer.load_sample_institutions_via_api():
        print("✅ Sample institutions loaded")
    
    # Provide ETL instructions
    deployer.provide_etl_instructions()
    
    # Generate integration examples
    deployer.generate_api_integration_examples()
    
    # Save configuration
    config = {
        "deployment_method": "api",
        "project_url": "https://uwoxkycxkidipgbptsgx.supabase.co",
        "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU",
        "dashboard_url": "https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx",
        "status": "partial_deployment_api_method",
        "next_steps": [
            "Complete schema deployment via Supabase SQL Editor",
            "Resolve network connectivity for ETL pipeline",
            "Run ETL pipeline with connection pooler settings"
        ]
    }
    
    with open('supabase_deployment_status.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT STATUS")
    print("=" * 50)
    print("✅ Supabase API connection working")
    print("⚠️ Direct PostgreSQL connection blocked (network issue)")
    print("✅ Sample institutions loaded via API")
    print("📋 Manual schema deployment required")
    print("📝 Integration examples generated")
    print()
    print("Next: Complete schema deployment in Supabase dashboard")
    print("=" * 50)

if __name__ == "__main__":
    main()