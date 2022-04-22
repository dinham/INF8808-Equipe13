from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from flask import Response

from app import app, server
from visualisations.caracteristiques import caracteristiques
from visualisations.depenses_menages import depenses_menages
from visualisations.horaires import horaires
from visualisations.inflation import inflation
from visualisations.paralleles import paralleles
from visualisations.pib import pib
from visualisations.revenu_menages import revenu_menages
from visualisations.salaires import salaires

html.Button()

app.layout = html.Div(
    id="main",
    children=[
        dcc.Location(id="url", refresh=False),
        html.Div(
            id="page-title",
            children=[
                html.Img(src="assets/revenuqc-logo.png", width=360, height=300),
                html.H1("Portrait économique du Québec"),
            ]
        ),
        html.Div(
            id="link-buttons",
            children=[
                dcc.Link(html.Button("PIB"), href="/pib", refresh=True),
                dcc.Link(html.Button("Inflation"), href="/inflation"),
                dcc.Link(html.Button("Revenu des ménages"), href="/revenu_menages"),
                dcc.Link(html.Button("Dépenses des ménages"), href="/depenses_menages"),
                dcc.Link(
                    html.Button("Caractéristiques du marché du travail"),
                    href="/caracteristiques",
                ),
                dcc.Link(
                    html.Button("Horaires de travail et emplois"), href="/horaires"
                ),
                dcc.Link(html.Button("Salaires"), href="/salaires"),
                dcc.Link(html.Button("Mises en parallèle"), href="/paralleles"),
            ],
            className="row",
        ),
        html.Div(id="page-content", children=[]),
    ],
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/pib":
        return pib.get_layout()
    if pathname == "/inflation":
        return inflation.get_layout()
    if pathname == "/revenu_menages":
        return revenu_menages.get_layout()
    if pathname == "/depenses_menages":
        return depenses_menages.get_layout()
    if pathname == "/caracteristiques":
        return caracteristiques.get_layout()
    if pathname == "/horaires":
        return horaires.get_layout()
    if pathname == "/salaires":
        return salaires.get_layout()
    if pathname == "/paralleles":
        return paralleles.get_layout()
    else:
        return "Sélectionnez une section pour la visualiser!"


if __name__ == "__main__":
    app.run_server(debug=False)
