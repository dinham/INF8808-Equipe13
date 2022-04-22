import pandas as pd  # (version 0.24.2)
import plotly.express as px
import plotly.graph_objects as go
from app import app
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import get_data_3

import hover_template
from template import THEME_GRAPH

df = get_data_3("revenu_menage.csv")

# -------------------------------------------------------------------------------------

TRIMESTERS = [
    "1er trim. 2019",
    "2e trim. 2019",
    "3e trim. 2019",
    "4e trim. 2019",
    "1er trim. 2020",
    "2e trim. 2020",
    "3e trim. 2020",
    "4e trim. 2020",
    "1er trim. 2021",
    "2e trim. 2021",
    "3e trim. 2021",
    "4e trim. 2021"
]

menage_clean = df.drop(['Élément statistique', 'Unité de mesure'], axis=1)

revenu_disponible = menage_clean[menage_clean['1er niveau de détail'].isin([
    'Rémunération des salariés',
    'Plus : revenu mixte net',
    'Revenu de la propriété reçu',
    'Moins : revenu de la propriété payé',
    'Égale : Revenu disponible des ménages',
    'Plus : transferts courants reçus',
    'Moins : transferts courants payés',
    "Taux d'épargne des ménages en pourcentage du revenu disponible des ménages"
])]

def essai_transfo(row):
    if row["1er niveau de détail"] == "Rémunération des salariés":
        return "Plus"
    elif row["1er niveau de détail"] == "Plus : revenu mixte net":
        return "Plus"
    elif row["1er niveau de détail"] == "Revenu de la propriété reçu":
        return "Plus"
    elif row["1er niveau de détail"] == "Moins : revenu de la propriété payé":
        return "Moins"
    elif (row['1er niveau de détail'] == 'Plus : transferts courants reçus'):
        return 'Plus'
    elif (row['1er niveau de détail'] == 'Moins : transferts courants payés'):
        return 'Moins'
    elif (row['1er niveau de détail'] == 'Égale : Revenu disponible des ménages'):
        return 'Égale'
    elif (row['1er niveau de détail'] == "Taux d'épargne des ménages en pourcentage du revenu disponible des ménages"):
        return "Taux d'epargne"

revenu_disponible["Impact"] = revenu_disponible.apply(
    lambda row: essai_transfo(row), axis=1
)

data = revenu_disponible.groupby(["Temps", "Impact", "1er niveau de détail"]).sum()

# -------------------------------------------------------------------------------------

def get_layout():
    return html.Main(
        className="viz-container",
        children=[
            html.Div(
                className="section-title",
                children=[
                    html.H1("Revenu disponible des ménages entre 2019 et 2021"),
                ],
            ),
            html.Div(
                id="year-dropdowns",
                children=[
                    html.P("Source à comparer"),
                    dcc.RadioItems(
                        id="bouton",
                        options=[
                            {"label": "Revenu brut", "value": "Plus"},
                            {"label": "Prélèvement obligatoire", "value": "Moins"},
                            {"label": "Revenu disponible", "value": "Égale"},
                            {'label': "Taux d'épargne", 'value': "Taux d'epargne"},
                            {"label": "Tous", "value": "All"},
                        ],
                        value="All",
                        style={"width": "50%"},
                    ),
                ]
            ),
            html.Div([
                dcc.Graph(
                    id="the_graph",
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                )
            ]),
            html.Br(),
            html.Br(),
            html.Br(),
        ],
    )

# -------------------------------------------------------------------------------------

@app.callback(
    Output(component_id="the_graph", component_property="figure"),
    [Input(component_id="bouton", component_property="value")],
)
def update_figure(impact):
    fig = go.Figure()
    fig.data = []

    if impact == "All":
        colors = [THEME_GRAPH["light_blue_color"], THEME_GRAPH["dark_blue_color"], THEME_GRAPH["light_grey_color"]]
        i = 0
        liste_categorie = list(set(data.index.get_level_values("Impact")))
        liste_categorie.remove("Taux d'epargne")
        liste_categorie.sort()
        for categorie in liste_categorie:
            data_2 = data.loc[pd.IndexSlice[:, [categorie]], :]
            fig.add_trace(
                go.Bar(
                    x=TRIMESTERS,
                    y=data_2["Valeur numérique"],
                    name=categorie,
                    marker_color=colors[i],
                    hovertemplate=hover_template.revenus_total_hover_template()
                )
            )
            fig.update_layout(
                barmode="group",
                xaxis_title="Trimestres",
                yaxis_title="Revenus (CAD)",
                title = 'Évolution de la contribution au revenu des ménages',
            )
            i += 1

    if impact == "Plus":
        data_2 = data.loc[pd.IndexSlice[:, ["Plus"]], :]

        fig = px.bar(
            x=data_2.index.get_level_values("Temps"),
            y=data_2["Valeur numérique"],
            color=data_2.index.get_level_values("1er niveau de détail"),
            labels={"pop": "population of Canada"},
            height=400,
            color_discrete_sequence=[THEME_GRAPH["light_blue_color"], THEME_GRAPH["dark_blue_color"], THEME_GRAPH["light_grey_color"], THEME_GRAPH["green_color"]],
            title = "Revenu brut",
            custom_data=[data_2.index.get_level_values("1er niveau de détail")]
        )
        
        fig.update_layout(
            xaxis_title="Trimestres",
            yaxis_title="Revenus (CAD)",
        )
        fig.update_traces(
            hovertemplate=hover_template.revenus_hover_template(False)
        )

    if impact == "Moins":
        data_2 = data.loc[pd.IndexSlice[:, ["Moins"]], :]

        fig = px.bar(
            x=data_2.index.get_level_values("Temps"),
            y=data_2["Valeur numérique"],
            color=data_2.index.get_level_values("1er niveau de détail"),
            labels={"pop": "population of Canada"},
            height=400,
            color_discrete_sequence=[THEME_GRAPH["light_blue_color"], THEME_GRAPH["dark_blue_color"]],
            title = "Prélèvement obligatoire",
            custom_data=[data_2.index.get_level_values("1er niveau de détail")]
        )
        fig.update_layout(
            xaxis_title="Trimestres",
            yaxis_title="Revenus (CAD)",
        )
        fig.update_traces(
            hovertemplate=hover_template.revenus_hover_template(False)
        )

    if impact == "Égale":
        data_2 = data.loc[pd.IndexSlice[:, ["Égale"]], :]

        fig = px.bar(
            x=TRIMESTERS,
            y=data_2["Valeur numérique"],
            color=data_2.index.get_level_values("1er niveau de détail"),
            color_discrete_sequence=["green"],
            title="Revenu disponible des ménages",
            height=400,
            custom_data=[data_2.index.get_level_values("1er niveau de détail")]
        )
        fig.update_layout(
            xaxis_title="Trimestres",
            yaxis_title="Revenus (CAD)",
        )
        fig.update_traces(
            marker_color=(THEME_GRAPH["dark_blue_color"]),
            hovertemplate=hover_template.revenus_hover_template(False)
        )
        
    if impact == "Taux d'epargne" :
            data_2 = data.loc[pd.IndexSlice[:, ["Taux d'epargne"]], :]

            fig = px.bar(
                x=TRIMESTERS,
                y=data_2["Valeur numérique"],
                color=data_2.index.get_level_values('1er niveau de détail'),
                title = "Taux d'épargne des ménages",
                height= 400,
                custom_data=[data_2.index.get_level_values("1er niveau de détail")]
            )
            fig.update_layout(
                xaxis_title="Trimestres",
                yaxis_title="Pourcentage du revenu disponible ",
            )
            fig.update_traces(
                marker_color=(THEME_GRAPH["light_blue_color"]),
                hovertemplate=hover_template.revenus_hover_template(True)
            )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
    )

    fig.update_yaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    return fig
