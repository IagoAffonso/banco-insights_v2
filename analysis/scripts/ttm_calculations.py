"""
🏦 TTM (Trailing Twelve Months) Calculations Module

This module implements proper TTM calculations for financial ratios following BACEN standards,
addressing the critical issue identified in the QA review.

Key Fix: ROE/ROA now use TTM methodology instead of point-in-time calculations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

class TTMCalculator:
    """
    Proper Trailing Twelve Months calculations for Brazilian banking ratios.
    
    Follows BACEN standards:
    - TTM Income: Sum of last 4 quarters
    - Average Balances: Average of 5 quarter-end values (current + last 4)
    """
    
    def __init__(self):
        self.quarter_sequence = self._generate_quarter_sequence()
    
    def _generate_quarter_sequence(self) -> List[str]:
        """Generate proper quarterly sequence for period calculations"""
        quarters = []
        for year in range(2013, 2025):
            for q in [1, 2, 3, 4]:
                quarters.append(f"{year}Q{q}")
        return quarters
    
    def calculate_ttm_income(self, df: pd.DataFrame, institution_code: str, 
                            period: str, income_column: str) -> float:
        """
        Calculate Trailing Twelve Months income (sum of last 4 quarters).
        
        Args:
            df: DataFrame with quarterly data
            institution_code: Institution identifier
            period: Current quarter (e.g., '2024Q3')
            income_column: Column name for income metric (e.g., 'Lucro_Liquido')
            
        Returns:
            TTM income value or NaN if insufficient data
        """
        
        # Get the last 4 quarters including current period
        period_idx = self._get_period_index(period)
        if period_idx < 3:  # Need at least 4 quarters
            return np.nan
            
        last_4_quarters = self.quarter_sequence[period_idx-3:period_idx+1]
        
        # Filter data for institution and periods
        inst_data = df[
            (df['CodInst'] == institution_code) & 
            (df['AnoMes_Q'].isin(last_4_quarters))
        ].copy()
        
        if len(inst_data) < 4:
            return np.nan
            
        # Sum the last 4 quarters
        ttm_income = inst_data[income_column].sum()
        return ttm_income
    
    def calculate_average_balance(self, df: pd.DataFrame, institution_code: str,
                                 period: str, balance_column: str) -> float:
        """
        Calculate average balance using 5 quarter-end values (BACEN standard).
        
        Args:
            df: DataFrame with quarterly data
            institution_code: Institution identifier  
            period: Current quarter (e.g., '2024Q3')
            balance_column: Column name for balance metric (e.g., 'Ativo_Total')
            
        Returns:
            Average balance or NaN if insufficient data
        """
        
        # Get current + last 4 quarters (5 total)
        period_idx = self._get_period_index(period)
        if period_idx < 4:  # Need at least 5 quarters
            return np.nan
            
        last_5_quarters = self.quarter_sequence[period_idx-4:period_idx+1]
        
        # Filter data for institution and periods
        inst_data = df[
            (df['CodInst'] == institution_code) & 
            (df['AnoMes_Q'].isin(last_5_quarters))
        ].copy()
        
        if len(inst_data) < 5:
            return np.nan
            
        # Calculate average of the 5 quarter-end balances
        avg_balance = inst_data[balance_column].mean()
        return avg_balance
    
    def calculate_roe_ttm(self, df: pd.DataFrame, institution_code: str, 
                         period: str) -> Tuple[float, Dict]:
        """
        Calculate proper ROE using TTM methodology.
        
        Formula: ROE = (TTM Net Income / Average Shareholders' Equity) × 100
        
        Returns:
            Tuple of (ROE value, calculation details)
        """
        
        # Calculate TTM net income
        ttm_income = self.calculate_ttm_income(
            df, institution_code, period, 'Lucro_Liquido'
        )
        
        # Calculate average equity
        avg_equity = self.calculate_average_balance(
            df, institution_code, period, 'Patrimonio_Liquido'
        )
        
        # Calculate ROE
        if pd.isna(ttm_income) or pd.isna(avg_equity) or avg_equity <= 0:
            roe = np.nan
        else:
            roe = (ttm_income / avg_equity) * 100
        
        # Return calculation details for audit trail
        details = {
            'ttm_net_income': ttm_income,
            'avg_equity': avg_equity,
            'roe_percent': roe,
            'methodology': 'TTM Income / Average Equity (5Q)',
            'formula': '(Sum Last 4Q Net Income) / (Avg Last 5Q Equity) × 100'
        }
        
        return roe, details
    
    def calculate_roa_ttm(self, df: pd.DataFrame, institution_code: str,
                         period: str) -> Tuple[float, Dict]:
        """
        Calculate proper ROA using TTM methodology.
        
        Formula: ROA = (TTM Net Income / Average Total Assets) × 100
        
        Returns:
            Tuple of (ROA value, calculation details)
        """
        
        # Calculate TTM net income
        ttm_income = self.calculate_ttm_income(
            df, institution_code, period, 'Lucro_Liquido'
        )
        
        # Calculate average assets
        avg_assets = self.calculate_average_balance(
            df, institution_code, period, 'Ativo_Total'
        )
        
        # Calculate ROA
        if pd.isna(ttm_income) or pd.isna(avg_assets) or avg_assets <= 0:
            roa = np.nan
        else:
            roa = (ttm_income / avg_assets) * 100
        
        # Return calculation details for audit trail
        details = {
            'ttm_net_income': ttm_income,
            'avg_assets': avg_assets,
            'roa_percent': roa,
            'methodology': 'TTM Income / Average Assets (5Q)',
            'formula': '(Sum Last 4Q Net Income) / (Avg Last 5Q Assets) × 100'
        }
        
        return roa, details
    
    def calculate_nim_ttm(self, df: pd.DataFrame, institution_code: str,
                         period: str) -> Tuple[float, Dict]:
        """
        Calculate Net Interest Margin using TTM methodology.
        
        Formula: NIM = (TTM Net Interest Income / Average Earning Assets) × 100
        
        Returns:
            Tuple of (NIM value, calculation details)
        """
        
        # Calculate TTM net interest income
        ttm_interest_income = self.calculate_ttm_income(
            df, institution_code, period, 'Resultado_de_Intermediacao_Financeira'
        )
        
        # Calculate average earning assets (credit + securities + interbank)
        # We'll approximate with credit portfolio + TVM
        credit_avg = self.calculate_average_balance(
            df, institution_code, period, 'Carteira_de_Credito_Classificada'
        )
        
        # For NIM calculation, earning assets ≈ credit portfolio (main earning component)
        avg_earning_assets = credit_avg
        
        # Calculate NIM
        if pd.isna(ttm_interest_income) or pd.isna(avg_earning_assets) or avg_earning_assets <= 0:
            nim = np.nan
        else:
            nim = (ttm_interest_income / avg_earning_assets) * 100
        
        details = {
            'ttm_net_interest_income': ttm_interest_income,
            'avg_earning_assets': avg_earning_assets,
            'nim_percent': nim,
            'methodology': 'TTM Interest Result / Average Credit Portfolio',
            'formula': '(Sum Last 4Q Interest Result) / (Avg Last 5Q Credit) × 100'
        }
        
        return nim, details
    
    def _get_period_index(self, period: str) -> int:
        """Get index of period in quarter sequence"""
        try:
            return self.quarter_sequence.index(period)
        except ValueError:
            return -1
    
    def calculate_all_ttm_ratios(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all TTM ratios for all institutions and periods.
        
        Args:
            df: DataFrame with quarterly data
            
        Returns:
            DataFrame with TTM calculations
        """
        
        results = []
        
        # Get unique institution-period combinations
        combinations = df[['CodInst', 'NomeInstituicao', 'AnoMes_Q']].drop_duplicates()
        
        print(f"🔄 Calculating TTM ratios for {len(combinations)} institution-period combinations...")
        
        for idx, row in combinations.iterrows():
            if idx % 100 == 0:
                print(f"   Processed {idx}/{len(combinations)} combinations...")
                
            institution_code = row['CodInst']
            institution_name = row['NomeInstituicao'] 
            period = row['AnoMes_Q']
            
            # Calculate TTM ratios
            roe, roe_details = self.calculate_roe_ttm(df, institution_code, period)
            roa, roa_details = self.calculate_roa_ttm(df, institution_code, period)
            nim, nim_details = self.calculate_nim_ttm(df, institution_code, period)
            
            result = {
                'CodInst': institution_code,
                'NomeInstituicao': institution_name,
                'AnoMes_Q': period,
                'ROE_TTM': round(roe, 4) if not pd.isna(roe) else None,
                'ROA_TTM': round(roa, 4) if not pd.isna(roa) else None,
                'NIM_TTM': round(nim, 4) if not pd.isna(nim) else None,
                'TTM_Net_Income': roe_details['ttm_net_income'],
                'Avg_Equity': roe_details['avg_equity'],
                'Avg_Assets': roa_details['avg_assets'],
                'Calculation_Method': 'BACEN_TTM_Standard'
            }
            
            results.append(result)
        
        results_df = pd.DataFrame(results)
        
        # Summary statistics
        valid_roe = results_df['ROE_TTM'].notna().sum()
        valid_roa = results_df['ROA_TTM'].notna().sum()
        total = len(results_df)
        
        print(f"\n📊 TTM Calculation Results:")
        print(f"   • Total combinations: {total:,}")
        print(f"   • Valid ROE calculations: {valid_roe:,} ({valid_roe/total*100:.1f}%)")
        print(f"   • Valid ROA calculations: {valid_roa:,} ({valid_roa/total*100:.1f}%)")
        
        return results_df

def demonstrate_ttm_calculation():
    """
    Demonstrate TTM calculations with sample data to show the improvement.
    """
    
    # Create sample quarterly data for demonstration
    sample_data = []
    
    # Sample institution data across 8 quarters
    institution_code = '00000001'
    institution_name = 'Banco Exemplo S.A.'
    
    quarters = ['2023Q1', '2023Q2', '2023Q3', '2023Q4', '2024Q1', '2024Q2', '2024Q3', '2024Q4']
    
    # Sample quarterly values with realistic growth
    quarterly_data = {
        '2023Q1': {'net_income': 15000000, 'equity': 240000000, 'assets': 1800000000},
        '2023Q2': {'net_income': 18000000, 'equity': 245000000, 'assets': 1850000000},
        '2023Q3': {'net_income': 20000000, 'equity': 250000000, 'assets': 1900000000}, 
        '2023Q4': {'net_income': 22000000, 'equity': 255000000, 'assets': 1950000000},
        '2024Q1': {'net_income': 17000000, 'equity': 260000000, 'assets': 2000000000},
        '2024Q2': {'net_income': 21000000, 'equity': 265000000, 'assets': 2050000000},
        '2024Q3': {'net_income': 24000000, 'equity': 270000000, 'assets': 2100000000},
        '2024Q4': {'net_income': 26000000, 'equity': 275000000, 'assets': 2150000000}
    }
    
    for quarter in quarters:
        sample_data.append({
            'CodInst': institution_code,
            'NomeInstituicao': institution_name,
            'AnoMes_Q': quarter,
            'Lucro_Liquido': quarterly_data[quarter]['net_income'],
            'Patrimonio_Liquido': quarterly_data[quarter]['equity'],
            'Ativo_Total': quarterly_data[quarter]['assets'],
            'Carteira_de_Credito_Classificada': quarterly_data[quarter]['assets'] * 0.6,
            'Resultado_de_Intermediacao_Financeira': quarterly_data[quarter]['net_income'] * 1.5
        })
    
    sample_df = pd.DataFrame(sample_data)
    
    # Calculate TTM for Q3 2024
    calculator = TTMCalculator()
    
    # Old way (WRONG)
    current_period_data = sample_df[sample_df['AnoMes_Q'] == '2024Q3'].iloc[0]
    old_roe = (current_period_data['Lucro_Liquido'] / current_period_data['Patrimonio_Liquido']) * 100
    old_roa = (current_period_data['Lucro_Liquido'] / current_period_data['Ativo_Total']) * 100
    
    # New way (CORRECT TTM)
    new_roe, roe_details = calculator.calculate_roe_ttm(sample_df, institution_code, '2024Q3')
    new_roa, roa_details = calculator.calculate_roa_ttm(sample_df, institution_code, '2024Q3')
    
    print("🏦 TTM CALCULATION DEMONSTRATION")
    print("=" * 50)
    print(f"Institution: {institution_name}")
    print(f"Period: 2024Q3")
    
    print(f"\n❌ OLD METHOD (Point-in-time - INCORRECT):")
    print(f"   • ROE: {old_roe:.2f}% (Q3 2024 only)")
    print(f"   • ROA: {old_roa:.2f}% (Q3 2024 only)")
    
    print(f"\n✅ NEW METHOD (TTM - CORRECT):")
    print(f"   • ROE: {new_roe:.2f}% (TTM)")
    print(f"   • ROA: {new_roa:.2f}% (TTM)")
    
    print(f"\n🔍 TTM Calculation Details:")
    print(f"   • TTM Net Income: R$ {roe_details['ttm_net_income']:,.0f}")
    print(f"     (Sum of Q4'23 + Q1'24 + Q2'24 + Q3'24)")
    print(f"   • Average Equity: R$ {roe_details['avg_equity']:,.0f}")
    print(f"     (Average of 5 quarters: Q3'23 to Q3'24)")
    print(f"   • Average Assets: R$ {roa_details['avg_assets']:,.0f}")
    
    print(f"\n📊 Impact Analysis:")
    roe_diff = new_roe - old_roe
    roa_diff = new_roa - old_roa
    print(f"   • ROE Difference: {roe_diff:+.2f} percentage points")
    print(f"   • ROA Difference: {roa_diff:+.2f} percentage points")
    print(f"   • Method: BACEN Standard TTM")
    
    return sample_df

if __name__ == "__main__":
    # Run demonstration
    demonstrate_ttm_calculation()
    
    print(f"\n✅ TTM calculation module ready!")
    print("This fixes the critical issue identified in the QA review.")