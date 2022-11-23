from dash import html


def layout():
    return html.Div(
        id='home',
        children=[
            html.H1(children='Home'),
            html.Div(
                children='page content'
            )
        ]
    )
