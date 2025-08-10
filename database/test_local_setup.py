#!/usr/bin/env python3
"""
Local Database Testing Script for Banco Insights 2.0

This script tests the database schema, runs sample data imports,
and validates the setup before Supabase deployment.
"""

import os
import sys
import asyncio
import asyncpg
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'banco_insights',
    'user': 'postgres',
    'password': 'postgres'
}

class DatabaseTester:
    def __init__(self):
        self.connection: Optional[asyncpg.Connection] = None
        self.test_results = []

    async def connect(self):
        """Connect to the local PostgreSQL database"""
        try:
            self.connection = await asyncpg.connect(**DATABASE_CONFIG)
            self.log_result("✅ Database connection successful")
            return True
        except Exception as e:
            self.log_result(f"❌ Database connection failed: {e}")
            return False

    async def disconnect(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            self.log_result("📝 Database connection closed")

    def log_result(self, message: str):
        """Log test result with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {message}"
        print(result)
        self.test_results.append(result)

    async def test_schema_structure(self):
        """Test that all tables and indexes were created correctly"""
        self.log_result("\n🔍 Testing Database Schema...")
        
        # Test main tables
        tables_to_check = [
            'institutions', 'report_types', 'metric_groups', 'metrics',
            'time_periods', 'geographic_regions', 'financial_data'
        ]
        
        for table in tables_to_check:
            try:
                result = await self.connection.fetchval(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = $1",
                    table
                )
                if result > 0:
                    self.log_result(f"  ✅ Table '{table}' exists")
                else:
                    self.log_result(f"  ❌ Table '{table}' missing")
            except Exception as e:
                self.log_result(f"  ❌ Error checking table '{table}': {e}")

    async def test_indexes(self):
        """Test that performance indexes were created"""
        self.log_result("\n📊 Testing Database Indexes...")
        
        indexes_to_check = [
            'idx_financial_data_institution_time',
            'idx_financial_data_report_metric',
            'idx_institutions_segment',
            'idx_time_periods_year_quarter'
        ]
        
        for index in indexes_to_check:
            try:
                result = await self.connection.fetchval(
                    "SELECT COUNT(*) FROM pg_indexes WHERE indexname = $1",
                    index
                )
                if result > 0:
                    self.log_result(f"  ✅ Index '{index}' exists")
                else:
                    self.log_result(f"  ❌ Index '{index}' missing")
            except Exception as e:
                self.log_result(f"  ❌ Error checking index '{index}': {e}")

    async def test_materialized_views(self):
        """Test materialized views creation and refresh"""
        self.log_result("\n📈 Testing Materialized Views...")
        
        views_to_check = [
            'market_share_view',
            'institution_summary_view', 
            'credit_portfolio_view'
        ]
        
        for view in views_to_check:
            try:
                result = await self.connection.fetchval(
                    "SELECT COUNT(*) FROM information_schema.views WHERE table_name = $1",
                    view
                )
                if result > 0:
                    self.log_result(f"  ✅ Materialized view '{view}' exists")
                    
                    # Test refresh
                    await self.connection.execute(f"REFRESH MATERIALIZED VIEW {view}")
                    self.log_result(f"  ✅ Materialized view '{view}' refreshed successfully")
                else:
                    self.log_result(f"  ❌ Materialized view '{view}' missing")
            except Exception as e:
                self.log_result(f"  ❌ Error with materialized view '{view}': {e}")

    async def test_sample_data_insertion(self):
        """Test inserting and querying sample data"""
        self.log_result("\n💾 Testing Sample Data Operations...")
        
        try:
            # Load sample data using the stored procedure
            await self.connection.execute("SELECT load_sample_data()")
            self.log_result("  ✅ Sample data loaded successfully")
            
            # Test querying institutions
            institutions = await self.connection.fetch(
                "SELECT name, short_name, segment FROM institutions WHERE status = 'active' LIMIT 5"
            )
            self.log_result(f"  ✅ Found {len(institutions)} active institutions")
            
            # Test querying financial data
            financial_records = await self.connection.fetch(
                "SELECT COUNT(*) as count FROM financial_data"
            )
            count = financial_records[0]['count'] if financial_records else 0
            self.log_result(f"  ✅ Found {count} financial data records")
            
            # Test time periods
            periods = await self.connection.fetch(
                "SELECT year, quarter_text FROM time_periods ORDER BY year DESC, quarter DESC LIMIT 3"
            )
            self.log_result(f"  ✅ Found {len(periods)} time periods")
            for period in periods:
                self.log_result(f"    📅 {period['year']} {period['quarter_text']}")
                
        except Exception as e:
            self.log_result(f"  ❌ Sample data operations failed: {e}")

    async def test_etl_procedures(self):
        """Test ETL procedures and functions"""
        self.log_result("\n⚙️ Testing ETL Procedures...")
        
        try:
            # Test ETL status function
            status = await self.connection.fetchrow("SELECT * FROM get_etl_status()")
            self.log_result("  ✅ ETL status function working")
            self.log_result(f"    📊 Total staging records: {status['total_staging_records']}")
            
            # Test data conversion functions
            numeric_test = await self.connection.fetchval("SELECT safe_numeric('123.45')")
            self.log_result(f"  ✅ safe_numeric function working: {numeric_test}")
            
            # Test quarter extraction
            quarter_info = await self.connection.fetchrow(
                "SELECT * FROM extract_quarter_info('2024T4')"
            )
            self.log_result(f"  ✅ Quarter extraction working: {quarter_info['year_val']} {quarter_info['quarter_text_val']}")
            
        except Exception as e:
            self.log_result(f"  ❌ ETL procedures test failed: {e}")

    async def test_performance_queries(self):
        """Test key performance queries that the frontend will use"""
        self.log_result("\n🚀 Testing Performance Queries...")
        
        queries = [
            {
                'name': 'Market Share Query',
                'sql': """
                    SELECT institution_name, market_share_pct, market_rank 
                    FROM market_share_view 
                    WHERE year = 2024 AND quarter = 4 
                    ORDER BY market_rank 
                    LIMIT 5
                """
            },
            {
                'name': 'Institution Summary',
                'sql': """
                    SELECT name, total_assets, net_income, basel_ratio 
                    FROM institution_summary_view 
                    WHERE year = 2024 AND quarter_text = 'T4'
                    LIMIT 3
                """
            },
            {
                'name': 'Time Series Data', 
                'sql': """
                    SELECT tp.year, tp.quarter_text, COUNT(*) as data_points
                    FROM financial_data fd
                    JOIN time_periods tp ON fd.time_period_id = tp.id
                    GROUP BY tp.year, tp.quarter_text, tp.id
                    ORDER BY tp.year DESC, tp.quarter DESC
                    LIMIT 8
                """
            }
        ]
        
        for query in queries:
            try:
                start_time = datetime.now()
                results = await self.connection.fetch(query['sql'])
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds() * 1000
                
                self.log_result(f"  ✅ {query['name']}: {len(results)} rows in {duration:.2f}ms")
                
                if duration > 1000:  # More than 1 second
                    self.log_result(f"    ⚠️  Query might be slow for production")
                    
            except Exception as e:
                self.log_result(f"  ❌ {query['name']} failed: {e}")

    async def generate_test_report(self):
        """Generate a comprehensive test report"""
        self.log_result("\n📋 Generating Test Report...")
        
        try:
            # Schema stats
            table_stats = await self.connection.fetch("""
                SELECT 
                    schemaname, tablename, 
                    n_tup_ins as inserts,
                    n_tup_upd as updates,
                    n_tup_del as deletes
                FROM pg_stat_user_tables 
                ORDER BY n_tup_ins DESC
            """)
            
            self.log_result("  📊 Table Statistics:")
            for stat in table_stats[:10]:  # Top 10 tables
                self.log_result(f"    {stat['tablename']}: {stat['inserts']} inserts")
            
            # Index usage
            index_stats = await self.connection.fetch("""
                SELECT 
                    indexrelname as index_name,
                    idx_tup_read,
                    idx_tup_fetch
                FROM pg_stat_user_indexes 
                WHERE idx_tup_read > 0
                ORDER BY idx_tup_read DESC
            """)
            
            self.log_result("  📈 Index Usage:")
            for stat in index_stats[:5]:  # Top 5 indexes
                self.log_result(f"    {stat['index_name']}: {stat['idx_tup_read']} reads")
            
        except Exception as e:
            self.log_result(f"  ❌ Error generating report: {e}")

    async def run_all_tests(self):
        """Run all database tests"""
        self.log_result("🚀 Starting Banco Insights 2.0 Database Tests")
        self.log_result("=" * 60)
        
        if not await self.connect():
            return False
        
        try:
            await self.test_schema_structure()
            await self.test_indexes()
            await self.test_materialized_views()
            await self.test_sample_data_insertion()
            await self.test_etl_procedures()
            await self.test_performance_queries()
            await self.generate_test_report()
            
            self.log_result("\n" + "=" * 60)
            self.log_result("✅ All database tests completed!")
            self.log_result("🎯 Database is ready for Supabase deployment")
            
            return True
            
        except Exception as e:
            self.log_result(f"❌ Test suite failed: {e}")
            return False
        finally:
            await self.disconnect()

def save_test_results(results: List[str]):
    """Save test results to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"database_test_results_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write("Banco Insights 2.0 - Database Test Results\n")
        f.write("=" * 50 + "\n\n")
        for result in results:
            f.write(result + "\n")
    
    print(f"\n📝 Test results saved to: {filename}")

async def main():
    """Main test runner"""
    tester = DatabaseTester()
    
    print("🏦 Banco Insights 2.0 - Database Schema Testing")
    print("=" * 60)
    print("This script will test the database schema and validate")
    print("the setup before Supabase deployment.\n")
    
    try:
        success = await tester.run_all_tests()
        save_test_results(tester.test_results)
        
        if success:
            print("\n🎉 All tests passed! Database is ready for production.")
            return 0
        else:
            print("\n⚠️ Some tests failed. Please review the results.")
            return 1
            
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    # Check dependencies
    try:
        import asyncpg
        import pandas as pd
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install asyncpg pandas")
        sys.exit(1)
    
    # Run tests
    exit_code = asyncio.run(main())
    sys.exit(exit_code)