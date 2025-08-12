"""
🏦 Basic TTM Calculations for Production Data

This script calculates TTM ratios using only the available columns in resumo_quarterly.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

def calculate_basic_ttm_ratios():
    """
    Calculate basic TTM ratios (ROE, ROA) using available resumo data.
    """
    
    print("🏦 CALCULATING BASIC TTM RATIOS ON PRODUCTION DATA")
    print("=" * 55)
    
    # Load the resumo data
    resumo_path = "data_restructured/core_tables/resumo_quarterly.csv"
    
    try:
        df = pd.read_csv(resumo_path)
        print(f"📊 Loaded resumo data: {len(df):,} records")
        print(f"   • Institutions: {df['CodInst'].nunique():,}")
        print(f"   • Date range: {df['AnoMes_Q'].min()} to {df['AnoMes_Q'].max()}")
        print(f"   • Available columns: {list(df.columns)}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {resumo_path}")
        return False
    
    print(f"\n🔄 Calculating TTM ratios...")
    
    # Prepare results list
    ttm_results = []
    
    # Get unique institution-period combinations for latest periods only
    # Filter for periods where we have at least 4 quarters of history
    df_sorted = df.sort_values(['CodInst', 'AnoMes_Q'])
    
    # Group by institution and get periods with sufficient history
    institutions_processed = 0
    total_institutions = df['CodInst'].nunique()
    
    for cod_inst in df['CodInst'].unique():
        institutions_processed += 1
        
        if institutions_processed % 100 == 0:
            print(f"   Processed {institutions_processed}/{total_institutions} institutions...")
        
        inst_data = df[df['CodInst'] == cod_inst].sort_values('AnoMes_Q').copy()
        
        if len(inst_data) < 4:  # Need at least 4 quarters for TTM
            continue
            
        institution_name = inst_data['NomeInstituicao'].iloc[0]
        
        # Calculate TTM for each period (starting from 4th quarter)
        for i in range(3, len(inst_data)):
            current_period = inst_data.iloc[i]
            period_name = current_period['AnoMes_Q']
            
            # Get last 4 quarters (including current)
            last_4_quarters = inst_data.iloc[i-3:i+1]
            
            # Calculate TTM Net Income (sum of last 4 quarters)
            ttm_net_income = last_4_quarters['Lucro_Liquido'].sum()
            
            # Calculate average equity (average of 5 quarters if available, otherwise 4)
            if i >= 4:
                equity_periods = inst_data.iloc[i-4:i+1]
            else:
                equity_periods = last_4_quarters
            avg_equity = equity_periods['Patrimonio_Liquido'].mean()
            
            # Calculate average total assets for ROA
            avg_assets = equity_periods['Ativo_Total'].mean()
            
            # Calculate TTM ratios
            roe_ttm = (ttm_net_income / avg_equity * 100) if avg_equity > 0 else np.nan
            roa_ttm = (ttm_net_income / avg_assets * 100) if avg_assets > 0 else np.nan
            
            # Store result
            result = {
                'CodInst': cod_inst,
                'NomeInstituicao': institution_name,
                'AnoMes_Q': period_name,
                'ROE_TTM': round(roe_ttm, 4) if not pd.isna(roe_ttm) else None,
                'ROA_TTM': round(roa_ttm, 4) if not pd.isna(roa_ttm) else None,
                'TTM_Net_Income': round(ttm_net_income, 2) if not pd.isna(ttm_net_income) else None,
                'Avg_Equity': round(avg_equity, 2) if not pd.isna(avg_equity) else None,
                'Avg_Assets': round(avg_assets, 2) if not pd.isna(avg_assets) else None,
                'Quarters_Used_Income': len(last_4_quarters),
                'Quarters_Used_Balance': len(equity_periods)
            }
            
            ttm_results.append(result)
    
    # Convert to DataFrame
    ttm_df = pd.DataFrame(ttm_results)
    
    # Save results
    output_path = Path("data_restructured/calculated_metrics/basic_ttm_ratios_quarterly.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    ttm_df.to_csv(output_path, index=False)
    print(f"💾 TTM ratios saved to: {output_path}")
    
    # Analysis
    print(f"\n📊 TTM ANALYSIS RESULTS:")
    
    total_records = len(ttm_df)
    valid_roe = ttm_df['ROE_TTM'].notna().sum()
    valid_roa = ttm_df['ROA_TTM'].notna().sum()
    
    print(f"   • Total institution-periods: {total_records:,}")
    print(f"   • Valid ROE calculations: {valid_roe:,} ({valid_roe/total_records*100:.1f}%)")
    print(f"   • Valid ROA calculations: {valid_roa:,} ({valid_roa/total_records*100:.1f}%)")
    
    # Sample results for latest period
    if len(ttm_df) > 0:
        latest_period = ttm_df['AnoMes_Q'].max()
        latest_data = ttm_df[ttm_df['AnoMes_Q'] == latest_period].copy()
        
        print(f"\n📋 LATEST PERIOD RESULTS ({latest_period}):")
        print(f"   • Institutions with data: {len(latest_data):,}")
        
        valid_latest = latest_data[latest_data['ROE_TTM'].notna()]
        if len(valid_latest) > 0:
            print(f"\n🏆 TOP 5 ROE PERFORMERS (TTM) - {latest_period}:")
            top_roe = valid_latest.nlargest(5, 'ROE_TTM')
            for idx, row in top_roe.iterrows():
                print(f"   • {row['NomeInstituicao'][:40]}: {row['ROE_TTM']:.2f}%")
            
            print(f"\n📊 TTM STATISTICS ({latest_period}):")
            print(f"   • ROE - Mean: {valid_latest['ROE_TTM'].mean():.2f}%")
            print(f"   • ROE - Median: {valid_latest['ROE_TTM'].median():.2f}%")
            print(f"   • ROA - Mean: {valid_latest['ROA_TTM'].mean():.2f}%")
            print(f"   • ROA - Median: {valid_latest['ROA_TTM'].median():.2f}%")
            
            # Show major banks if available
            major_banks = ['00000001', '00416968', '00558456', '60701190']
            major_data = valid_latest[valid_latest['CodInst'].isin(major_banks)]
            
            if len(major_data) > 0:
                print(f"\n🏛️  MAJOR BANKS TTM PERFORMANCE ({latest_period}):")
                for idx, row in major_data.iterrows():
                    bank_name = row['NomeInstituicao'][:30]
                    roe = row['ROE_TTM']
                    roa = row['ROA_TTM']
                    print(f"   • {bank_name}: ROE {roe:.2f}%, ROA {roa:.2f}%")
    
    return True

def demonstrate_ttm_improvement():
    """
    Show comparison between old point-in-time vs new TTM method.
    """
    
    print(f"\n" + "=" * 50)
    print("🎯 TTM IMPROVEMENT DEMONSTRATION")
    print("=" * 50)
    
    # Load original data
    df = pd.read_csv("data_restructured/core_tables/resumo_quarterly.csv")
    
    # Find institutions with good history
    institution_counts = df['CodInst'].value_counts()
    sample_institutions = institution_counts[institution_counts >= 8].head(3)
    
    for cod_inst in sample_institutions.index:
        inst_data = df[df['CodInst'] == cod_inst].sort_values('AnoMes_Q')
        if len(inst_data) < 8:
            continue
            
        institution_name = inst_data['NomeInstituicao'].iloc[0]
        latest_period = inst_data['AnoMes_Q'].iloc[-1]
        
        print(f"\n🏦 Institution: {institution_name[:40]}")
        print(f"📅 Latest Period: {latest_period}")
        
        # Old method (point-in-time)
        latest_data = inst_data.iloc[-1]
        if pd.notna(latest_data['Lucro_Liquido']) and pd.notna(latest_data['Patrimonio_Liquido']):
            old_roe = (latest_data['Lucro_Liquido'] / latest_data['Patrimonio_Liquido']) * 100
            
            # New method (TTM)
            last_4_quarters = inst_data.iloc[-4:]
            ttm_income = last_4_quarters['Lucro_Liquido'].sum()
            avg_equity = inst_data.iloc[-5:]['Patrimonio_Liquido'].mean() if len(inst_data) >= 5 else last_4_quarters['Patrimonio_Liquido'].mean()
            
            new_roe = (ttm_income / avg_equity) * 100 if avg_equity > 0 else np.nan
            
            if not pd.isna(new_roe):
                print(f"❌ Old Method (Point-in-time): {old_roe:.2f}%")
                print(f"✅ New Method (TTM): {new_roe:.2f}%")
                print(f"📊 Difference: {new_roe - old_roe:+.2f} percentage points")
                print(f"🔍 TTM Income: R$ {ttm_income:,.0f}")
                print(f"🔍 Avg Equity: R$ {avg_equity:,.0f}")
                break
    
    print(f"\n✅ Basic TTM calculations successfully applied to production data!")

if __name__ == "__main__":
    
    # Run basic TTM calculations
    success = calculate_basic_ttm_ratios()
    
    if success:
        # Demonstrate improvement
        demonstrate_ttm_improvement()
        
        print(f"\n🎉 BASIC TTM CALCULATIONS COMPLETE!")
        print(f"✅ Critical QA issue #2 RESOLVED (TTM methodology)")
        print(f"📊 Ready to proceed with sanity checks")
        
    else:
        print(f"❌ TTM calculation failed")