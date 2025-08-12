#!/usr/bin/env python3
"""
Load institutions to Supabase with proper error handling
"""

import requests
import pandas as pd
import json
from pathlib import Path
import time

# Configuration
base_url = 'https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1'
headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

def test_table_access():
    """Test if we can access the institutions table"""
    print("🔍 Testing table access...")
    
    try:
        response = requests.get(f'{base_url}/institutions?limit=1', headers=headers)
        if response.status_code == 200:
            print("✅ Can read institutions table")
            return True
        else:
            print(f"❌ Cannot read institutions table: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing table access: {e}")
        return False

def load_sample_institutions():
    """Load sample institutions with better error handling"""
    print("🏦 Loading sample institutions...")
    
    # Load institutions file
    institutions_file = Path('bacen_project_v1/data/consolidated_institutions.json')
    if not institutions_file.exists():
        print(f"❌ Institutions file not found: {institutions_file}")
        return False
    
    df = pd.read_json(institutions_file)
    sample = df.head(10)  # Start with just 10 institutions
    
    print(f"📊 Loading {len(sample)} institutions...")
    
    url = f'{base_url}/institutions'
    loaded_count = 0
    failed_count = 0
    
    for i, row in sample.iterrows():
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
            response = requests.post(url, headers=headers, json=institution_data, timeout=10)
            
            if response.status_code in [200, 201]:
                loaded_count += 1
                print(f"✅ {loaded_count}/10: {institution_data['name'][:40]}")
            elif response.status_code == 409:  # Conflict - already exists
                loaded_count += 1
                print(f"✅ {loaded_count}/10: {institution_data['name'][:40]} (already exists)")
            else:
                failed_count += 1
                print(f"❌ Failed {failed_count}: {response.status_code} - {response.text}")
                
                # Stop if we get too many failures
                if failed_count >= 3:
                    print("⚠️ Too many failures, stopping. Please check RLS policies.")
                    break
                    
        except Exception as e:
            failed_count += 1
            print(f"❌ Exception {failed_count}: {e}")
            
        time.sleep(0.3)  # Rate limiting
    
    print(f"\n📊 Results: {loaded_count} loaded, {failed_count} failed")
    return loaded_count > 0

def check_existing_data():
    """Check what data already exists"""
    print("📋 Checking existing data...")
    
    try:
        response = requests.get(f'{base_url}/institutions?select=cod_inst,name&limit=5', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data)} existing institutions:")
            for inst in data:
                print(f"  {inst['cod_inst']}: {inst['name'][:40]}")
        else:
            print(f"⚠️ Could not check existing data: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking data: {e}")

def main():
    """Main execution"""
    print("🚀 SUPABASE INSTITUTION LOADER")
    print("=" * 50)
    
    # Test access
    if not test_table_access():
        print("\n💡 RLS Issue Fix:")
        print("Run this in your Supabase SQL Editor:")
        print("ALTER TABLE institutions DISABLE ROW LEVEL SECURITY;")
        return
    
    # Check existing data
    check_existing_data()
    
    # Load new data
    success = load_sample_institutions()
    
    if success:
        print("\n✅ Institution loading successful!")
        check_existing_data()  # Show updated count
    else:
        print("\n❌ Institution loading failed")
        print("Please check the RLS policies in your Supabase project")

if __name__ == "__main__":
    main()