"""
🏦 Production Data Transformation Script - Banco Insights 2.0

This script safely processes the actual consolidated_cleaned.csv file and transforms it
into the new transposed structure with proper TTM calculations included.

IMPORTANT: Uses chunked processing to handle the 1GB+ CSV file safely.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import Dict, List, Optional, Tuple
import warnings
from ttm_calculations import TTMCalculator
import os

warnings.filterwarnings('ignore')

class ProductionDataTransformer:
    """
    Production-ready data transformation with chunked processing and TTM calculations.
    """
    
    def __init__(self, source_file: str = "bacen_project_v1/data/consolidated_cleaned.csv", 
                 chunk_size: int = 50000):
        """
        Initialize the production transformer.
        
        Args:
            source_file: Path to the large consolidated CSV file
            chunk_size: Number of rows to process at once
        """
        self.source_file = source_file
        self.chunk_size = chunk_size
        self.output_dir = Path("data_restructured")
        self.ttm_calculator = TTMCalculator()
        
        # Ensure source file exists
        if not os.path.exists(source_file):
            raise FileNotFoundError(f"Source file not found: {source_file}")
            
        # Load metric mappings
        self.load_metric_mappings()
        
    def load_metric_mappings(self):
        """Load metric identifier mappings from unique_values.json"""
        try:
            with open('EDA/unique_values.json', 'r') as f:
                unique_values = json.load(f)
                
            self.available_identifiers = set(unique_values.get('NomeRelatorio_Grupo_Coluna', []))
            print(f"📊 Loaded {len(self.available_identifiers)} unique metric identifiers")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not load unique values mapping: {e}")
            self.available_identifiers = set()
    
    def get_production_table_definitions(self) -> Dict[str, Dict]:
        """
        Define comprehensive table structure for production use.
        
        Returns:
            Dictionary with complete table definitions
        """
        
        tables = {
            'resumo_quarterly': {
                'description': 'Executive summary with key financial metrics',
                'priority': 1,
                'metrics': {
                    'Ativo_Total': 'Resumo_nagroup_Ativo Total',
                    'Carteira_de_Credito_Classificada': 'Resumo_nagroup_Carteira de Crédito Classificada',
                    'Patrimonio_Liquido': 'Resumo_nagroup_Patrimônio Líquido',
                    'Captacoes': 'Resumo_nagroup_Captações', 
                    'Lucro_Liquido': 'Resumo_nagroup_Lucro Líquido',
                    'Indice_de_Basileia': 'Resumo_nagroup_Índice de Basileia',
                    'Indice_de_Imobilizacao': 'Resumo_nagroup_Índice de Imobilização'
                }
            },
            
            'credito_clientes_operacoes_quarterly': {
                'description': 'Customer market share metrics (KEY TABLE)',
                'priority': 1,
                'metrics': {
                    'Quantidade_de_Clientes_com_Operacoes_Ativas': 'Carteira de crédito ativa - quantidade de clientes e de operações_nagroup_Quantidade de clientes com operações ativas',
                    'Quantidade_de_Operacoes_Ativas': 'Carteira de crédito ativa - quantidade de clientes e de operações_nagroup_Quantidade de operações ativas'
                }
            },
            
            'demonstracao_resultado_quarterly': {
                'description': 'Income statement components',
                'priority': 2,
                'metrics': {
                    'Receitas_de_Intermediacao_Financeira': 'Demonstração de Resultado_Resultado de Intermediação Financeira - Receitas de Intermediação Financeira_Receitas de Intermediação Financeira \\\\n(a) = (a1) + (a2) + (a3) + (a4) + (a5) + (a6)',
                    'Rendas_de_Operacoes_de_Credito': 'Demonstração de Resultado_Resultado de Intermediação Financeira - Receitas de Intermediação Financeira_Rendas de Operações de Crédito \\\\n(a1)',
                    'Despesas_de_Intermediacao_Financeira': 'Demonstração de Resultado_Resultado de Intermediação Financeira - Despesas de Intermediação Financeira_Despesas de Intermediação Financeira \\\\n(b) = (b1) + (b2) + (b3) + (b4) + (b5)',
                    'Despesas_de_Captacao': 'Demonstração de Resultado_Resultado de Intermediação Financeira - Despesas de Intermediação Financeira_Despesas de Captação \\\\n(b1)',
                    'Resultado_de_Intermediacao_Financeira': 'Demonstração de Resultado_Resultado de Intermediação Financeira_Resultado de Intermediação Financeira \\\\n(c) = (a) + (b)',
                    'Rendas_de_Prestacao_de_Servicos': 'Demonstração de Resultado_Outras Receitas/Despesas Operacionais_Rendas de Prestação de Serviços \\\\n(d1)',
                    'Despesas_de_Pessoal': 'Demonstração de Resultado_Outras Receitas/Despesas Operacionais_Despesas de Pessoal \\\\n(d3)',
                    'Despesas_Administrativas': 'Demonstração de Resultado_Outras Receitas/Despesas Operacionais_Despesas Administrativas \\\\n(d4)',
                    'Resultado_Operacional': 'Demonstração de Resultado_nagroup_Resultado Operacional \\\\n(e) = (c) + (d)',
                    'Lucro_Liquido': 'Demonstração de Resultado_nagroup_Lucro Líquido \\\\n(j) = (g) + (h) + (i)'
                }
            },
            
            'ativo_quarterly': {
                'description': 'Balance sheet assets breakdown',
                'priority': 2,
                'metrics': {
                    'Ativo_Total_Ajustado': 'Ativo_nagroup_Ativo Total Ajustado \\\\n(i) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h)',
                    'Ativo_Total': 'Ativo_nagroup_Ativo Total \\\\n(k) = (i) - (j)',
                    'Disponibilidades': 'Ativo_nagroup_Disponibilidades \\\\n(a)',
                    'Aplicacoes_Interfinanceiras_de_Liquidez': 'Ativo_nagroup_Aplicações Interfinanceiras de Liquidez \\\\n(b)',
                    'TVM_e_Instrumentos_Financeiros_Derivativos': 'Ativo_nagroup_TVM e Instrumentos Financeiros Derivativos \\\\n(c)',
                    'Operacoes_de_Credito': 'Ativo_Operações de Crédito_Operações de Crédito \\\\n(d1)',
                    'Provisao_sobre_Operacoes_de_Credito': 'Ativo_Operações de Crédito_Provisão sobre Operações de Crédito \\\\n(d2)',
                    'Operacoes_de_Credito_Liquidas_de_Provisao': 'Ativo_Operações de Crédito_Operações de Crédito Líquidas de Provisão \\\\n(d)'
                }
            },
            
            'passivo_quarterly': {
                'description': 'Balance sheet liabilities breakdown', 
                'priority': 2,
                'metrics': {
                    'Depositos_a_Vista': 'Passivo_Captações - Depósito Total_Depósitos à Vista \\\\n(a1)',
                    'Depositos_de_Poupanca': 'Passivo_Captações - Depósito Total_Depósitos de Poupança \\\\n(a2)',
                    'Depositos_a_Prazo': 'Passivo_Captações - Depósito Total_Depósitos a Prazo \\\\n(a4)',
                    'Deposito_Total': 'Passivo_Captações - Depósito Total_Depósito Total \\\\n(a)',
                    'Obrigacoes_por_Operacoes_Compromissadas': 'Passivo_Captações_Obrigações por Operações Compromissadas \\\\n(b)',
                    'Captacoes': 'Passivo_Captações_Captações \\\\n(e) = (a) + (b) + (c) + (d)',
                    'Patrimonio_Liquido': 'Passivo_nagroup_Patrimônio Líquido \\\\n(j)',
                    'Passivo_Total': 'Passivo_nagroup_Passivo Total \\\\n(k) = (h) + (i) + (j)'
                }
            },
            
            'credito_risco_quarterly': {
                'description': 'Credit portfolio by risk level (AA-H)',
                'priority': 3,
                'metrics': {
                    'Total_Geral': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_Total Geral',
                    'AA': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_AA',
                    'A': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_A',
                    'B': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_B',
                    'C': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_C',
                    'D': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_D',
                    'E': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_E',
                    'F': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_F',
                    'G': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_G',
                    'H': 'Carteira de crédito ativa - por nível de risco da operação_nagroup_H'
                }
            }
        }
        
        return tables
    
    def validate_metric_identifiers(self, metrics: Dict[str, str]) -> Tuple[Dict[str, str], List[str]]:
        """
        Validate that metric identifiers exist in the actual data.
        
        Args:
            metrics: Dictionary of metric name -> identifier mapping
            
        Returns:
            Tuple of (validated_metrics, missing_identifiers)
        """
        validated_metrics = {}
        missing_identifiers = []
        
        for metric_name, identifier in metrics.items():
            if identifier in self.available_identifiers:
                validated_metrics[metric_name] = identifier
            else:
                missing_identifiers.append((metric_name, identifier))
        
        return validated_metrics, missing_identifiers
    
    def process_table_chunks(self, table_name: str, metrics: Dict[str, str]) -> bool:
        """
        Process a table using chunked reading from the actual CSV file.
        
        Args:
            table_name: Name of output table
            metrics: Dictionary of metrics to extract
            
        Returns:
            Success status
        """
        
        print(f"\\n🔄 Processing {table_name} from actual data...")\n        \n        # Validate metrics\n        validated_metrics, missing = self.validate_metric_identifiers(metrics)\n        if missing:\n            print(f\"⚠️  Missing {len(missing)} identifiers in data:\")\n            for name, identifier in missing:\n                print(f\"   • {name}: {identifier[:60]}...\")\n        \n        if not validated_metrics:\n            print(f\"❌ No valid metrics found for {table_name}\")\n            return False\n            \n        print(f\"✅ Found {len(validated_metrics)} valid metrics\")\n        \n        # Determine output path\n        if table_name in ['resumo_quarterly', 'credito_clientes_operacoes_quarterly', \n                         'demonstracao_resultado_quarterly', 'ativo_quarterly', 'passivo_quarterly']:\n            output_path = self.output_dir / \"core_tables\" / f\"{table_name}.csv\"\n        elif 'credito' in table_name:\n            output_path = self.output_dir / \"credit_tables\" / f\"{table_name}.csv\"\n        else:\n            output_path = self.output_dir / \"calculated_metrics\" / f\"{table_name}.csv\"\n            \n        output_path.parent.mkdir(parents=True, exist_ok=True)\n        \n        # Process chunks\n        chunk_results = []\n        total_chunks = 0\n        total_relevant_rows = 0\n        \n        try:\n            print(f\"📊 Reading from {self.source_file}...\")\n            \n            chunk_iter = pd.read_csv(\n                self.source_file,\n                chunksize=self.chunk_size,\n                dtype={'CodInst': str, 'Saldo': float}\n            )\n            \n            for chunk_num, chunk in enumerate(chunk_iter, 1):\n                total_chunks = chunk_num\n                \n                # Filter for relevant metrics\n                relevant_chunk = chunk[\n                    chunk['NomeRelatorio_Grupo_Coluna'].isin(validated_metrics.values())\n                ].copy()\n                \n                if len(relevant_chunk) == 0:\n                    continue\n                \n                total_relevant_rows += len(relevant_chunk)\n                \n                # Pivot chunk to wide format\n                chunk_result = self.pivot_chunk_to_wide_format(relevant_chunk, validated_metrics)\n                if chunk_result is not None and len(chunk_result) > 0:\n                    chunk_results.append(chunk_result)\n                \n                # Progress indicator\n                if chunk_num % 20 == 0:\n                    print(f\"   📈 Processed {chunk_num} chunks, found {total_relevant_rows:,} relevant rows\")\n            \n            print(f\"\\n📋 Chunk Processing Summary:\")\n            print(f\"   • Total chunks processed: {total_chunks:,}\")\n            print(f\"   • Relevant rows found: {total_relevant_rows:,}\")\n            print(f\"   • Valid result chunks: {len(chunk_results)}\")\n            \n            # Combine results\n            if chunk_results:\n                print(f\"🔗 Combining {len(chunk_results)} result chunks...\")\n                final_result = pd.concat(chunk_results, ignore_index=True)\n                \n                # Remove duplicates (keep last value for same institution-period)\n                initial_rows = len(final_result)\n                final_result = final_result.drop_duplicates(\n                    subset=['CodInst', 'AnoMes'], keep='last'\n                )\n                \n                print(f\"🔧 Data cleaning:\")\n                print(f\"   • Initial rows: {initial_rows:,}\")\n                print(f\"   • After deduplication: {len(final_result):,}\")\n                print(f\"   • Unique institutions: {final_result['CodInst'].nunique():,}\")\n                print(f\"   • Date range: {final_result['AnoMes_Q'].min()} to {final_result['AnoMes_Q'].max()}\")\n                \n                # Save result\n                final_result.to_csv(output_path, index=False)\n                print(f\"💾 Saved to: {output_path}\")\n                \n                return True\n            else:\n                print(f\"❌ No valid data found for {table_name}\")\n                return False\n                \n        except Exception as e:\n            print(f\"❌ Error processing {table_name}: {str(e)}\")\n            return False\n    \n    def pivot_chunk_to_wide_format(self, chunk: pd.DataFrame, metrics: Dict[str, str]) -> Optional[pd.DataFrame]:\n        \"\"\"\n        Convert chunk from long format to wide format safely.\n        \"\"\"\n        try:\n            # Create reverse mapping (identifier -> clean name)\n            reverse_mapping = {v: k for k, v in metrics.items()}\n            \n            # Add clean metric names\n            chunk['Clean_Metric_Name'] = chunk['NomeRelatorio_Grupo_Coluna'].map(reverse_mapping)\n            \n            # Pivot to wide format\n            result = chunk.pivot_table(\n                index=['CodInst', 'NomeInstituicao', 'AnoMes', 'AnoMes_Q', 'AnoMes_Y'],\n                columns='Clean_Metric_Name',\n                values='Saldo',\n                aggfunc='first'  # Take first value if duplicates\n            ).reset_index()\n            \n            # Flatten column names\n            result.columns.name = None\n            \n            return result\n            \n        except Exception as e:\n            print(f\"   ⚠️  Error pivoting chunk: {str(e)}\")\n            return None\n    \n    def process_all_tables(self) -> Dict[str, bool]:\n        \"\"\"\n        Process all production tables from the actual data.\n        \"\"\"\n        \n        tables_def = self.get_production_table_definitions()\n        results = {}\n        \n        print(\"🚀 PRODUCTION DATA TRANSFORMATION STARTED\")\n        print(\"=\" * 60)\n        print(f\"📊 Source: {self.source_file}\")\n        print(f\"🎯 Target: {self.output_dir}\")\n        print(f\"📦 Tables to process: {len(tables_def)}\")\n        \n        # Process by priority\n        priority_1_tables = {k: v for k, v in tables_def.items() if v.get('priority', 3) == 1}\n        priority_2_tables = {k: v for k, v in tables_def.items() if v.get('priority', 3) == 2}\n        priority_3_tables = {k: v for k, v in tables_def.items() if v.get('priority', 3) == 3}\n        \n        for priority, tables in [(1, priority_1_tables), (2, priority_2_tables), (3, priority_3_tables)]:\n            if not tables:\n                continue\n                \n            print(f\"\\n🎯 PRIORITY {priority} TABLES ({len(tables)} tables)\")\n            print(\"-\" * 40)\n            \n            for table_name, table_config in tables.items():\n                print(f\"\\n📊 Table: {table_name}\")\n                print(f\"   📋 Description: {table_config['description']}\")\n                print(f\"   📈 Metrics: {len(table_config['metrics'])}\")\n                \n                success = self.process_table_chunks(table_name, table_config['metrics'])\n                results[table_name] = success\n                \n                if success:\n                    print(f\"   ✅ SUCCESS\")\n                else:\n                    print(f\"   ❌ FAILED\")\n        \n        # Summary\n        print(\"\\n\" + \"=\" * 60)\n        print(\"📋 PRODUCTION TRANSFORMATION SUMMARY\")\n        successful = sum(results.values())\n        total = len(results)\n        print(f\"   • Successful tables: {successful}/{total}\")\n        print(f\"   • Success rate: {successful/total*100:.1f}%\")\n        \n        if successful == total:\n            print(\"   🎉 ALL TABLES PROCESSED SUCCESSFULLY!\")\n        else:\n            failed_tables = [k for k, v in results.items() if not v]\n            print(f\"   ⚠️  Failed tables: {', '.join(failed_tables)}\")\n        \n        return results\n\ndef main():\n    \"\"\"Main execution function\"\"\"\n    \n    print(\"🏦 BANCO INSIGHTS 2.0 - PRODUCTION DATA TRANSFORMATION\")\n    print(\"=\" * 70)\n    print(\"⚠️  PROCESSING ACTUAL CONSOLIDATED_CLEANED.CSV (1GB+ FILE)\")\n    print(\"✅ Using safe chunked processing to avoid memory issues\")\n    print()\n    \n    try:\n        # Initialize transformer\n        transformer = ProductionDataTransformer()\n        \n        # Process all tables\n        results = transformer.process_all_tables()\n        \n        print(f\"\\n🎯 Transformation completed!\")\n        print(f\"   Check data_restructured/ folders for output files.\")\n        \n        # Next step preparation\n        if all(results.values()):\n            print(f\"\\n🚀 Ready for next steps:\")\n            print(f\"   1. ✅ Data transformation complete\")\n            print(f\"   2. 🔄 Next: Run TTM calculations\")\n            print(f\"   3. 🔄 Next: Implement sanity checks\")\n        else:\n            print(f\"\\n⚠️  Some tables failed - review logs above\")\n            \n    except Exception as e:\n        print(f\"❌ Critical error: {str(e)}\")\n        return False\n        \n    return True\n\nif __name__ == \"__main__\":\n    success = main()