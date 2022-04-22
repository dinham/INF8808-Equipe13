from dash import dcc
from dash import html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import get_data

import hover_template
from template import THEME_GRAPH

df_chomage = get_data("taux_chomage.csv")
df_emplois = get_data("taux_emplois.csv")

REGIONS = [
    "Bas-Saint-Laurent",
    "Saguenay-Lac-Saint-Jean",
    "Capitale-Nationale",
    "Mauricie",
    "Estrie",
    "Montréal",
    "Outaouais",
    "Abitibi-Témiscamingue",
    "Côte-Nord et Nord-du-Québec",
    "Gaspésie-Îles-de-la-Madeleine",
    "Chaudière-Appalaches",
    "Laval",
    "Lanaudière",
    "Laurentides",
    "Montérégie",
    "Centre-du-Québec"
]

EMPLOI_COLOR = 'rgb(81,191,256)'
CHOMAGE_COLOR = 'rgb(2,116,169)'

# -------------------------------------------------------------------------------

def get_layout():
    return html.Main(
        className="viz-container",
        children=[
            html.Div(
                className="section-title",
                children=[
                    html.H1("Taux de chômage et d'emplois par région administratives du Québec entre janvier 2019 et décembre 2021"),
                ],
            ),
            html.Div(get_graphs())
        ],
    )

# https://stackoverflow.com/questions/55062551/how-do-i-show-several-charts-charts-in-dash-python-using-a-for-loop
def get_graphs():
    graph_per_region = []

    for region in REGIONS:
        if region not in graph_per_region:
            graph_per_region.append(
                dcc.Graph(
                    id="taux-chomage",
                    className="graph",
                    figure=graph_chomage_emplois(region),
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False,
                    ),
                    style={'display': 'inline-block'}
                ),
        )

    return graph_per_region

def graph_chomage_emplois(region):
    region_emplois = df_emplois.loc[df_emplois['Territoire'] == region]
    region_chomage = df_chomage.loc[df_chomage['Territoire'] == region]

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    fig.add_trace(
        go.Scatter(
            x=region_emplois["Mois"],
            y=region_emplois["Valeur"],
            name="Taux d'emploi",
            marker=dict(color=THEME_GRAPH["light_blue_color"]),
            hovertemplate=hover_template.caracteristiques_hover_template("Taux d'emploi")
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=region_chomage["Mois"],
            y=region_chomage["Valeur"],
            name="Taux de chômage",
            marker=dict(color=THEME_GRAPH["dark_blue_color"]),
            hovertemplate=hover_template.caracteristiques_hover_template("Taux de chômage")
        ),
        row=2, col=1
    )

    fig.update_layout(
        height=500,
        width=450,
        title_text=region,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        )
    )
    fig.update_xaxes(
        linecolor='#b8b8b8',
        linewidth=2,
        gridcolor='#f0f0f0',
        gridwidth=2,
        tickangle=45,
        tickvals=['Janvier 2019', 'Septembre 2019', 'Juin 2020', 'Mars 2021', 'Décembre 2021'],
        ticktext=["Janv. 2019", "Sept. 2019", "Juin 2020", "Mars 2021", "Déc. 2021"]
    )
    fig.update_yaxes(
        linecolor='#b8b8b8',
        linewidth=2,
        gridcolor='#f0f0f0'
    )

    if region == "Mauricie":
        fig.update_layout(width=535, showlegend=True, legend_borderwidth=1, legend_itemclick=False)
    
    return fig
