import os

import dash

ASSETS_PATH = os.path.abspath(os.path.join(os.curdir, "assets"))

stylesheets = [os.path.join(ASSETS_PATH, sheet) for sheet in os.listdir(ASSETS_PATH)]

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=stylesheets,
)
app.title = "Portrait économique du Quebec | Revenu Québec"

server = app.server
