#!/usr/bin/env python3
"""
Supabase Deployment Script for Banco Insights 2.0

This script handles the deployment of the database schema to Supabase,
including migrations, data seeding, and configuration validation.
"""

import os
import sys
import json
import asyncio
import asyncpg
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SupabaseConfig:
    """Supabase configuration data class"""
    project_url: str
    anon_key: str
    service_role_key: str
    database_url: str
    database_password: str

class SupabaseDeployer:
    def __init__(self, config_file: str = None):
        self.config_file = config_file or os.getenv('SUPABASE_CONFIG_FILE', '.env')
        self.config = self._load_config()
        self.connection: Optional[asyncpg.Connection] = None
        
    def _load_config(self) -> SupabaseConfig:
        """Load Supabase configuration from environment or config file"""
        # Try to load from environment variables first
        if all(os.getenv(key) for key in ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY']):
            return SupabaseConfig(
                project_url=os.getenv('SUPABASE_URL'),
                anon_key=os.getenv('SUPABASE_ANON_KEY'),
                service_role_key=os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
                database_url=os.getenv('SUPABASE_DB_URL'),
                database_password=os.getenv('SUPABASE_DB_PASSWORD')
            )
        
        # Try to load from .env file
        env_path = Path(self.config_file)
        if env_path.exists():
            config = {}
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key] = value.strip('"\'')
            
            return SupabaseConfig(
                project_url=config.get('SUPABASE_URL'),
                anon_key=config.get('SUPABASE_ANON_KEY'),
                service_role_key=config.get('SUPABASE_SERVICE_ROLE_KEY'),
                database_url=config.get('SUPABASE_DB_URL'),
                database_password=config.get('SUPABASE_DB_PASSWORD')
            )
        
        raise ValueError("Supabase configuration not found. Please set environment variables or create .env file.")

    async def connect_to_supabase(self) -> bool:
        """Connect to Supabase PostgreSQL database"""
        if not self.config.database_url:
            print("❌ Database URL not provided")
            return False
        
        try:
            self.connection = await asyncpg.connect(self.config.database_url)
            print("✅ Connected to Supabase database")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Supabase: {e}")
            return False

    async def disconnect(self):
        """Disconnect from database"""
        if self.connection:
            await self.connection.close()
            print("📝 Disconnected from Supabase database")

    def validate_supabase_cli(self) -> bool:
        """Validate that Supabase CLI is installed and configured"""
        try:
            result = subprocess.run(['supabase', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Supabase CLI found: {result.stdout.strip()}")
                return True
            else:
                print("❌ Supabase CLI not found")
                return False
        except FileNotFoundError:
            print("❌ Supabase CLI not installed")
            print("   Install with: npm install -g supabase")
            return False

    async def run_schema_migration(self) -> bool:
        """Run database schema migration on Supabase"""
        print("\n🗄️ Running Schema Migration...")
        
        schema_files = [
            "../schema/001_initial_schema.sql",
            "../migrations/001_seed_dimensions.sql", 
            "../migrations/002_etl_procedures.sql"
        ]
        
        for schema_file in schema_files:
            file_path = Path(__file__).parent / schema_file
            if not file_path.exists():
                print(f"❌ Schema file not found: {schema_file}")
                return False
                
            try:
                print(f"  📄 Executing {schema_file}...")
                with open(file_path, 'r') as f:
                    sql_content = f.read()
                
                # Split on semicolon and execute each statement
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for i, statement in enumerate(statements):
                    if statement:
                        try:
                            await self.connection.execute(statement)
                        except Exception as e:
                            # Log non-critical errors but continue
                            if "already exists" in str(e).lower():
                                continue  # Skip "already exists" errors
                            elif "relation" in str(e).lower() and "does not exist" in str(e).lower():
                                print(f"    ⚠️  Warning in statement {i+1}: {e}")
                                continue
                            else:
                                print(f"    ❌ Error in statement {i+1}: {e}")
                                return False
                
                print(f"  ✅ {schema_file} executed successfully")
                
            except Exception as e:
                print(f"  ❌ Failed to execute {schema_file}: {e}")
                return False
        
        return True

    async def configure_row_level_security(self) -> bool:
        """Configure Row Level Security policies for Supabase"""
        print("\n🔒 Configuring Row Level Security...")
        
        rls_policies = [
            # Read policies for authenticated users
            """
            CREATE POLICY IF NOT EXISTS "authenticated_read_institutions" 
            ON institutions FOR SELECT 
            TO authenticated 
            USING (true);
            """,
            """
            CREATE POLICY IF NOT EXISTS "authenticated_read_financial_data" 
            ON financial_data FOR SELECT 
            TO authenticated 
            USING (true);
            """,
            # Admin write policies
            """
            CREATE POLICY IF NOT EXISTS "admin_write_institutions" 
            ON institutions FOR ALL 
            TO authenticated 
            USING (
                EXISTS (
                    SELECT 1 FROM auth.users 
                    WHERE auth.users.id = auth.uid() 
                    AND auth.users.raw_user_meta_data->>'role' = 'admin'
                )
            );
            """,
            """
            CREATE POLICY IF NOT EXISTS "admin_write_financial_data" 
            ON financial_data FOR ALL 
            TO authenticated 
            USING (
                EXISTS (
                    SELECT 1 FROM auth.users 
                    WHERE auth.users.id = auth.uid() 
                    AND auth.users.raw_user_meta_data->>'role' = 'admin'
                )
            );
            """
        ]
        
        for policy in rls_policies:
            try:
                await self.connection.execute(policy)
                print("  ✅ RLS policy configured")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print("  ℹ️  RLS policy already exists")
                else:
                    print(f"  ❌ RLS policy failed: {e}")
                    return False
        
        return True

    async def create_supabase_functions(self) -> bool:
        """Create Supabase edge functions for API endpoints"""
        print("\n⚡ Creating Supabase Functions...")
        
        functions = {
            'market-share': {
                'description': 'Get market share data for institutions',
                'sql': """
                    CREATE OR REPLACE FUNCTION get_market_share(
                        p_year INTEGER DEFAULT NULL,
                        p_quarter INTEGER DEFAULT NULL,
                        p_segment TEXT DEFAULT NULL
                    )
                    RETURNS TABLE (
                        institution_id UUID,
                        institution_name TEXT,
                        market_share NUMERIC,
                        rank INTEGER
                    ) 
                    LANGUAGE plpgsql
                    SECURITY DEFINER
                    AS $$
                    BEGIN
                        RETURN QUERY
                        SELECT 
                            ms.institution_id,
                            ms.institution_name,
                            ms.market_share_pct,
                            ms.market_rank::INTEGER
                        FROM market_share_view ms
                        WHERE 
                            (p_year IS NULL OR ms.year = p_year)
                            AND (p_quarter IS NULL OR ms.quarter = p_quarter)
                            AND (p_segment IS NULL OR ms.segment = p_segment)
                        ORDER BY ms.market_rank;
                    END;
                    $$;
                """
            },
            'institution-summary': {
                'description': 'Get institution summary data',
                'sql': """
                    CREATE OR REPLACE FUNCTION get_institution_summary(
                        p_institution_id UUID DEFAULT NULL,
                        p_year INTEGER DEFAULT NULL
                    )
                    RETURNS TABLE (
                        institution_id UUID,
                        name TEXT,
                        total_assets NUMERIC,
                        net_income NUMERIC,
                        basel_ratio NUMERIC
                    )
                    LANGUAGE plpgsql
                    SECURITY DEFINER
                    AS $$
                    BEGIN
                        RETURN QUERY
                        SELECT 
                            isv.institution_id,
                            isv.name,
                            isv.total_assets,
                            isv.net_income,
                            isv.basel_ratio
                        FROM institution_summary_view isv
                        WHERE 
                            (p_institution_id IS NULL OR isv.institution_id = p_institution_id)
                            AND (p_year IS NULL OR isv.year = p_year)
                        ORDER BY isv.total_assets DESC NULLS LAST;
                    END;
                    $$;
                """
            }
        }
        
        for func_name, func_config in functions.items():
            try:
                await self.connection.execute(func_config['sql'])
                print(f"  ✅ Function '{func_name}' created")
            except Exception as e:
                print(f"  ❌ Function '{func_name}' failed: {e}")
                return False
        
        return True

    async def refresh_materialized_views(self) -> bool:
        """Refresh materialized views after data loading"""
        print("\n🔄 Refreshing Materialized Views...")
        
        try:
            result = await self.connection.fetch("SELECT * FROM refresh_materialized_views_with_log()")
            for row in result:
                print(f"  ✅ {row['view_name']} refreshed in {row['refresh_time']}")
            return True
        except Exception as e:
            print(f"  ❌ Failed to refresh views: {e}")
            return False

    async def validate_deployment(self) -> bool:
        """Validate the Supabase deployment"""
        print("\n✅ Validating Deployment...")
        
        validations = [
            {
                'name': 'Tables Created',
                'sql': "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
            },
            {
                'name': 'Sample Data Present',
                'sql': "SELECT COUNT(*) FROM institutions"
            },
            {
                'name': 'Financial Data Present',
                'sql': "SELECT COUNT(*) FROM financial_data"
            },
            {
                'name': 'Views Working',
                'sql': "SELECT COUNT(*) FROM market_share_view"
            }
        ]
        
        for validation in validations:
            try:
                result = await self.connection.fetchval(validation['sql'])
                print(f"  ✅ {validation['name']}: {result}")
            except Exception as e:
                print(f"  ❌ {validation['name']} failed: {e}")
                return False
        
        return True

    def generate_environment_file(self):
        """Generate .env file with Supabase configuration"""
        print("\n📝 Generating Environment Configuration...")
        
        env_content = f"""# Banco Insights 2.0 - Supabase Configuration
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL={self.config.project_url}
NEXT_PUBLIC_SUPABASE_ANON_KEY={self.config.anon_key}
SUPABASE_SERVICE_ROLE_KEY={self.config.service_role_key}

# Database Configuration
SUPABASE_DB_URL={self.config.database_url}
DATABASE_URL={self.config.database_url}

# Application Configuration
NODE_ENV=production
NEXT_PUBLIC_APP_NAME="Banco Insights 2.0"
NEXT_PUBLIC_APP_VERSION="2.0.0"

# API Configuration
API_BASE_URL={self.config.project_url}/rest/v1
API_KEY={self.config.anon_key}

# Security Configuration
JWT_SECRET={self.config.service_role_key}
ENCRYPTION_KEY="your-encryption-key-here"

# Optional: External Services
SENTRY_DSN=""
GOOGLE_ANALYTICS_ID=""
"""
        
        with open('../../.env.production', 'w') as f:
            f.write(env_content)
        
        print("  ✅ Environment file created: .env.production")
        print("  ⚠️  Remember to update encryption keys and external service configurations")

    async def deploy_to_supabase(self) -> bool:
        """Main deployment workflow"""
        print("🚀 Starting Supabase Deployment for Banco Insights 2.0")
        print("=" * 70)
        
        # Validate prerequisites
        if not self.validate_supabase_cli():
            return False
        
        # Connect to Supabase
        if not await self.connect_to_supabase():
            return False
        
        try:
            # Run migrations
            if not await self.run_schema_migration():
                return False
            
            # Configure security
            if not await self.configure_row_level_security():
                return False
            
            # Create functions
            if not await self.create_supabase_functions():
                return False
            
            # Refresh views
            if not await self.refresh_materialized_views():
                return False
            
            # Validate deployment
            if not await self.validate_deployment():
                return False
            
            # Generate configuration
            self.generate_environment_file()
            
            print("\n" + "=" * 70)
            print("🎉 Supabase deployment completed successfully!")
            print("🎯 Database is ready for production use")
            print("\n📋 Next Steps:")
            print("1. Update frontend environment variables")
            print("2. Configure authentication providers")
            print("3. Set up monitoring and alerts")
            print("4. Load production data using ETL procedures")
            
            return True
            
        except Exception as e:
            print(f"💥 Deployment failed: {e}")
            return False
        finally:
            await self.disconnect()

def main():
    """Main entry point"""
    print("🏦 Banco Insights 2.0 - Supabase Deployment Tool")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
Usage: python deploy.py [config_file]

This script deploys the Banco Insights 2.0 database schema to Supabase.

Environment Variables Required:
- SUPABASE_URL: Your Supabase project URL
- SUPABASE_ANON_KEY: Your Supabase anonymous key
- SUPABASE_SERVICE_ROLE_KEY: Your Supabase service role key
- SUPABASE_DB_URL: Your Supabase database URL
- SUPABASE_DB_PASSWORD: Your database password

Alternatively, create a .env file with these variables.
""")
        return 0
    
    try:
        deployer = SupabaseDeployer(sys.argv[1] if len(sys.argv) > 1 else None)
        success = asyncio.run(deployer.deploy_to_supabase())
        return 0 if success else 1
    except Exception as e:
        print(f"💥 Deployment error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())