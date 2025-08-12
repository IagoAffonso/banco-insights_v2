"""
🏦 Market Analysis Calculations Supplement
Focusing on Customer-Based Market Share Analysis

This module documents the market analysis calculations with special emphasis on 
'Quantidade de Clientes com Operacoes Ativas' as highlighted by the user.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class MarketAnalysisCalculations:
    """
    Comprehensive market analysis calculations for Banco Insights platform.
    Includes both monetary and customer-based market share analysis.
    """
    
    @staticmethod
    def calculate_customer_market_share(df: pd.DataFrame, period: str) -> pd.DataFrame:
        """
        Calculate market share based on active customer count.
        
        This is a crucial metric that shows:
        - Customer penetration by institution
        - Banking democratization trends
        - Different business model approaches
        - Digital vs traditional bank reach
        
        Args:
            df: DataFrame with customer count data
            period: Quarter period (e.g., '2024Q3')
            
        Returns:
            DataFrame with customer market share analysis
        """
        
        # Filter for specific period
        period_data = df[df['AnoMes_Q'] == period].copy()
        
        # Calculate total market customers
        total_market_customers = period_data['Quantidade_de_Clientes_com_Operacoes_Ativas'].sum()
        
        # Calculate market share for each institution
        period_data['Customer_Market_Share_Pct'] = (
            period_data['Quantidade_de_Clientes_com_Operacoes_Ativas'] / total_market_customers * 100
        )
        
        # Rank institutions by customer count
        period_data['Customer_Market_Rank'] = period_data['Quantidade_de_Clientes_com_Operacoes_Ativas'].rank(
            ascending=False, method='dense'
        ).astype(int)
        
        # Calculate cumulative market share
        period_data = period_data.sort_values('Quantidade_de_Clientes_com_Operacoes_Ativas', ascending=False)
        period_data['Cumulative_Customer_Share'] = period_data['Customer_Market_Share_Pct'].cumsum()
        
        # Business model classification based on customers vs assets
        # This helps identify different strategic approaches
        period_data['Customer_Asset_Ratio'] = (
            period_data['Customer_Market_Share_Pct'] / period_data.get('Asset_Market_Share_Pct', 1)
        )
        
        def classify_business_model(ratio):
            if ratio > 1.2:
                return "Mass Market" # High customers, lower assets per customer
            elif ratio < 0.8:
                return "Premium/Corporate" # Lower customers, higher assets per customer  
            else:
                return "Balanced" # Proportional customers and assets
                
        period_data['Business_Model_Type'] = period_data['Customer_Asset_Ratio'].apply(classify_business_model)
        
        return period_data[['CodInst', 'NomeInstituicao', 'AnoMes_Q',
                          'Quantidade_de_Clientes_com_Operacoes_Ativas',
                          'Customer_Market_Share_Pct', 'Customer_Market_Rank',
                          'Cumulative_Customer_Share', 'Business_Model_Type']]
    
    @staticmethod
    def calculate_market_concentration_hhi(market_shares: List[float]) -> float:
        """
        Calculate Herfindahl-Hirschman Index (HHI) for market concentration.
        
        Args:
            market_shares: List of market share percentages
            
        Returns:
            HHI value (0-10000 scale)
            
        Interpretation:
            • HHI < 1500: Competitive market
            • HHI 1500-2500: Moderately concentrated
            • HHI > 2500: Highly concentrated
        """
        hhi = sum(share**2 for share in market_shares)
        return round(hhi, 2)
    
    @staticmethod
    def calculate_concentration_ratios(df: pd.DataFrame, top_n_list: List[int] = [4, 5, 10, 20]) -> Dict:
        """
        Calculate concentration ratios (CR) for top N institutions.
        
        Args:
            df: DataFrame with market share data
            top_n_list: List of top N values to calculate
            
        Returns:
            Dictionary with concentration ratios
        """
        # Sort by market share descending
        df_sorted = df.sort_values('Customer_Market_Share_Pct', ascending=False)
        
        concentration_ratios = {}
        for n in top_n_list:
            if len(df_sorted) >= n:
                cr_n = df_sorted['Customer_Market_Share_Pct'].head(n).sum()
                concentration_ratios[f'CR{n}'] = round(cr_n, 2)
            
        return concentration_ratios
    
    @staticmethod
    def analyze_customer_growth_trends(df: pd.DataFrame, institution_code: str, periods: int = 8) -> Dict:
        """
        Analyze customer growth trends for a specific institution.
        
        Args:
            df: DataFrame with historical customer data
            institution_code: Institution code to analyze
            periods: Number of quarters to analyze
            
        Returns:
            Dictionary with growth analysis
        """
        
        # Filter for specific institution and recent periods
        inst_data = df[df['CodInst'] == institution_code].sort_values('AnoMes_Q').tail(periods)
        
        if len(inst_data) < 2:
            return {'error': 'Insufficient data for growth analysis'}
        
        # Calculate quarterly growth rates
        inst_data['QoQ_Customer_Growth'] = inst_data['Quantidade_de_Clientes_com_Operacoes_Ativas'].pct_change() * 100
        
        # Calculate year-over-year growth (if enough data)
        if len(inst_data) >= 4:
            inst_data['YoY_Customer_Growth'] = inst_data['Quantidade_de_Clientes_com_Operacoes_Ativas'].pct_change(periods=4) * 100
        
        growth_analysis = {
            'institution_code': institution_code,
            'latest_customer_count': int(inst_data['Quantidade_de_Clientes_com_Operacoes_Ativas'].iloc[-1]),
            'latest_qoq_growth': round(inst_data['QoQ_Customer_Growth'].iloc[-1], 2),
            'avg_qoq_growth': round(inst_data['QoQ_Customer_Growth'].mean(), 2),
            'customer_growth_volatility': round(inst_data['QoQ_Customer_Growth'].std(), 2),
            'periods_analyzed': len(inst_data)
        }
        
        if 'YoY_Customer_Growth' in inst_data.columns:
            growth_analysis['latest_yoy_growth'] = round(inst_data['YoY_Customer_Growth'].iloc[-1], 2)
            growth_analysis['avg_yoy_growth'] = round(inst_data['YoY_Customer_Growth'].mean(), 2)
        
        return growth_analysis

# Example usage and documentation
def demonstrate_customer_market_analysis():
    """
    Demonstrate customer market share analysis with sample data.
    This shows how the metrics work in practice.
    """
    
    # Sample data representing customer counts for major Brazilian banks
    sample_data = pd.DataFrame({
        'CodInst': ['00000001', '00416968', '00558456', '60701190', '00000208', '03017677'],
        'NomeInstituicao': [
            'Banco do Brasil S.A.',
            'Banco Bradesco S.A.', 
            'Itaú Unibanco S.A.',
            'Caixa Econômica Federal',
            'Banco Santander S.A.',
            'Banco Inter S.A.'
        ],
        'AnoMes_Q': ['2024Q3'] * 6,
        'Quantidade_de_Clientes_com_Operacoes_Ativas': [
            45000000,  # BB - Large state bank
            35000000,  # Bradesco - Large private bank
            40000000,  # Itaú - Large private bank
            50000000,  # CEF - State bank with social programs
            15000000,  # Santander - Foreign bank
            12000000   # Inter - Digital bank
        ],
        # Also include asset market share for comparison
        'Asset_Market_Share_Pct': [18.5, 15.2, 16.8, 12.3, 8.1, 2.1]
    })
    
    # Calculate customer market share
    market_analysis = MarketAnalysisCalculations.calculate_customer_market_share(sample_data, '2024Q3')
    
    print("🎯 Customer Market Share Analysis - Sample Results:")
    print("="*60)
    
    for _, row in market_analysis.iterrows():
        print(f"\n🏦 {row['NomeInstituicao']}")
        print(f"   • Active Customers: {row['Quantidade_de_Clientes_com_Operacoes_Ativas']:,}")
        print(f"   • Customer Market Share: {row['Customer_Market_Share_Pct']:.2f}%")
        print(f"   • Market Rank: #{row['Customer_Market_Rank']}")
        print(f"   • Business Model: {row['Business_Model_Type']}")
    
    # Calculate market concentration
    customer_shares = market_analysis['Customer_Market_Share_Pct'].tolist()
    hhi_customers = MarketAnalysisCalculations.calculate_market_concentration_hhi(customer_shares)
    concentration_ratios = MarketAnalysisCalculations.calculate_concentration_ratios(market_analysis)
    
    print(f"\n📊 Market Concentration Analysis:")
    print(f"   • HHI Index: {hhi_customers} ({'Competitive' if hhi_customers < 1500 else 'Moderately Concentrated' if hhi_customers < 2500 else 'Highly Concentrated'})")
    
    for cr_name, cr_value in concentration_ratios.items():
        print(f"   • {cr_name}: {cr_value}%")
    
    print(f"\n🔍 Key Insights:")
    print(f"   • Total Market: {sample_data['Quantidade_de_Clientes_com_Operacoes_Ativas'].sum():,} active customers")
    print(f"   • Top 3 concentration: {market_analysis['Customer_Market_Share_Pct'].head(3).sum():.1f}%")
    
    # Identify business model differences
    mass_market_banks = market_analysis[market_analysis['Business_Model_Type'] == 'Mass Market']['NomeInstituicao'].tolist()
    premium_banks = market_analysis[market_analysis['Business_Model_Type'] == 'Premium/Corporate']['NomeInstituicao'].tolist()
    
    if mass_market_banks:
        print(f"   • Mass Market Focus: {', '.join(mass_market_banks)}")
    if premium_banks:
        print(f"   • Premium/Corporate Focus: {', '.join(premium_banks)}")

# Statistical aggregations for customer metrics
class CustomerMetricAggregations:
    """
    Statistical aggregations specifically for customer-based metrics.
    """
    
    @staticmethod
    def calculate_customer_statistics(df: pd.DataFrame, groupby_cols: List[str] = None) -> Dict:
        """
        Calculate comprehensive statistics for customer metrics.
        
        Args:
            df: DataFrame with customer data
            groupby_cols: Columns to group by (e.g., ['AnoMes_Q'] for time series)
            
        Returns:
            Dictionary with statistical measures
        """
        
        customer_col = 'Quantidade_de_Clientes_com_Operacoes_Ativas'
        
        if groupby_cols:
            grouped_stats = df.groupby(groupby_cols)[customer_col].agg([
                'sum',      # Total market customers
                'mean',     # Average per institution
                'median',   # Median per institution  
                'std',      # Standard deviation
                'min',      # Minimum
                'max',      # Maximum
                'count'     # Number of institutions
            ]).round(0)
            
            # Add coefficient of variation (volatility measure)
            grouped_stats['coefficient_variation'] = (grouped_stats['std'] / grouped_stats['mean'] * 100).round(2)
            
            return grouped_stats
        else:
            # Single period statistics
            stats = {
                'total_market_customers': df[customer_col].sum(),
                'avg_customers_per_institution': df[customer_col].mean(),
                'median_customers_per_institution': df[customer_col].median(),
                'customer_distribution_std': df[customer_col].std(),
                'largest_institution_customers': df[customer_col].max(),
                'smallest_institution_customers': df[customer_col].min(),
                'total_institutions': len(df),
                'coefficient_variation': (df[customer_col].std() / df[customer_col].mean() * 100)
            }
            
            return {k: round(v, 0) if isinstance(v, float) else v for k, v in stats.items()}

if __name__ == "__main__":
    # Run demonstration
    demonstrate_customer_market_analysis()
    
    print(f"\n" + "="*60)
    print("📋 This analysis highlights why 'Quantidade de Clientes com Operacoes Ativas'")
    print("   is such a valuable metric for banking market intelligence!")
    print("="*60)