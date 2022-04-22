from typing import List
import pandas as pd
import plotly.graph_objects as go
from app import app
from dash import dcc, html
from dash.dependencies import Input, Output, State
from plotly.graph_objs._figure import Figure
from plotly.subplots import make_subplots
from utils import get_data

import hover_template
from template import THEME_GRAPH

df = get_data("salaires.csv")
df = df.sort_values("Annee")

df_pib = get_data("PIB_short.csv")
df_pib = df_pib.sort_values("Annee")

years = df["Annee"].unique()

# -------------------------------------------------------------------------------------

def get_layout():
    return html.Main(
        className="viz-container",
        children=[
            html.Div(
                className="section-title",
                children=[
                    html.H1("Mises en parallèle entre les salaires moyens par industrie et la variation de PIB"),
                ],
            ),
            html.Div(
                id="year-dropdowns",
                children=[
                    html.P("Visualiser pour l'année"),
                    dcc.Dropdown(
                        id="year-start-dropdown",
                        className="year-dropdown",
                        options=[{"label": x, "value": x} for x in years],
                        value=min(years),
                    ),
                    html.P("à l'année"),
                    dcc.Dropdown(
                        id="year-end-dropdown",
                        className="year-dropdown",
                        options=[{"label": x, "value": x} for x in years],
                        value=max(years),
                    ),
                ],
            ),
            html.P(id="pib-variation"),
            dcc.Graph(
                id="paralleles-salaire-pib-range",
                className="graph",
                figure=go.Figure(),
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


def get_avg_salary_line_fig(df: pd.DataFrame, sectors: List[str]) -> Figure:
    fig: Figure = go.Figure()
    for sector in sectors:
        sector_trace = get_sector_avg_salary_trace(df, sector)
        fig.add_trace(sector_trace)
    return fig


def get_sector_avg_salary_trace(df: pd.DataFrame, sector: str):
    sub_df = df[df["Secteur"].isin([sector])]
    return go.Scatter(
        x=sub_df["Annee"],
        y=sub_df["Salaire"],
        line_shape="spline",
        mode="lines+markers",
        name=sector
    )


def get_multiple_sectors_fig(
    df: pd.DataFrame, sectors: List[str], rows: int, cols: int
) -> Figure:
    fig: Figure = make_subplots(rows, cols)

    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            sector = sectors[(i - 1) * (cols) + (j - 1)]
            sector_trace = get_sector_avg_salary_trace(df, sector)
            fig.add_trace(sector_trace, i, j)

    return fig


@app.callback(
    Output("paralleles-salaire-pib-range", "figure"),
    [Input("year-start-dropdown", "value"), Input("year-end-dropdown", "value")],
)
def get_range_fig(start: int, end: int):
    filtered_df = df.loc[(df["Annee"] == start) | (df["Annee"] == end)]
    fig: Figure = go.Figure()

    for _, sector in filtered_df.groupby("Secteur"):
        fig.add_trace(
            go.Scatter(
                x=sector["Salaire"],
                y=sector["Secteur"],
                line=dict(color="#C0C0C0"),
                orientation="h"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=sector.loc[sector["Annee"] == start]["Salaire"],
                y=sector["Secteur"],
                marker=dict(color=THEME_GRAPH['dark_blue_color']),
                mode="markers"
            )
        )

        start_salary = sector.loc[sector["Annee"] == start]["Salaire"]
        end_salary = sector.loc[sector["Annee"] == end]["Salaire"]

        diff = float(end_salary) - float(start_salary)

        diff_percent = diff / abs(float(start_salary)) * 100

        if diff >= 0:
            txt_format = "+{:.2f}%"
            txt_color = THEME_GRAPH['dark_blue_color']
            symbol_color = THEME_GRAPH['light_blue_color']
            align = "middle right"
            symbol = "triangle-right"
        else:
            txt_format = "{:.2f}%"
            txt_color = "red"
            symbol_color = "red"
            align = "middle left"
            symbol = "triangle-left"

        fig.add_trace(
            go.Scatter(
                x=end_salary,
                y=sector["Secteur"],
                marker_symbol=symbol,
                marker=dict(
                    color=symbol_color,
                    size=8,
                    line=dict(width=2, color=THEME_GRAPH['light_blue_color']),
                ),
                mode="markers+text",
                text=txt_format.format(diff_percent),
                textposition=align,
                textfont=dict(color=txt_color),
                hovertemplate=hover_template.paralleles_hover_template()
            )
        )

    fig.update_layout(
        showlegend=False,
        title=f"Évolution du salaire moyen par industrie de l'année {start} à l'année {end}",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        )
    )
    fig.update_xaxes(
        title_text="Salaire moyen ($)",
        dtick=2,
        fixedrange=True,
        gridcolor='#f0f0f0',
        gridwidth=2,
    )
    fig.update_yaxes(dtick=1,gridcolor='#f0f0f0',gridwidth=2)

    return fig


@app.callback(
    Output("pib-variation", "children"),
    [Input("year-start-dropdown", "value"), Input("year-end-dropdown", "value")],
)
def get_pib_variation(start: int, end: int):
    start_pib = df_pib.loc[df_pib["Annee"] == start]["PIB"]
    end_pib = df_pib.loc[df_pib["Annee"] == end]["PIB"]

    diff = float(end_pib) - float(start_pib)
    diff_percent = diff / abs(float(start_pib)) * 100

    diff_prefix = "+" if diff_percent > 0 else ""

    f_pib = (
        f"Différence de PIB entre {start} et {end}: {diff_prefix}{diff_percent:.2f}%"
    )

    return f_pib
