import pandas as pd
import plotly.graph_objects as go
from app import app
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.graph_objs._figure import Figure
from utils import add_rectangle_shape, get_data2, get_empty_figure

import hover_template

years = ["2016-2017", "2018-2019", "2020-2021", "2022-2023"]
years = pd.DataFrame(years)
years = years[0].unique()

empty_fig = get_empty_figure("Veuillez sélectionner les années pour lesquelles vous souhaitez visualiser l'évolution du taux d'inflation")
add_rectangle_shape(empty_fig)


def get_layout():
    return html.Main(
        className="viz-container",
        children=[
            html.Div(
                className="section-title",
                children=[
                    html.H1("Variation annuelle de l'inflation par groupe de produits entre 2016 et 2022"),
                ],
            ),
            html.Div(
                id="year-dropdowns",
                children=[
                    html.P("Visualiser pour les années :"),
                    dcc.Dropdown(
                        id="year-choosen",
                        className="year-dropdown",
                        options=[{"label": x, "value": x} for x in years],
                        value=min(years),
                    ),
                ],
            ),
            dcc.Graph(
                id="heatmap-inflation",
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

@app.callback(
    Output("heatmap-inflation", "figure"),
    [Input("year-choosen", "value")],
)
def get_heatmap(year: str):
    fig: Figure = go.Figure()

    if year is None:
        return empty_fig
    else:
        # Preprocess
        name_csv = "Inflation_" + year + ".csv"
        name_csv = str(name_csv)
        df = get_data2(name_csv)

        df = df[df["Unité"] == "Variation annuelle en %"].reset_index()
        df = df.drop(
            index=[
                2,
                3,
                5,
                6,
                7,
                8,
                9,
                11,
                12,
                13,
                14,
                17,
                18,
                19,
                20,
                22,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                33,
                36,
                37,
                38,
            ]
        )
        df = df.loc[::-1].reset_index(drop=True)

        df = df.drop(columns="index")
        df = df.drop(columns="Unité")

        # On enlève les indexes des lignes qu'on ne souhaite pas voir dans la carte de chaleur
        df = df.set_index("Produits et groupes de produits")

        fig = go.Figure(
            go.Heatmap(x=df.columns, y=df.index, z=df, zmid=0, colorscale="RdBu_r")
        )

        fig.update_layout(
            dragmode=False,
            xaxis=dict(tickmode="linear"),
            title=f"Évolution du taux d'inflation par produits et groupes de produits durant les années {year}",
            xaxis_title="Mois",
            yaxis_title="Produits",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#ffffff',
            font=dict(
                family="Arial Narrow",
                size=15,
            ),
        )
        fig.update_traces(hovertemplate=hover_template.inflation_hover_template())

    return fig
