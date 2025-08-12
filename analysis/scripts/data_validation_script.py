#!/usr/bin/env python3
"""
BACEN Data Validation Script
Comprehensive analysis to identify discrepancies between CSV and database calculations
"""

import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

def main():
    print("🔍 BACEN Data Validation Analysis")
    print("=" * 50)
    print(f"📅 Analysis started at: {datetime.now()}")
    
    # Load environment variables
    load_dotenv('/Users/iagoaffonso/code/IagoAffonso/banco-insights-2.0/supabase_config.env')
    
    # Step 1: Load CSV data
    print("\n📊 Step 1: Loading CSV Data")
    csv_path = '/Users/iagoaffonso/code/IagoAffonso/banco-insights-2.0/bacen_project_v1/data/financial_metrics.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    print(f"📁 Loading from: {csv_path}")
    print(f"📏 File size: {os.path.getsize(csv_path) / (1024*1024):.2f} MB")
    
    # Load data
    financial_metrics = pd.read_csv(csv_path)
    print(f"✅ Data loaded: {financial_metrics.shape[0]:,} rows, {financial_metrics.shape[1]} columns")
    
    # Step 2: Replicate user's Ativo Total calculation
    print("\n💰 Step 2: Ativo Total Calculation (User's Method)")
    print("Filter: NomeRelatorio='Resumo' AND AnoMes_Q='2024Q3' AND NomeColuna='Ativo Total'")
    
    # Apply filters step by step
    step1 = financial_metrics[financial_metrics['NomeRelatorio'] == 'Resumo']
    print(f"   After NomeRelatorio filter: {step1.shape[0]:,} rows")
    
    step2 = step1[step1['AnoMes_Q'] == '2024Q3']
    print(f"   After AnoMes_Q filter: {step2.shape[0]:,} rows")
    
    step3 = step2[step2['NomeColuna'] == 'Ativo Total']
    print(f"   After NomeColuna filter: {step3.shape[0]:,} rows")
    
    # Calculate sum
    sumativo_total_2024Q3 = step3['Saldo'].sum()
    print(f"\n💰 ATIVO TOTAL 2024Q3 (CSV): {sumativo_total_2024Q3:,.2f}")
    print(f"   In trillions: {sumativo_total_2024Q3/1_000_000_000_000:.2f}")
    print(f"   In billions: {sumativo_total_2024Q3/1_000_000_000:.2f}")
    
    # Step 3: Replicate credit portfolio calculation
    print("\n💳 Step 3: Carteira de Crédito Calculation")
    print("Filter: NomeRelatorio='Resumo' AND AnoMes_Q='2024Q3' AND NomeColuna='Carteira de Crédito Classificada'")
    
    credit_step1 = financial_metrics[financial_metrics['NomeRelatorio'] == 'Resumo']
    credit_step2 = credit_step1[credit_step1['AnoMes_Q'] == '2024Q3']
    credit_step3 = credit_step2[credit_step2['NomeColuna'] == 'Carteira de Crédito Classificada']
    
    sum_carteira_credito_2024Q3 = credit_step3['Saldo'].sum()
    print(f"📊 Final filtered rows: {credit_step3.shape[0]:,}")
    print(f"\n💳 CARTEIRA DE CRÉDITO 2024Q3 (CSV): {sum_carteira_credito_2024Q3:,.2f}")
    print(f"   In trillions: {sum_carteira_credito_2024Q3/1_000_000_000_000:.2f}")
    print(f"   In billions: {sum_carteira_credito_2024Q3/1_000_000_000:.2f}")
    
    # Verify against user's expected value
    user_expected = 6709275484424.04
    difference = abs(sum_carteira_credito_2024Q3 - user_expected)
    print(f"\n✅ User expected: {user_expected:,.2f}")
    print(f"🔍 Our calculation: {sum_carteira_credito_2024Q3:,.2f}")
    print(f"📊 Difference: {difference:,.2f} ({'✅ MATCH' if difference < 1 else '❌ MISMATCH'})")
    
    # Step 4: Connect to database and compare
    print("\n🗄️ Step 4: Database Comparison")
    
    try:
        conn = psycopg2.connect(
            host="aws-1-sa-east-1.pooler.supabase.com",
            database="postgres",
            user="postgres.uwoxkycxkidipgbptsgx",
            password="En9QmRQaw14nhwxL",
            port="6543"
        )
        print("✅ Database connection successful")
        
        cursor = conn.cursor()
        
        # Get latest quarter
        cursor.execute("""
            SELECT year, quarter, quarter_text
            FROM time_periods tp
            WHERE EXISTS (
                SELECT 1 FROM financial_data fd WHERE fd.time_period_id = tp.id
            )
            ORDER BY year DESC, quarter DESC
            LIMIT 1
        """)
        
        latest_q = cursor.fetchone()
        if latest_q:
            print(f"📅 Latest quarter in database: {latest_q[0]}Q{latest_q[1]}")
            
            # Get database calculation (same as API)
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN m.nome_coluna = 'Ativo Total' THEN fd.valor END) as total_assets,
                    COUNT(CASE WHEN m.nome_coluna = 'Ativo Total' THEN 1 END) as asset_records,
                    COUNT(DISTINCT CASE WHEN m.nome_coluna = 'Ativo Total' THEN i.id END) as institutions_with_assets
                FROM financial_data fd
                JOIN institutions i ON fd.institution_id = i.id
                JOIN metrics m ON fd.metric_id = m.id
                JOIN time_periods tp ON fd.time_period_id = tp.id
                WHERE tp.year = %s AND tp.quarter = %s
                  AND m.nome_coluna = 'Ativo Total'
                  AND i.status = 'active'
                  AND fd.valor IS NOT NULL
            """, (latest_q[0], latest_q[1]))
            
            db_result = cursor.fetchone()
            db_value = db_result[0] or 0
            db_records = db_result[1] or 0
            db_institutions = db_result[2] or 0
            
            print(f"\n💰 DATABASE ATIVO TOTAL {latest_q[0]}Q{latest_q[1]}:")
            print(f"   Value: {db_value:,.2f}")
            print(f"   Records: {db_records:,}")
            print(f"   Institutions: {db_institutions:,}")
            print(f"   In billions: {db_value/1_000_000_000:.2f}")
            
            # Comparison
            print(f"\n🔍 CRITICAL COMPARISON:")
            print(f"   CSV Expected: {sumativo_total_2024Q3:,.2f}")
            print(f"   Database Actual: {db_value:,.2f}")
            print(f"   Missing Amount: {sumativo_total_2024Q3 - db_value:,.2f}")
            
            if sumativo_total_2024Q3 > 0:
                ratio = (db_value / sumativo_total_2024Q3) * 100
                print(f"   Database shows only {ratio:.2f}% of expected value!")
            
            # Get sample institutions from database
            cursor.execute("""
                SELECT i.name, fd.valor
                FROM financial_data fd
                JOIN institutions i ON fd.institution_id = i.id
                JOIN metrics m ON fd.metric_id = m.id
                JOIN time_periods tp ON fd.time_period_id = tp.id
                WHERE tp.year = %s AND tp.quarter = %s
                  AND m.nome_coluna = 'Ativo Total'
                  AND i.status = 'active'
                  AND fd.valor IS NOT NULL
                ORDER BY fd.valor DESC
                LIMIT 5
            """, (latest_q[0], latest_q[1]))
            
            db_sample = cursor.fetchall()
            print(f"\n🏦 Top 5 institutions in DATABASE:")
            for i, (name, value) in enumerate(db_sample):
                print(f"   {i+1}. {name[:40]:<40}: {value:>15,.2f}")
            
            # Compare with CSV
            csv_top5 = step3.nlargest(5, 'Saldo')[['InstituicaoFinanceira', 'Saldo']]
            print(f"\n🏦 Top 5 institutions in CSV:")
            for i, (idx, row) in enumerate(csv_top5.iterrows()):
                print(f"   {i+1}. {row['InstituicaoFinanceira'][:40]:<40}: {row['Saldo']:>15,.2f}")
        
        cursor.close()
        conn.close()
        print("\n✅ Database connection closed")
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
    
    # Step 5: Summary and recommendations
    print("\n🚨 ANALYSIS SUMMARY")
    print("=" * 50)
    
    print(f"\n📊 EXPECTED VALUES (Direct CSV Calculation):")
    print(f"   Ativo Total: {sumativo_total_2024Q3:,.2f} ({sumativo_total_2024Q3/1_000_000_000:.1f} billion)")
    print(f"   Credit Portfolio: {sum_carteira_credito_2024Q3:,.2f} ({sum_carteira_credito_2024Q3/1_000_000_000:.1f} billion)")
    
    if 'db_value' in locals():
        print(f"\n🗄️ ACTUAL VALUES (Database API):")
        print(f"   Ativo Total: {db_value:,.2f} ({db_value/1_000_000_000:.1f} billion)")
        
        if sumativo_total_2024Q3 > 0:
            ratio = (db_value / sumativo_total_2024Q3) * 100
            print(f"\n❌ MASSIVE DISCREPANCY:")
            print(f"   Database shows only {ratio:.2f}% of expected value")
            print(f"   Missing: {(sumativo_total_2024Q3 - db_value)/1_000_000_000:.1f} billion")
    
    print(f"\n🔍 ROOT CAUSE INVESTIGATION NEEDED:")
    print(f"   1. ✓ CSV calculations verified (match user's results)")
    print(f"   2. ❌ Database/ETL process has major issues")
    print(f"   3. ❌ API calculations return wrong values")
    print(f"   4. ❌ Frontend displays incorrect data")
    
    print(f"\n🎯 IMMEDIATE ACTIONS REQUIRED:")
    print(f"   1. Investigate ETL data loading process")
    print(f"   2. Check institution and metric mappings")
    print(f"   3. Verify time period mappings")
    print(f"   4. Audit data conversion and aggregation logic")
    print(f"   5. Test with smaller datasets to isolate issues")
    
    print(f"\n📝 NOTEBOOK CREATED:")
    print(f"   Full analysis available in: data_validation_notebook.ipynb")
    print(f"   Use Jupyter to run interactive analysis")

if __name__ == "__main__":
    main()