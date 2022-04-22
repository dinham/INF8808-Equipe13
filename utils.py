import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure

from constants import ROOT_PATH

def get_data(filename: str):
    return pd.read_csv(ROOT_PATH.joinpath("datasets", filename))
def get_data2(filename: str):
    return pd.read_csv(ROOT_PATH.joinpath("datasets", filename),on_bad_lines='skip', encoding = 'UTF-8',sep=';',decimal='.')
def get_data_3(filename: str):
    return pd.read_csv(ROOT_PATH.joinpath("datasets", filename),sep = ';',header = 1, decimal  = ',')

def get_empty_figure(title):
    fig = px.line()
    fig.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False),
        annotations=[
            dict(
                xref="x",
                yref="y",
                text=title,
                showarrow=False,
            )
        ],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial Narrow",
            size=15,
        ),

    )
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])

    return fig

def add_rectangle_shape(fig: Figure):
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=25,
                x1=75,
                y0=25,
                y1=75,
                fillcolor="#DFD9E2",
                line=dict(color="#DFD9E2"),
            ),
        ],
    )