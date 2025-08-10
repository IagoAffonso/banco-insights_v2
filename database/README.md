# Banco Insights 2.0 - Database Design & Migration

This directory contains the complete database design, migration scripts, and deployment tools for Banco Insights 2.0, optimized for Supabase PostgreSQL.

## 📁 Directory Structure

```
database/
├── schema/
│   └── 001_initial_schema.sql      # Complete database schema
├── migrations/
│   ├── 001_seed_dimensions.sql     # Dimension table seeding
│   └── 002_etl_procedures.sql      # ETL functions and procedures
├── supabase/
│   ├── config.toml                 # Supabase configuration
│   └── deploy.py                   # Supabase deployment script
├── docker-compose.yml              # Local PostgreSQL setup
├── test_local_setup.py            # Local testing script
└── README.md                       # This file
```

## 🏗️ Database Architecture

### Design Principles

1. **Star Schema Design**: Optimized for analytics with dimension and fact tables
2. **Performance-First**: Materialized views and strategic indexing
3. **Frontend-Optimized**: Schema matches frontend data requirements
4. **Scalable**: Designed to handle 2000+ institutions and 12+ years of data
5. **BACEN Compliant**: Aligned with Brazilian banking regulatory structure

### Schema Overview

#### Dimension Tables
- `institutions` - Financial institutions master data
- `report_types` - 13 BACEN report categories
- `metric_groups` - 54 metric groupings from EDA analysis
- `metrics` - 208+ financial metrics and KPIs
- `time_periods` - Quarterly time dimension
- `geographic_regions` - Brazilian regions + international

#### Fact Tables
- `financial_data` - Main fact table with all financial metrics
  - Optimized composite unique constraints
  - Support for risk levels, maturity buckets, indexers
  - Audit trails and data lineage

#### Materialized Views
- `market_share_view` - Pre-calculated market share data
- `institution_summary_view` - Institution overview metrics
- `credit_portfolio_view` - Detailed credit portfolio analysis

## 🚀 Quick Start

### Local Development Setup

1. **Start Local PostgreSQL**:
   ```bash
   cd database
   docker-compose up -d
   ```

2. **Test Schema Setup**:
   ```bash
   pip install asyncpg pandas
   python test_local_setup.py
   ```

3. **Access Database**:
   - PostgreSQL: `localhost:5432` (postgres/postgres)
   - pgAdmin: `http://localhost:5050` (admin@bancoinights.com/admin)

### Supabase Deployment

1. **Configure Environment**:
   ```bash
   # Create .env file with your Supabase credentials
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-service-key
   SUPABASE_DB_URL=postgresql://user:pass@host:5432/dbname
   ```

2. **Deploy to Supabase**:
   ```bash
   cd supabase
   python deploy.py
   ```

## 📊 Key Features

### Performance Optimizations

1. **Strategic Indexing**:
   - Composite indexes on frequently queried columns
   - GIN indexes for full-text search
   - Partial indexes for filtered queries

2. **Materialized Views**:
   - Pre-calculated market share data
   - Aggregated institution summaries
   - Optimized credit portfolio views

3. **Query Performance**:
   - Sub-second response times for dashboard queries
   - Efficient time-series data retrieval
   - Optimized joins with proper foreign keys

### Data Quality & Integrity

1. **Comprehensive Constraints**:
   - Check constraints for data validation
   - Unique constraints to prevent duplicates
   - Foreign key relationships for referential integrity

2. **ETL Processing**:
   - Safe data type conversion functions
   - Error handling and logging
   - Batch processing capabilities

3. **Audit Trail**:
   - Created/updated timestamps
   - Data source tracking
   - Processing status monitoring

## 🔧 ETL Procedures

### Core ETL Functions

```sql
-- Process BACEN data in batches
SELECT * FROM process_bacen_data_batch(1000);

-- Process all pending data
SELECT * FROM process_all_bacen_data();

-- Check processing status
SELECT * FROM get_etl_status();

-- Refresh materialized views
SELECT refresh_all_materialized_views();
```

### Data Loading Workflow

1. **Stage Data**: Insert raw BACEN data into `staging_bacen_raw`
2. **Process**: Use ETL functions to clean and transform
3. **Validate**: Check data quality and completeness
4. **Refresh Views**: Update materialized views
5. **Monitor**: Track processing status and errors

## 🔒 Security & Access Control

### Row Level Security (RLS)

- **Public Read Access**: Authenticated users can read all data
- **Admin Write Access**: Only admin users can modify data
- **Policy-Based Security**: Fine-grained access control

### API Security

```sql
-- Example RLS policy
CREATE POLICY "authenticated_read" ON financial_data
FOR SELECT TO authenticated USING (true);

CREATE POLICY "admin_write" ON financial_data  
FOR ALL TO authenticated
USING (auth.jwt() ->> 'role' = 'admin');
```

## 📈 Data Model

### Institution Data Structure

Based on frontend requirements and BACEN taxonomy:

```typescript
interface Institution {
  id: UUID;
  cod_inst: string;        // BACEN institution code
  cnpj: string;           // Brazilian tax ID
  name: string;           // Full institution name
  short_name: string;     // Display name
  segment: 'S1'|'S2'|'S3'|'S4'|'S5'; // Size classification
  control_type: string;   // Ownership type
  region: string;         // Geographic region
  status: 'active'|'inactive';
}
```

### Financial Data Structure

```typescript
interface FinancialData {
  institution_id: UUID;
  time_period_id: UUID;
  report_type_id: UUID;
  metric_group_id: UUID; 
  metric_id: UUID;
  valor: number;          // Financial value
  risk_level?: string;    // AA to H
  maturity_bucket?: string;
  indexer?: string;       // Interest rate indexer
}
```

## 🧪 Testing

### Automated Tests

The `test_local_setup.py` script validates:

- ✅ Schema structure creation
- ✅ Index performance optimization
- ✅ Materialized view functionality
- ✅ ETL procedure execution
- ✅ Sample data insertion
- ✅ Query performance benchmarks

### Manual Testing

```bash
# Run comprehensive tests
python test_local_setup.py

# Check specific components
docker exec -it banco_insights_db psql -U postgres -d banco_insights
```

## 🔄 Migration Strategy

### From v1.0 to v2.0

1. **Extract Current Data**: Export from existing Streamlit/FastAPI setup
2. **Transform**: Use ETL procedures to clean and structure data
3. **Load**: Batch insert into new schema
4. **Validate**: Compare totals and key metrics
5. **Switch**: Update frontend to use new database

### Data Migration Commands

```bash
# Export from v1.0
python scripts/export_v1_data.py

# Transform and load
python database/supabase/migrate_v1_data.py

# Validate migration
python database/test_migration_integrity.py
```

## 📚 API Integration

### Supabase Functions

Custom PostgreSQL functions for common queries:

```sql
-- Get market share data
SELECT * FROM get_market_share(2024, 4, 'S1');

-- Get institution summary  
SELECT * FROM get_institution_summary(institution_uuid);

-- Get time series data
SELECT * FROM get_time_series_data('Ativo Total', 2020, 2024);
```

### REST API Endpoints

Supabase automatically generates REST API endpoints:

```
GET /rest/v1/institutions
GET /rest/v1/financial_data
GET /rest/v1/market_share_view
GET /rest/v1/institution_summary_view
```

## 🛠️ Maintenance

### Regular Maintenance Tasks

1. **Daily**: Refresh materialized views
2. **Weekly**: Analyze query performance
3. **Monthly**: Update statistics and vacuum
4. **Quarterly**: Load new BACEN data

### Performance Monitoring

```sql
-- Check query performance
SELECT * FROM pg_stat_statements;

-- Monitor index usage
SELECT * FROM pg_stat_user_indexes;

-- Check materialized view freshness
SELECT schemaname, matviewname, last_refresh 
FROM pg_matviews;
```

## 🔍 Troubleshooting

### Common Issues

1. **Connection Problems**:
   - Verify database URL and credentials
   - Check firewall settings
   - Confirm Supabase project status

2. **Performance Issues**:
   - Analyze slow queries with EXPLAIN
   - Check index usage statistics
   - Consider materialized view refresh

3. **Data Inconsistencies**:
   - Run ETL status checks
   - Validate foreign key constraints
   - Check for duplicate records

### Debug Commands

```sql
-- Check ETL status
SELECT * FROM get_etl_status();

-- View processing errors
SELECT * FROM staging_bacen_raw WHERE error_message IS NOT NULL;

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM market_share_view WHERE year = 2024;
```

## 📞 Support

For issues with the database setup:

1. Check the logs in `database_test_results_*.txt`
2. Review the schema documentation
3. Run the validation tests
4. Check Supabase dashboard for errors

---

**Status**: ✅ Phase 4 Complete - Database Design & Migration Ready

**Next Phase**: Integration with frontend and API development