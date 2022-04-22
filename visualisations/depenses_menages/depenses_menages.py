from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from utils import get_data2
from app import app

import hover_template
from template import THEME_GRAPH

depense = get_data2("depense_menages_cat.csv")
depense_all = get_data2("depense_menage_detail.csv")

liste_service = ['Santé','Transports',"Dépenses nettes à l'étranger",'Logement, eau, électricité, gaz et autres combustibles','Loisirs et culture','Communications','Assurance et services financiers','Enseignement']
liste_biens = ['Produits alimentaires et boissons non alcoolisées','Meubles, articles de ménage et autres biens et services liés au logement','Boissons alcoolisées, tabac et cannabis',"Articles d'habillement et chaussures","Logement, eau, électricité, gaz et autres combustibles"]

colors = [
    THEME_GRAPH["light_blue_color"],
    THEME_GRAPH["dark_blue_color"],
    THEME_GRAPH["light_grey_color"],
    THEME_GRAPH["turquoise_color"],
    THEME_GRAPH["green_color"],
    THEME_GRAPH["apple_green_color"],
    THEME_GRAPH["red_color"],
    THEME_GRAPH["orange_color"],
]

def get_layout():
    return html.Main(
        html.Div([
            html.Div(
                className="section-title",
                children=[
                    html.H1("Évolution des dépenses trimestrielles des ménages entre 2018 et 2021"),
                ],
            ),
            html.Div(
                className="section-subtitle",
                children=[
                    html.P('Quel catégorie de dépense voulez-vous comparer ?'),
                    dcc.RadioItems(
                            id='bouton2',
                            options=[
                                {'label': 'Bien', 'value': 'bien'},
                                {'label': 'Service', 'value': 'service'},
                                {'label': 'Bien et Service', 'value': 'bets'},
                            ],
                            value='bets',
                            style={"width": "50%"}
                    ),
                ]
            ),
            html.Div([
                dcc.Graph(
                    id='the_graph_bien',
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                )
            ])    
        ]),
    )

@app.callback(
    Output(component_id='the_graph_bien', component_property='figure'),
    [Input(component_id='bouton2', component_property='value')],
)

def update_figure (impact) :
    plot = go.Figure()
    if impact == 'bets':
        depense_bien = depense.loc[depense['1er niveau de détail'] == 'Biens']
        plot.add_trace(go.Scatter(
            name='Bien',
            x=depense_bien['Temps'],
            y=depense_bien['Valeur numérique'],
            stackgroup='one',
            marker=dict(color=colors[0]),
            text=depense_bien['1er niveau de détail'],
            hovertemplate=hover_template.depenses_hover_template()
        ))
        depense_service = depense.loc[depense['1er niveau de détail'] == 'Services']
        plot.add_trace(go.Scatter(
            name='Service',
            x=depense_service['Temps'],
            y=depense_service['Valeur numérique'],
            stackgroup='one',
            marker=dict(color=colors[1]),
            text=depense_service['1er niveau de détail'],
            hovertemplate=hover_template.depenses_hover_template()
        )
    )

    elif impact == 'bien' :
        i = 0
        for element in liste_biens:
            depense_bien = depense_all.loc[depense_all['1er niveau de détail'] == element]
            plot.add_trace(go.Scatter(
                name=element,
                x=depense_bien['Temps'],
                y=depense_bien['Valeur numérique'],
                stackgroup='one',
                marker=dict(color=colors[i]),
                text=depense_bien['1er niveau de détail'],
                hovertemplate=hover_template.depenses_hover_template()
            ))
            i += 1

    elif impact =='service' :
        i = 0
        for element in liste_service:
            depense_bien = depense_all.loc[depense_all['1er niveau de détail'] == element]
            plot.add_trace(go.Scatter(
                name=element,
                x=depense_bien['Temps'],
                y=depense_bien['Valeur numérique'],
                stackgroup='one',
                marker=dict(color=colors[i]),
                text=depense_bien['1er niveau de détail'],
                hovertemplate=hover_template.depenses_hover_template()
            ))
            i += 1

    plot.update_layout(
        title="Évolution des dépenses trimestrielles des ménages",
        xaxis_title="Trimestres",
        yaxis_title="Dépenses (M$)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
    )

    plot.update_xaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    plot.update_yaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )
    
    return(plot)
