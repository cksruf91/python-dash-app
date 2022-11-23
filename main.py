import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input

from components.app import APP
from pages import home, page1, page2

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def sidebar():
    return html.Div(
        [
            html.H3("일정생성", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("GPT 단계별 생성", href="/step-gen", active="exact"),
                    dbc.NavLink("GPT 일괄 생성", href="/batch-gen", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )


def content():
    return html.Div(
        id="page-content", style=CONTENT_STYLE, children=[]
    )


def main_layout():
    return html.Div([dcc.Location(id="url"), sidebar(), content()])


@APP.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout()
    elif pathname == "/step-gen":
        return page1.layout()
    elif pathname == "/batch-gen":
        return page2.layout()
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


def main():
    APP.layout = main_layout()
    return APP


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
