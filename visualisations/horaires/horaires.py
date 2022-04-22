from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from app import app
from utils import get_data

import hover_template
from template import THEME_GRAPH


df_horaires = get_data("horaires.csv")
df_salaires = get_data("salaires_horaires.csv")
years = df_horaires["Année"].unique()

# -------------------------------------------------------------------------------

def get_layout():
    return html.Main(
        className="viz-container",
        children=[
            html.Div(
                className="section-title",
                children=[
                    html.H1("Écart salarial et d'heures effectivement travaillées entre les sexes au Québec selon l'industrie entre 2017 et 2021"),
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
                    )
                ],
            ),
            dcc.Graph(
                id="salaires-sexe-graph",
                className="graph",
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False,
                ),
            ),
            dcc.Graph(
                id="horaires-sexe-graph",
                className="graph",
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False,
                ),
            )
        ],
    )
@app.callback(
    Output("salaires-sexe-graph", "figure"),
    Input("year-start-dropdown", "value")
)
# https://medium.com/@ginoasuncion/creating-a-dumbbell-plot-with-plotly-python-570ff768ff7e
def update_figure_salaires(selected_year):
    years_df = df_salaires.loc[df_salaires['Année'] == selected_year]

    fig = px.scatter(
        years_df,
        x="Salaires",
        y="Industries",
        color="Sexe",
        text='Salaires',
        range_x=[10, 50],
        title=f"Écart salarial entre les sexes au Québec par industrie de l'année {selected_year}",
        color_discrete_sequence=[THEME_GRAPH["light_blue_color"], THEME_GRAPH["dark_blue_color"]],
        custom_data=['Sexe']
    )

    fig.update_traces(
        marker=dict(size=10, opacity=1),
        textposition='top center',
        textfont=dict(size=10),
        hovertemplate=hover_template.horaires_hover_template()
    )
    fig.update_layout(
        xaxis_title="Salaire ($)",
        yaxis_title="Industries (SCIAN)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
        legend_itemclick=False,
        legend_borderwidth=1
    )
    fig.update_xaxes(
        showline=True,
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    fig.update_yaxes(
        dtick=1,
        showline=True,
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    for i in years_df["Industries"].unique():
        df_sub = years_df[years_df["Industries"] == i]

        fig.add_shape(
            type="line",
            layer="above",
            line=dict(width=5, color='grey'),
            opacity=0.3,
            y0=df_sub.Industries.values[0],
            x0=df_sub.Salaires.values[0],
            y1=df_sub.Industries.values[1],
            x1=df_sub.Salaires.values[1],
        )    


    return fig

@app.callback(
    Output("horaires-sexe-graph", "figure"),
    Input("year-start-dropdown", "value")
)
def update_figure_horaires(selected_year):
    years_df = df_horaires.loc[df_horaires['Année'] == selected_year]

    fig = px.scatter(
        years_df,
        x="Heures",
        y="Industries",
        color="Sexe",
        text='Heures',
        range_x=[20, 50],
        title=f"Écart d'heures effectivement travaillés entre les sexes au Québec par industrie de l'année {selected_year}",
        color_discrete_sequence=[THEME_GRAPH["light_blue_color"], THEME_GRAPH["dark_blue_color"]],
        custom_data=['Sexe']
    )

    fig.update_traces(
        marker=dict(size=10, opacity=1),
        textposition='top center',
        textfont=dict(size=10),
        hovertemplate=hover_template.horaires_hover_template()
    )
    fig.update_layout(
        xaxis_title="Heures (h)",
        yaxis_title="Industries (SCIAN)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),
        legend_itemclick=False,
        legend_borderwidth=1
    )
    fig.update_xaxes(
        gridcolor='#f0f0f0',
        gridwidth=2,
    )

    fig.update_yaxes(
        dtick=1,
        gridcolor='#f0f0f0',
        gridwidth=2,
    )
    
    for i in years_df["Industries"].unique():
        df_sub = years_df[years_df["Industries"] == i]

        fig.add_shape(
            type="line",
            layer="above",
            line=dict(width=5, color='grey'),
            opacity=0.3,
            y0=df_sub.Industries.values[0],
            x0=df_sub.Heures.values[0],
            y1=df_sub.Industries.values[1],
            x1=df_sub.Heures.values[1],
        )

    return fig