from typing import List
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output
from plotly.graph_objs._figure import Figure
from plotly.subplots import make_subplots
from utils import add_rectangle_shape, get_data, get_empty_figure

import hover_template
from template import THEME_GRAPH

GLOBAL_SUBSET = ["Total des employés, toutes les industries"]
GOODS_SUBSET = [
    "Secteur de la production de biens",
    "Agriculture",
    "Foresterie, pêche, mines, exploitation en carrière, et extraction de pétrole et de gaz",
    "Services publics",
    "Construction",
    "Fabrication",
]
SERVICES_SUBSET = [
    "Secteur des services",
    "Commerce de gros et de détail",
    "Transport et entreposage",
    "Finance, assurances, services immobiliers et de location",
    "Services professionnels, scientifiques et techniques",
    "Services aux entreprises, services relatifs aux bâtiments et autres services de soutien",
    "Services d'enseignement",
    "Soins de santé et assistance sociale",
    "Information, culture et loisirs",
    "Services d'hébergement et de restauration",
    "Autres services (sauf les administrations publiques)",
    "Administrations publiques",
]

IGNORE_BARS = [
    "Total des employés, toutes les industries",
    "Secteur des services",
    "Secteur de la production de biens",
]

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

# LOAD + SORT
df = get_data("salaires.csv")
df = df.sort_values("Annee")

empty_fig = get_empty_figure("Veuillez survoller un point de la courbe pour afficher les données")
add_rectangle_shape(empty_fig)


def get_layout():
    # TOTAL
    fig_total = get_avg_salary_line_fig(
        df,
        GLOBAL_SUBSET,
    )
    fig_total.update_layout(
        title="Évolution du salaire moyen, toutes les industries",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
    )
    fig_total.update_xaxes(title_text="Année", dtick=1, fixedrange=True, gridcolor='#f0f0f0', gridwidth=2,)
    fig_total.update_yaxes(title_text="Salaire moyen ($)", gridcolor='#f0f0f0', gridwidth=2)

    # GOODS
    fig_goods = get_multiple_sectors_fig(df, GOODS_SUBSET, 2, 3)
    fig_goods.update_layout(
        title="Évolution du salaire moyen, secteur de la production de biens",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
    )

    fig_goods.update_xaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    fig_goods.update_yaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    # SERVICES
    fig_services = get_multiple_sectors_fig(
        df,
        SERVICES_SUBSET,
        4,
        3,
    )
    fig_services.update_layout(
        title="Évolution du salaire moyen, secteur des services",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
    )

    fig_services.update_xaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    fig_services.update_yaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )


    return html.Main(
        className="viz-container",
        children=[
            html.Div(
                className="section-title",
                children=[
                    html.H1("Évolution des salaires moyens selon les industries, du secteur de la production des biens et du secteur des services"),
                ],
            ),
            dcc.Graph(
                id="salaires-total",
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
                id="salaires-total-bar",
                className="graph",
                figure=empty_fig,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False,
                ),
            ),
            dcc.Graph(
                id="salaires-biens",
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
                id="salaires-servicess",
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

def get_sector_avg_salary_trace(df: pd.DataFrame, sector: str, color):
    sub_df = df[df["Secteur"].isin([sector])]
    return go.Scatter(
        x=sub_df["Annee"],
        y=sub_df["Salaire"],
        line_shape="spline",
        mode="lines+markers",
        name=sector,
        marker=dict(color=color),
        hovertemplate=hover_template.salaires_salairemoy_hover_template()
    )

def get_avg_salary_line_fig(df: pd.DataFrame, sectors: List[str]) -> Figure:
    fig: Figure = go.Figure()
    i = 0
    for sector in sectors:
        sector_trace = get_sector_avg_salary_trace(df, sector, colors[i])
        fig.add_trace(sector_trace)
        i += 1
    return fig

def get_multiple_sectors_fig(df: pd.DataFrame, sectors: List[str], rows: int, cols: int) -> Figure:
    fig: Figure = make_subplots(rows, cols)
    k = 0
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            sector = sectors[(i - 1) * (cols) + (j - 1)]
            sector_trace = get_sector_avg_salary_trace(df, sector, colors[k])
            fig.add_trace(sector_trace, i, j)
            k += 1
    return fig


@app.callback(
    Output("salaires-total-bar", "figure"), [Input("salaires-total", "hoverData")]
)
def get_year_bar_fig(hoverData) -> Figure:
    if hoverData is None:
        return empty_fig

    fig: Figure = go.Figure()

    year = hoverData["points"][0]["x"]
    sorted_df = df.sort_values("Salaire")
    top_3 = (
        sorted_df.loc[
            (sorted_df["Annee"] == year) & (~sorted_df["Secteur"].isin(IGNORE_BARS))
        ]
        .head(3)
        .sort_values("Salaire", ascending=False)
    )
    bottom_3 = (
        sorted_df.loc[
            (sorted_df["Annee"] == year) & (~sorted_df["Secteur"].isin(IGNORE_BARS))
        ]
        .tail(3)
        .sort_values("Salaire", ascending=False)
    )

    fig.add_trace(
        go.Bar(
            x=bottom_3["Salaire"],
            y=bottom_3["Secteur"],
            orientation="h",
            text=bottom_3["Salaire"],
            marker=dict(color=colors[0]),
        )
    )

    fig.add_trace(
        go.Bar(
            x=top_3["Salaire"],
            y=top_3["Secteur"],
            orientation="h",
            text=top_3["Salaire"],
            marker=dict(color=colors[1]),
        )
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=hover_template.salaires_bar_hover_template()
    )

    fig.update_layout(
        showlegend=False,
        title=f"Trois salaires moyens les plus élevés et les moins élevés pour l'année {year}",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
    )

    return fig
