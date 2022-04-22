from typing import List
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from plotly.graph_objs._figure import Figure
from plotly.subplots import make_subplots
from utils import get_data2

import hover_template
from template import THEME_GRAPH

GLOBAL_SUBSET = [
    "Total (Ensemble des industries)",
    "Secteur producteur de biens",
    "Secteur producteur de services",
]
GOODS_SUBSET = [
    "Agriculture, foresterie, pêche et chasse",
    "Extraction minière, exploitation en carrière, et extraction de pétrole et de gaz",
    "Services publics",
    "Production, transport et distribution d'électricité",
    "Construction",
    "Fabrication",
]
SERVICES_SUBSET = [
    "Commerce de gros",
    "Commerce de détail",
    "Transport et entreposage",
    "Industrie de l'information et industrie culturelle",
    "Finance et assurances",
    "Services immobiliers et services de location et de location à bail",
    "Services professionnels, scientifiques et techniques",
    "Gestion de sociétés et d'entreprises",
    "Services administratifs, services de soutien, services de gestion des déchets et services d'assainissement",
    "Services d'enseignement",
    "Soins de santé et assistance sociale",
    "Arts, spectacles et loisirs",
    "Hébergement et services de restauration",
    "Administrations publiques",
    "Autres services",
]

df = get_data2("PIB.csv")
colors = [
    THEME_GRAPH["light_blue_color"],
    THEME_GRAPH["dark_blue_color"],
    THEME_GRAPH["light_grey_color"],
    THEME_GRAPH["turquoise_color"],
    THEME_GRAPH["green_color"],
    THEME_GRAPH["dark_green_color"],
    THEME_GRAPH["apple_green_color"],
    THEME_GRAPH["red_color"],
    THEME_GRAPH["dark_red_color"],
    THEME_GRAPH["orange_color"],
    THEME_GRAPH["dark_orange_color"],
    THEME_GRAPH["yellow_color"],
    THEME_GRAPH["dark_yellow_color"],
    THEME_GRAPH["dark_grey_color"],
    THEME_GRAPH["medium_grey_color"]
]

# -------------------------------------------------------------------------------------

def get_layout():
    # TOTAL
    fig_total = get_evolPIB_fig(
        df,
        GLOBAL_SUBSET,
    )
    fig_total.update_layout(
        title="Évolution du produit intérieur brut global de 2017 à 2021",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        )
    )

    fig_total.update_xaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    fig_total.update_yaxes(
        title_text="PIB réel aux prix de base, désaisonnalisé en M$ enchaînés",
        gridcolor='#f0f0f0',gridwidth=2
    )

    # GOODS
    fig_goods = get_multiple_sectors_fig(df, GOODS_SUBSET, 2, 3)
    fig_goods.update_layout(
        title="Évolution du PIB, industries du secteur producteur de biens",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        )
    )

    fig_goods.update_xaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )
    fig_goods.update_yaxes(gridcolor='#f0f0f0',gridwidth=2)

    # SERVICES
    fig_services = get_multiple_sectors_fig(
        df,
        SERVICES_SUBSET,
        3,
        5,
    )
    fig_services.update_layout(
        title="Évolution du PIB, industries du secteur producteur de services",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        )
    )

    fig_services.update_xaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )
    fig_services.update_yaxes(gridcolor='#f0f0f0',gridwidth=2)


    return html.Main(
        className="viz-container",
        children=[
            html.Div(
                className="section-title",
                children=[
                    html.H1("Évolution du PIB global, du secteur de production de biens et du secteur de producteur de services"),
                ],
            ),

            dcc.Graph(
                id="pib-total",
                className="graph",
                figure=fig_total,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False,
                ),
            ),
            dcc.Graph(
                id="pib-biens",
                className="graph",
                figure=fig_goods,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False,
                ),
            ),
            dcc.Graph(
                id="pib-servicess",
                className="graph",
                figure=fig_services,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False,
                ),
            ),
        ],
    )

def get_evolPIB_trace(df: pd.DataFrame, sector: str, color):
    sub_df = df[df["1er niveau de détail"].isin([sector])]
    return go.Scatter(
        x=sub_df["Temps"],
        y=sub_df["Valeur numérique"],
        mode="lines",
        name=sector,
        marker=dict(color=color),
    )

def get_evolPIB_fig(df: pd.DataFrame, sectors: List[str]) -> Figure:
    fig: Figure = go.Figure()
    i = 0
    for sector in sectors:
        sector_trace = get_evolPIB_trace(df, sector, colors[i])
        fig.add_trace(sector_trace)
        i += 1

    fig.update_traces(
        hovertemplate=hover_template.pib_hover_template()
    )
    return fig

def get_multiple_sectors_fig(df: pd.DataFrame, sectors: List[str], rows: int, cols: int) -> Figure:
    fig: Figure = make_subplots(
        rows, cols, shared_xaxes="columns", horizontal_spacing=0.05
    )
    k = 0
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            sector = sectors[(i - 1) * (cols) + (j - 1)]
            sector_trace = get_evolPIB_trace(df, sector, colors[k])
            fig.add_trace(sector_trace, i, j)
            k += 1
    
    fig.update_traces(
        hovertemplate=hover_template.pib_hover_template()
    )

    return fig
