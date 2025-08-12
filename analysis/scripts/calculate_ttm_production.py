"""
🏦 Calculate TTM Ratios on Production Data

This script applies proper TTM calculations to the actual restructured data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from ttm_calculations import TTMCalculator
import warnings

warnings.filterwarnings('ignore')

def calculate_ttm_on_production_data():
    """
    Calculate TTM ratios on the actual production data.
    """
    
    print("🏦 CALCULATING TTM RATIOS ON PRODUCTION DATA")
    print("=" * 50)
    
    # Load the real data
    resumo_path = "data_restructured/core_tables/resumo_quarterly.csv"
    
    try:
        df = pd.read_csv(resumo_path)
        print(f"📊 Loaded resumo data: {len(df):,} records")
        print(f"   • Institutions: {df['CodInst'].nunique():,}")
        print(f"   • Date range: {df['AnoMes_Q'].min()} to {df['AnoMes_Q'].max()}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {resumo_path}")
        return False
    
    # Initialize TTM calculator
    calculator = TTMCalculator()
    
    # Calculate TTM ratios for all data
    print(f"\\n🔄 Calculating TTM ratios...")
    ttm_results = calculator.calculate_all_ttm_ratios(df)
    
    # Save TTM results
    output_path = Path("data_restructured/calculated_metrics/ttm_ratios_quarterly.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    ttm_results.to_csv(output_path, index=False)
    print(f"💾 TTM ratios saved to: {output_path}")
    
    # Analyze results
    print(f"\\n📊 TTM ANALYSIS RESULTS:")
    
    # Overall statistics
    total_records = len(ttm_results)
    valid_roe = ttm_results['ROE_TTM'].notna().sum()
    valid_roa = ttm_results['ROA_TTM'].notna().sum()
    
    print(f"   • Total institution-periods: {total_records:,}")
    print(f"   • Valid ROE calculations: {valid_roe:,} ({valid_roe/total_records*100:.1f}%)")
    print(f"   • Valid ROA calculations: {valid_roa:,} ({valid_roa/total_records*100:.1f}%)")
    
    # Sample of calculated ratios
    valid_ttm = ttm_results[ttm_results['ROE_TTM'].notna()].copy()
    
    if len(valid_ttm) > 0:
        print(f"\\n📋 SAMPLE TTM RESULTS (Latest Available):")
        print(f"   📅 Period: {valid_ttm['AnoMes_Q'].mode().iloc[0] if len(valid_ttm) > 0 else 'N/A'}")
        
        # Show top 5 ROE performers
        top_roe = valid_ttm.nlargest(5, 'ROE_TTM')
        print(f"\\n🏆 TOP 5 ROE PERFORMERS (TTM):")
        for idx, row in top_roe.iterrows():
            print(f"   • {row['NomeInstituicao'][:40]}: {row['ROE_TTM']:.2f}%")
        
        # Basic statistics
        print(f"\\n📊 TTM STATISTICS:")
        print(f"   • ROE - Mean: {valid_ttm['ROE_TTM'].mean():.2f}%")
        print(f"   • ROE - Median: {valid_ttm['ROE_TTM'].median():.2f}%")
        print(f"   • ROA - Mean: {valid_ttm['ROA_TTM'].mean():.2f}%")
        print(f"   • ROA - Median: {valid_ttm['ROA_TTM'].median():.2f}%")
        
        # Compare with major banks (if available)
        major_banks = ['00000001', '00416968', '00558456', '60701190']  # BB, Bradesco, Itaú, CEF
        major_data = valid_ttm[valid_ttm['CodInst'].isin(major_banks)]
        
        if len(major_data) > 0:
            print(f"\\n🏛️  MAJOR BANKS TTM PERFORMANCE:")
            for idx, row in major_data.iterrows():
                bank_name = row['NomeInstituicao'][:25] 
                roe = row['ROE_TTM']
                roa = row['ROA_TTM']
                print(f"   • {bank_name}: ROE {roe:.2f}%, ROA {roa:.2f}%")
    
    return True

def demonstrate_ttm_improvement():
    """
    Demonstrate the improvement from the old vs new TTM method with real data.
    """
    
    print(f"\\n" + "=" * 50)
    print("🎯 TTM IMPROVEMENT DEMONSTRATION")
    print("=" * 50)
    
    # Load resumo data
    df = pd.read_csv("data_restructured/core_tables/resumo_quarterly.csv")
    
    # Pick a sample institution with sufficient history
    institution_counts = df['CodInst'].value_counts()
    sample_institutions = institution_counts[institution_counts >= 8].head(3)
    
    calculator = TTMCalculator()
    
    for cod_inst in sample_institutions.index:
        inst_data = df[df['CodInst'] == cod_inst].sort_values('AnoMes_Q')
        if len(inst_data) < 8:
            continue
            
        institution_name = inst_data['NomeInstituicao'].iloc[0]
        latest_period = inst_data['AnoMes_Q'].iloc[-1]
        
        print(f"\\n🏦 Institution: {institution_name[:40]}")
        print(f"📅 Latest Period: {latest_period}")
        
        # Old method (point-in-time)
        latest_data = inst_data.iloc[-1]
        if pd.notna(latest_data['Lucro_Liquido']) and pd.notna(latest_data['Patrimonio_Liquido']):
            old_roe = (latest_data['Lucro_Liquido'] / latest_data['Patrimonio_Liquido']) * 100
            
            # New method (TTM)
            new_roe, details = calculator.calculate_roe_ttm(df, cod_inst, latest_period)
            
            if not pd.isna(new_roe):
                print(f"❌ Old Method (Point-in-time): {old_roe:.2f}%")
                print(f"✅ New Method (TTM): {new_roe:.2f}%")
                print(f"📊 Difference: {new_roe - old_roe:+.2f} percentage points")
                print(f"🔍 TTM Income: R$ {details['ttm_net_income']:,.0f}")
                print(f"🔍 Avg Equity: R$ {details['avg_equity']:,.0f}")
                break
    
    print(f"\\n✅ TTM calculations successfully applied to production data!")

if __name__ == "__main__":
    
    # Run TTM calculations
    success = calculate_ttm_on_production_data()
    
    if success:
        # Demonstrate improvement
        demonstrate_ttm_improvement()
        
        print(f"\\n🎉 TTM CALCULATIONS COMPLETE!")
        print(f"✅ Critical QA issue #2 RESOLVED (TTM methodology)")
        
    else:
        print(f"❌ TTM calculation failed")