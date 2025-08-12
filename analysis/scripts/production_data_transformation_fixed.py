"""
🏦 Production Data Transformation Script - Fixed Version

This script safely processes the actual consolidated_cleaned.csv file.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import os
import warnings

warnings.filterwarnings('ignore')

def safe_process_key_tables():
    """
    Process only the most critical tables first to test the system.
    """
    
    print("🏦 BANCO INSIGHTS 2.0 - SAFE PRODUCTION TRANSFORMATION")
    print("=" * 60)
    
    source_file = "bacen_project_v1/data/consolidated_cleaned.csv"
    
    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        return False
    
    # Load unique identifiers
    try:
        with open('EDA/unique_values.json', 'r') as f:
            unique_values = json.load(f)
        available_ids = set(unique_values.get('NomeRelatorio_Grupo_Coluna', []))
        print(f"📊 Loaded {len(available_ids)} unique identifiers")
    except Exception as e:
        print(f"❌ Error loading identifiers: {e}")
        return False
    
    # Define key tables to process
    key_tables = {
        'resumo_quarterly': {
            'Ativo_Total': 'Resumo_nagroup_Ativo Total',
            'Patrimonio_Liquido': 'Resumo_nagroup_Patrimônio Líquido',
            'Lucro_Liquido': 'Resumo_nagroup_Lucro Líquido',
            'Captacoes': 'Resumo_nagroup_Captações'
        },
        'credito_clientes_operacoes_quarterly': {
            'Quantidade_de_Clientes_com_Operacoes_Ativas': 'Carteira de crédito ativa - quantidade de clientes e de operações_nagroup_Quantidade de clientes com operações ativas',
            'Quantidade_de_Operacoes_Ativas': 'Carteira de crédito ativa - quantidade de clientes e de operações_nagroup_Quantidade de operações ativas'
        }
    }
    
    # Process each table
    results = {}
    
    for table_name, metrics in key_tables.items():
        print(f"\\n🔄 Processing {table_name}...")
        
        # Validate metrics exist
        valid_metrics = {}
        for clean_name, identifier in metrics.items():
            if identifier in available_ids:
                valid_metrics[clean_name] = identifier
            else:
                print(f"   ⚠️  Missing: {clean_name}")
        
        if not valid_metrics:
            print(f"   ❌ No valid metrics found for {table_name}")
            results[table_name] = False
            continue
        
        print(f"   ✅ Found {len(valid_metrics)} valid metrics")
        
        # Process in chunks
        try:
            chunk_results = []
            chunk_size = 50000
            total_chunks = 0
            relevant_rows = 0
            
            chunk_iter = pd.read_csv(
                source_file,
                chunksize=chunk_size,
                dtype={'CodInst': str, 'Saldo': float}
            )
            
            for chunk_num, chunk in enumerate(chunk_iter, 1):
                total_chunks = chunk_num
                
                # Filter for our metrics
                relevant = chunk[
                    chunk['NomeRelatorio_Grupo_Coluna'].isin(valid_metrics.values())
                ].copy()
                
                if len(relevant) == 0:
                    continue
                
                relevant_rows += len(relevant)
                
                # Create reverse mapping
                reverse_map = {v: k for k, v in valid_metrics.items()}
                relevant['Clean_Metric'] = relevant['NomeRelatorio_Grupo_Coluna'].map(reverse_map)
                
                # Pivot to wide format
                try:
                    pivoted = relevant.pivot_table(
                        index=['CodInst', 'NomeInstituicao', 'AnoMes', 'AnoMes_Q', 'AnoMes_Y'],
                        columns='Clean_Metric',
                        values='Saldo',
                        aggfunc='first'
                    ).reset_index()
                    
                    pivoted.columns.name = None
                    
                    if len(pivoted) > 0:
                        chunk_results.append(pivoted)
                        
                except Exception as e:
                    print(f"   ⚠️  Error pivoting chunk {chunk_num}: {e}")
                
                if chunk_num % 20 == 0:
                    print(f"     📈 Processed {chunk_num} chunks, {relevant_rows:,} relevant rows")
            
            print(f"   📊 Summary: {total_chunks:,} chunks, {relevant_rows:,} relevant rows")
            
            # Combine results
            if chunk_results:
                final_df = pd.concat(chunk_results, ignore_index=True)
                
                # Remove duplicates
                initial_rows = len(final_df)
                final_df = final_df.drop_duplicates(subset=['CodInst', 'AnoMes'], keep='last')
                
                print(f"   🔧 Deduplication: {initial_rows:,} → {len(final_df):,} rows")
                print(f"   🏛️  Institutions: {final_df['CodInst'].nunique():,}")
                print(f"   📅 Date range: {final_df['AnoMes_Q'].min()} to {final_df['AnoMes_Q'].max()}")
                
                # Save result
                output_path = Path("data_restructured/core_tables") / f"{table_name}.csv"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                final_df.to_csv(output_path, index=False)
                
                print(f"   💾 Saved: {output_path}")
                results[table_name] = True
            else:
                print(f"   ❌ No data found")
                results[table_name] = False
                
        except Exception as e:
            print(f"   ❌ Error processing {table_name}: {e}")
            results[table_name] = False
    
    # Summary
    successful = sum(results.values())
    total = len(results)
    
    print(f"\\n📋 TRANSFORMATION SUMMARY")
    print(f"   • Success rate: {successful}/{total} ({successful/total*100:.1f}%)")
    
    if successful == total:
        print("   🎉 ALL KEY TABLES PROCESSED SUCCESSFULLY!")
        return True
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"   ⚠️  Failed tables: {', '.join(failed)}")
        return False

if __name__ == "__main__":
    success = safe_process_key_tables()
    
    if success:
        print("\\n🚀 Next steps ready:")
        print("   1. ✅ Core tables created")
        print("   2. 🔄 Ready for TTM calculations")
        print("   3. 🔄 Ready for sanity checks")
    else:
        print("\\n❌ Review errors above before proceeding")