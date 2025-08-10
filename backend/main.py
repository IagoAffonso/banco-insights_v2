from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional
import os
import json
import logging
import sys
from pathlib import Path

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the v1 project to Python path
current_dir = Path(__file__).parent
v1_project_path = current_dir.parent / "bacen_project_v1"
sys.path.append(str(v1_project_path))

# Import after path is added
try:
    from scripts.plotting import plot_market_share
    plotting_available = True
    logger.info("Successfully imported plotting functions")
except ImportError as e:
    logger.warning(f"Could not import plotting functions: {e}")
    plotting_available = False

# Initialize FastAPI app
app = FastAPI(
    title="Banco Insights 2.0 API",
    description="Brazilian banking sector intelligence platform API",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js development servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store dataframes
df_market_metrics = None
credit_data_df = None
df_fmp = None
financial_metrics_df = None

def load_data():
    """Load data from the v1 project data directory"""
    global df_market_metrics, credit_data_df, df_fmp, financial_metrics_df
    
    try:
        # Use the same path resolution as for importing
        current_dir = Path(__file__).parent
        data_dir = current_dir.parent / "bacen_project_v1" / "data"
        
        # Load main dataframes
        df_market_metrics = pd.read_csv(data_dir / "market_metrics.csv")
        credit_data_df = pd.read_csv(data_dir / "credit_data.csv")
        df_fmp = pd.read_csv(data_dir / "financial_metrics_processed.csv")
        financial_metrics_df = pd.read_csv(data_dir / "financial_metrics.csv")
        
        logger.info(f"All dataframes loaded successfully from {data_dir}")
        logger.info(f"Market metrics shape: {df_market_metrics.shape}")
        
    except Exception as e:
        error_msg = f"Failed to load dataframes: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

# Load data on startup (using modern lifespan approach would be better, but this works)
@app.on_event("startup") 
async def startup_event():
    load_data()

@app.get("/")
def root():
    return {
        "message": "Welcome to Banco Insights 2.0 API",
        "status": "ok",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/market-share")
def get_market_share_plot(
    feature: str = Query(
        default='Quantidade de clientes com operações ativas',
        description="Financial metric to analyze"
    ),
    top_n: int = Query(
        default=10,
        description="Number of top institutions to display separately",
        ge=1,
        le=50
    ),
    initial_year: Optional[int] = Query(
        default=None,
        description="Starting year for analysis",
        ge=2013,
        le=2024
    ),
    drop_nubank: int = Query(
        default=0,
        description="Nubank handling: 0=keep both, 1=drop NU PAGAMENTOS, 2=drop NUBANK",
        ge=0,
        le=2
    ),
    custom_selected_institutions: Optional[List[str]] = Query(
        default=None,
        description="List of specific institutions to always include"
    )
):
    """
    Generate interactive market share visualization with customizable parameters.
    
    This endpoint creates a stacked area chart showing the evolution of market share
    over time for financial institutions based on the selected metric.
    """
    try:
        # Validate that data is loaded
        if df_market_metrics is None:
            raise HTTPException(status_code=500, detail="Market data not loaded")
            
        # Check if plotting function is available
        if not plotting_available:
            raise HTTPException(status_code=500, detail="Plotting functions not available")
        
        # Ensure custom_selected_institutions is None or a list
        if custom_selected_institutions == []:
            custom_selected_institutions = None

        # Call the plotting function from v1
        fig = plot_market_share(
            df=df_market_metrics,
            feature=feature,
            top_n=top_n,
            initial_year=initial_year,
            drop_nubank=drop_nubank,
            custom_selected_institutions=custom_selected_institutions
        )

        # Convert to JSON for frontend consumption
        fig_json = fig.to_json()
        
        return {
            "success": True,
            "figure_json": fig_json,
            "parameters": {
                "feature": feature,
                "top_n": top_n,
                "initial_year": initial_year,
                "drop_nubank": drop_nubank,
                "custom_selected_institutions": custom_selected_institutions
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating market share plot: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics")
def get_available_metrics():
    """Get list of available financial metrics for analysis"""
    try:
        available_metrics = [
            'Quantidade de clientes com operações ativas',
            'Carteira de Crédito Pessoa Física',
            'Carteira de Crédito Pessoa Jurídica',
            'Carteira de Crédito Classificada',
            'Receitas de Intermediação Financeira',
            'Rendas de Prestação de Serviços',
            'Captações',
            'Lucro Líquido',
            'Passivo Captacoes: Depósitos Total',
            'Passivo Captacoes: Emissão de Títulos (LCI,LCA,LCF...)',
            'Receita com Operações de Crédito',
            'Receita com Operações de Títulos e Valores Mobiliários',
            'Receita com Operações de Câmbio'
        ]
        
        return {
            "success": True,
            "metrics": available_metrics,
            "count": len(available_metrics)
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/institutions")
def get_institutions():
    """Get list of all available institutions"""
    try:
        if df_market_metrics is None:
            raise HTTPException(status_code=500, detail="Market data not loaded")
        
        institutions = sorted(df_market_metrics['NomeInstituicao'].unique().tolist())
        
        return {
            "success": True,
            "institutions": institutions,
            "count": len(institutions)
        }
        
    except Exception as e:
        logger.error(f"Error getting institutions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)