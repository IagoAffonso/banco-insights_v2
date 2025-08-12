#!/usr/bin/env python3
"""
Test Supabase Connection with different configurations
"""

import psycopg2
import requests
import json

# Test different connection configurations
configs_to_test = [
    {
        'name': 'Config 1: Standard Supabase',
        'host': 'db.uwoxkycxkidipgbptsgx.supabase.co',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres',
        'password': 'En9QmRQaw14nhwxL'
    },
    {
        'name': 'Config 2: Supabase External Port',
        'host': 'db.uwoxkycxkidipgbptsgx.supabase.co',
        'port': 6543,
        'database': 'postgres',
        'user': 'postgres',
        'password': 'En9QmRQaw14nhwxL'
    },
    {
        'name': 'Config 3: Supabase with Project User',
        'host': 'db.uwoxkycxkidipgbptsgx.supabase.co',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres.uwoxkycxkidipgbptsgx',
        'password': 'En9QmRQaw14nhwxL'
    }
]

def test_supabase_api():
    """Test Supabase REST API connectivity"""
    print("🌐 Testing Supabase REST API...")
    
    url = "https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1/"
    headers = {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"✅ Supabase API accessible - Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Supabase API test failed: {e}")
        return False

def test_database_connections():
    """Test different database connection configurations"""
    print("\n🔌 Testing PostgreSQL connections...")
    
    for config in configs_to_test:
        print(f"\n📋 {config['name']}")
        try:
            conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
                connect_timeout=10
            )
            
            with conn.cursor() as cursor:
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
                print(f"✅ Connected! PostgreSQL version: {version[:50]}...")
            
            conn.close()
            return config  # Return successful config
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    return None

def main():
    """Main test function"""
    print("🧪 SUPABASE CONNECTION TESTING")
    print("=" * 50)
    
    # Test API connectivity
    api_works = test_supabase_api()
    
    # Test database connectivity
    successful_config = test_database_connections()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    print(f"🌐 Supabase API: {'✅ Working' if api_works else '❌ Failed'}")
    print(f"🗄️ Database: {'✅ Working' if successful_config else '❌ Failed'}")
    
    if successful_config:
        print(f"\n🎉 SUCCESS! Use this configuration:")
        print(f"Host: {successful_config['host']}")
        print(f"Port: {successful_config['port']}")
        print(f"User: {successful_config['user']}")
        print(f"Database: {successful_config['database']}")
        
        # Save successful config
        with open('working_supabase_config.json', 'w') as f:
            json.dump(successful_config, f, indent=2)
        print(f"📝 Saved working config to: working_supabase_config.json")
    else:
        print(f"\n💥 No working database configuration found")
        print(f"Please check your Supabase project settings at:")
        print(f"https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx/settings/database")

if __name__ == "__main__":
    main()