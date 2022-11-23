import dash_bootstrap_components as dbc
from dash import Dash

APP = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
