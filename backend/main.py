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
allowed_origins_env = os.getenv("CORS_ORIGINS")
default_allowed = ["http://localhost:3000", "http://localhost:3001"]
allowed_origins = (
    [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
    if allowed_origins_env
    else default_allowed
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Next.js development servers or env-provided
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store dataframes
df_market_metrics = None
credit_data_df = None
df_fmp = None
financial_metrics_df = None
institutions_index = None

def load_data():
    """Load data from the v1 project data directory"""
    global df_market_metrics, credit_data_df, df_fmp, financial_metrics_df, institutions_index

    try:
        # Use the same path resolution as for importing
        current_dir = Path(__file__).parent
        data_dir = current_dir.parent / "bacen_project_v1" / "data"

        # Load main dataframes
        df_market_metrics = pd.read_csv(data_dir / "market_metrics.csv")
        credit_data_df = pd.read_csv(data_dir / "credit_data.csv")
        df_fmp = pd.read_csv(data_dir / "financial_metrics_processed.csv")
        financial_metrics_df = pd.read_csv(data_dir / "financial_metrics.csv")
        # Optional: lightweight institutions roster if present (name, cnpj, type, region)
        inst_json = data_dir / "consolidated_institutions.json"
        if inst_json.exists():
            try:
                institutions_index = pd.read_json(inst_json)
                logger.info(f"Institutions index loaded: {institutions_index.shape}")
            except Exception as e:
                logger.warning(f"Failed to load institutions index: {e}\nProceeding without it.")

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

@app.get("/api/metrics/map")
def get_metrics_map():
    """Return mapping of display metric names to raw column identifiers."""
    try:
        items = [{"display": k, "raw": v} for k, v in FEATURE_NAME_DICT.items()]
        return {"success": True, "count": len(items), "items": items}
    except Exception as e:
        logger.error(f"Error getting metrics map: {e}")
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

# -------------------------
# Helpers for aggregations
# -------------------------

# Mapping copied from v1 plotting for consistent feature names
FEATURE_NAME_DICT = {
    'Quantidade de clientes com operações ativas':'Carteira de crédito ativa - quantidade de clientes e de operações_nagroup_Quantidade de clientes com operações ativas',
    'Carteira de Crédito Pessoa Física':'Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento_nagroup_Total da Carteira de Pessoa Física',
    'Carteira de Crédito Pessoa Jurídica':'Carteira de crédito ativa Pessoa Jurídica - por porte do tomador_nagroup_Total da Carteira de Pessoa Jurídica',
    'Carteira de Crédito Classificada':'Resumo_nagroup_Carteira de Crédito Classificada',
    'Receitas de Intermediação Financeira':'Demonstração de Resultado_Resultado de Intermediação Financeira - Receitas de Intermediação Financeira_Receitas de Intermediação Financeira \n(a) = (a1) + (a2) + (a3) + (a4) + (a5) + (a6)',
    'Rendas de Prestação de Serviços':'Demonstração de Resultado_Outras Receitas/Despesas Operacionais_Rendas de Prestação de Serviços \n(d1)',
    'Captações':'Resumo_nagroup_Captações',
    'Lucro Líquido':'Resumo_nagroup_Lucro Líquido',
    'Passivo Captacoes: Depósitos Total':'Passivo_Captações - Depósito Total_Depósito Total \n(a)',
    'Passivo Captacoes: Emissão de Títulos (LCI,LCA,LCF...)':'Passivo_Captações - Recursos de Aceites e Emissão de Títulos_Recursos de Aceites e Emissão de Títulos \n(c)',
    'Receita com Operações de Crédito':'Demonstração de Resultado_Resultado de Intermediação Financeira - Receitas de Intermediação Financeira_Rendas de Operações de Crédito \n(a1)',
    'Receita com Operações de Títulos e Valores Mobiliários':'Demonstração de Resultado_Resultado de Intermediação Financeira - Receitas de Intermediação Financeira_Rendas de Operações com TVM \n(a3)',
    'Receita com Operações de Câmbio':'Demonstração de Resultado_Resultado de Intermediação Financeira - Receitas de Intermediação Financeira_Resultado de Operações de Câmbio \n(a5)',
    # Assets (from EDA: Ativo_nagroup_Ativo Total (k) = (i) - (j))
    'Ativo Total':'Ativo_nagroup_Ativo Total \n(k) = (i) - (j)'
}

# Credit modality mapping (subset reused from v1 plotting)
CREDIT_MODALITY_MAP = {
    # PF totals and modalities
    'Total PF': 'Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento_nagroup_Total da Carteira de Pessoa Física',
    'Habitação PF': 'Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento_Habitação_Total',
    'Rural PF': 'Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento_Rural e Agroindustrial_Total',
    # PJ totals and modalities
    'Total PJ': 'Carteira de crédito ativa Pessoa Jurídica - por porte do tomador_nagroup_Total da Carteira de Pessoa Jurídica',
    'Rural PJ': 'Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento_Rural e Agroindustrial_Total',
}

def _latest_quarter(values: pd.Series) -> str:
    # Assumes AnoMes_Q string sortable; fallback to AnoMes date
    try:
        return values.dropna().astype(str).sort_values().iloc[-1]
    except Exception:
        return str(values.dropna().iloc[-1])

def _df_for_feature(feature_display: str) -> pd.DataFrame:
    if df_market_metrics is None:
        raise HTTPException(status_code=500, detail="Market data not loaded")
    if feature_display not in FEATURE_NAME_DICT:
        raise HTTPException(status_code=400, detail=f"Unknown feature: {feature_display}")
    raw_col = FEATURE_NAME_DICT[feature_display]
    df = df_market_metrics[df_market_metrics['NomeRelatorio_Grupo_Coluna'] == raw_col].copy()
    if 'AnoMes' in df.columns:
        try:
            df['AnoMes'] = pd.to_datetime(df['AnoMes'])
        except Exception:
            pass
    return df

def _latest_quarter_group(df: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    # Returns latest quarter label and grouped sums by institution for that quarter
    if 'AnoMes_Q' not in df.columns:
        raise HTTPException(status_code=500, detail="Missing AnoMes_Q in dataset")
    latest = _latest_quarter(df['AnoMes_Q'])
    latest_df = df[df['AnoMes_Q'] == latest]
    grouped = latest_df.groupby('NomeInstituicao', as_index=False)['Saldo'].sum()
    return latest, grouped

def _shares(grouped: pd.DataFrame) -> pd.DataFrame:
    total = grouped['Saldo'].sum()
    if total == 0:
        grouped['share'] = 0.0
    else:
        grouped['share'] = grouped['Saldo'] / total * 100.0
    return grouped.sort_values('share', ascending=False).reset_index(drop=True)

# -------------------------
# New APIs (Phase 1)
# -------------------------

@app.get("/api/snapshot")
def get_snapshot(
    feature: str = Query(default='Carteira de Crédito Classificada', description="Metric for snapshot aggregates"),
):
    try:
        df = _df_for_feature(feature)
        period, grouped = _latest_quarter_group(df)
        ranked = _shares(grouped)
        top5_conc = float(ranked.head(5)['share'].sum()) if not ranked.empty else 0.0
        total_value = float(grouped['Saldo'].sum()) if not grouped.empty else 0.0
        institutions_count = int(df_market_metrics['NomeInstituicao'].nunique())
        return {
            "success": True,
            "period": period,
            "totalValue": total_value,
            "institutionsCount": institutions_count,
            "marketConcentrationTop5": top5_conc,
            # Placeholders for future expansion when mapped from financial_metrics_df
            "roeAvg": None,
            "baselAvg": None,
            "metric": feature
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in snapshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market-concentration")
def get_market_concentration(
    feature: str = Query(default='Carteira de Crédito Classificada'),
    top_n: int = Query(default=10, ge=1, le=50),
):
    try:
        df = _df_for_feature(feature)
        period, grouped = _latest_quarter_group(df)
        ranked = _shares(grouped)
        items = []
        for i, row in ranked.head(top_n).iterrows():
            items.append({
                "rank": i + 1,
                "name": row['NomeInstituicao'],
                "marketShare": float(row['share']),
                "value": float(row['Saldo'])
            })
        concentration = float(ranked.head(top_n)['share'].sum()) if not ranked.empty else 0.0
        return {
            "success": True,
            "period": period,
            "feature": feature,
            "top": items,
            "concentration": concentration
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in market concentration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rankings")
def get_rankings(
    feature: str = Query(default='Carteira de Crédito Classificada', description="Metric to rank by"),
    period: Optional[str] = Query(default=None, description="Quarter label e.g. 2019Q1; default latest"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    try:
        df = _df_for_feature(feature)
        if period is None:
            period, grouped = _latest_quarter_group(df)
        else:
            grouped = df[df['AnoMes_Q'] == period].groupby('NomeInstituicao', as_index=False)['Saldo'].sum()
        ranked = grouped.sort_values('Saldo', ascending=False).reset_index(drop=True)
        total = int(ranked.shape[0])
        page = ranked.iloc[offset:offset+limit]
        # Compute shares for page (relative to full market)
        total_market = ranked['Saldo'].sum()
        items = []
        for i, row in page.iterrows():
            share = (float(row['Saldo'])/total_market*100.0) if total_market else 0.0
            items.append({
                "rank": int(i + 1),
                "institution_id": None,
                "name": row['NomeInstituicao'],
                "value": float(row['Saldo']),
                "changePct": None,
                "trend": None,
                "marketShare": share
            })
        return {
            "success": True,
            "period": period,
            "total": total,
            "limit": limit,
            "offset": offset,
            "feature": feature,
            "items": items
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in rankings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/institutions/search")
def search_institutions(
    query: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    feature: str = Query(default='Carteira de Crédito Classificada', description="Metric to attach latest values")
):
    try:
        names = df_market_metrics['NomeInstituicao'].dropna().unique().tolist()
        if query:
            q = query.lower().strip()
            names = [n for n in names if q in n.lower()]
        names.sort()
        total = len(names)
        start = (page-1)*page_size
        end = start + page_size
        page_names = names[start:end]

        # attach latest values for requested metric
        df = _df_for_feature(feature)
        period, grouped = _latest_quarter_group(df)
        latest_map = {r['NomeInstituicao']: float(r['Saldo']) for _, r in grouped.iterrows()}

        items = []
        for n in page_names:
            item = {
                "id": None,
                "name": n,
                "cnpj": None,
                "type": None,
                "region": None,
                "latest": {"value": latest_map.get(n), "period": period, "feature": feature}
            }
            # If we have institutions_index, attempt to enrich
            try:
                if institutions_index is not None and not institutions_index.empty:
                    match = institutions_index[institutions_index['name'].str.lower() == n.lower()]
                    if not match.empty:
                        row = match.iloc[0]
                        item.update({
                            "id": row.get('id'),
                            "cnpj": row.get('cnpj'),
                            "type": row.get('type'),
                            "region": row.get('region')
                        })
            except Exception:
                pass
            items.append(item)

        return {
            "success": True,
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in institutions search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/credit/segments")
def get_credit_segments(
    period: Optional[str] = Query(default=None, description="Quarter label e.g. 2024Q4; default latest"),
    scope: str = Query(default='market', description="market or institution"),
    institution: Optional[str] = Query(default=None),
):
    """Return credit segments breakdown (PF, PJ, Habitacional, Rural) with share and YoY growth."""
    try:
        if credit_data_df is None:
            raise HTTPException(status_code=500, detail="Credit data not loaded")
        df = credit_data_df.copy()
        # Prep date types
        try:
            df['AnoMes'] = pd.to_datetime(df['AnoMes'])
        except Exception:
            pass

        if scope == 'institution':
            if not institution:
                raise HTTPException(status_code=400, detail="institution is required when scope=institution")
            df = df[df['NomeInstituicao'] == institution]

        # Determine period
        period_latest = _latest_quarter(df['AnoMes_Q'])
        target_period = period or period_latest

        # Helper to aggregate a modality key
        def agg_for_key(mod_key: str, per: str) -> float:
            sub = df[(df['NomeRelatorio_Grupo_Coluna'] == mod_key) & (df['AnoMes_Q'] == per)]
            return float(sub['Saldo'].sum()) if not sub.empty else 0.0

        # Compute segment values
        total_pf = agg_for_key(CREDIT_MODALITY_MAP['Total PF'], target_period)
        total_pj = agg_for_key(CREDIT_MODALITY_MAP['Total PJ'], target_period)
        habit_pf = agg_for_key(CREDIT_MODALITY_MAP['Habitação PF'], target_period)
        rural_pf = agg_for_key(CREDIT_MODALITY_MAP['Rural PF'], target_period)
        rural_pj = agg_for_key(CREDIT_MODALITY_MAP['Rural PJ'], target_period)
        rural_total = rural_pf + rural_pj
        total_market = total_pf + total_pj

        def share(v: float, t: float) -> float:
            return (v / t * 100.0) if t else 0.0

        # YoY growth vs same quarter previous year
        def prev_year(q: str) -> str:
            # Assumes format YYYYQn
            try:
                y = int(q[:4]) - 1
                return f"{y}{q[4:]}"
            except Exception:
                return q

        prev = prev_year(target_period)
        total_pf_prev = agg_for_key(CREDIT_MODALITY_MAP['Total PF'], prev)
        total_pj_prev = agg_for_key(CREDIT_MODALITY_MAP['Total PJ'], prev)
        habit_pf_prev = agg_for_key(CREDIT_MODALITY_MAP['Habitação PF'], prev)
        rural_total_prev = agg_for_key(CREDIT_MODALITY_MAP['Rural PF'], prev) + agg_for_key(CREDIT_MODALITY_MAP['Rural PJ'], prev)

        def growth(curr: float, prev: float) -> float:
            if prev == 0:
                return 0.0
            return (curr - prev) / prev * 100.0

        items = [
            {"segment": "Pessoa Física", "value": total_pf, "share": share(total_pf, total_market), "growthYoY": growth(total_pf, total_pf_prev)},
            {"segment": "Pessoa Jurídica", "value": total_pj, "share": share(total_pj, total_market), "growthYoY": growth(total_pj, total_pj_prev)},
            {"segment": "Habitacional", "value": habit_pf, "share": share(habit_pf, total_market), "growthYoY": growth(habit_pf, habit_pf_prev)},
            {"segment": "Rural", "value": rural_total, "share": share(rural_total, total_market), "growthYoY": growth(rural_total, rural_total_prev)},
        ]

        return {"success": True, "period": target_period, "scope": scope, "institution": institution, "items": items}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in credit segments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/timeseries")
def get_timeseries(
    feature: str = Query(..., description="Display feature name from metrics map"),
    scope: str = Query(default='market', description="market or institution"),
    institution: Optional[str] = Query(default=None)
):
    """Return a simple timeseries for a given feature, aggregated quarterly."""
    try:
        df = _df_for_feature(feature)
        if scope == 'institution':
            if not institution:
                raise HTTPException(status_code=400, detail="institution is required when scope=institution")
            df = df[df['NomeInstituicao'] == institution]
        ts = df.groupby('AnoMes_Q', as_index=False)['Saldo'].sum().sort_values('AnoMes_Q')
        series = [{"period": r['AnoMes_Q'], "value": float(r['Saldo'])} for _, r in ts.iterrows()]
        return {"success": True, "feature": feature, "scope": scope, "institution": institution, "series": series}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in timeseries: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/financials/dre")
def get_financials_dre(
    scope: str = Query(default='market', description="market or institution"),
    institution: Optional[str] = Query(default=None),
    period: Optional[str] = Query(default=None, description="Quarter label; default latest")
):
    """Return a simplified DRE table for the requested scope and period.
    Note: This is a best-effort mapping over the consolidated financials; will be refined using EDA docs.
    """
    try:
        if financial_metrics_df is None:
            raise HTTPException(status_code=500, detail="Financial metrics not loaded")
        df = financial_metrics_df.copy()
        # Filter to DRE-related rows
        if 'NomeRelatorio' in df.columns:
            df = df[df['NomeRelatorio'].str.contains('Demonstra', na=False)]
        if scope == 'institution':
            if not institution:
                raise HTTPException(status_code=400, detail="institution is required when scope=institution")
            df = df[df['NomeInstituicao'] == institution]
        # Pick period
        per = period or _latest_quarter(df['AnoMes_Q'])
        dper = df[df['AnoMes_Q'] == per]
        # Aggregate by account name if available
        account_col = 'NomeColuna' if 'NomeColuna' in dper.columns else ('Conta' if 'Conta' in dper.columns else None)
        if account_col is None:
            raise HTTPException(status_code=500, detail="Unexpected DRE schema; cannot find account column")
        grouped = dper.groupby(account_col, as_index=False)['Saldo'].sum().sort_values('Saldo', ascending=False)
        rows = [{
            "account": r[account_col],
            "value": float(r['Saldo'])
        } for _, r in grouped.iterrows()]
        return {"success": True, "scope": scope, "institution": institution, "period": per, "rows": rows}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in DRE: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/credit/portfolio")
def get_credit_portfolio(
    scope: str = Query(default='market', description='market or institution'),
    institution: Optional[str] = Query(default=None),
    grouping: str = Query(default='pfpj', description='pfpj or modality'),
    percentage: bool = Query(default=True)
):
    """Return credit portfolio breakdown by grouping (pfpj or coarse modalities)."""
    try:
        if credit_data_df is None:
            raise HTTPException(status_code=500, detail="Credit data not loaded")
        df = credit_data_df.copy()
        if scope == 'institution':
            if not institution:
                raise HTTPException(status_code=400, detail="institution is required when scope=institution")
            df = df[df['NomeInstituicao'] == institution]
        period = _latest_quarter(df['AnoMes_Q'])

        total_pf = df[(df['NomeRelatorio_Grupo_Coluna'] == CREDIT_MODALITY_MAP['Total PF']) & (df['AnoMes_Q'] == period)]['Saldo'].sum()
        total_pj = df[(df['NomeRelatorio_Grupo_Coluna'] == CREDIT_MODALITY_MAP['Total PJ']) & (df['AnoMes_Q'] == period)]['Saldo'].sum()
        total = total_pf + total_pj

        if grouping == 'pfpj':
            data = [
                {"key": "Pessoa Física", "value": float(total_pf)},
                {"key": "Pessoa Jurídica", "value": float(total_pj)}
            ]
        else:
            # coarse modalities: Habitacional (PF), Rural (PF+PJ), Outros = remainder
            habit_pf = df[(df['NomeRelatorio_Grupo_Coluna'] == CREDIT_MODALITY_MAP['Habitação PF']) & (df['AnoMes_Q'] == period)]['Saldo'].sum()
            rural_pf = df[(df['NomeRelatorio_Grupo_Coluna'] == CREDIT_MODALITY_MAP['Rural PF']) & (df['AnoMes_Q'] == period)]['Saldo'].sum()
            rural_pj = df[(df['NomeRelatorio_Grupo_Coluna'] == CREDIT_MODALITY_MAP['Rural PJ']) & (df['AnoMes_Q'] == period)]['Saldo'].sum()
            rural_total = rural_pf + rural_pj
            others = max(total - (habit_pf + rural_total), 0)
            data = [
                {"key": "Habitacional PF", "value": float(habit_pf)},
                {"key": "Rural (PF+PJ)", "value": float(rural_total)},
                {"key": "Outros", "value": float(others)}
            ]

        if percentage and total > 0:
            for d in data:
                d['share'] = d['value'] / total * 100.0
        return {"success": True, "period": period, "grouping": grouping, "percentage": percentage, "items": data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in credit portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
