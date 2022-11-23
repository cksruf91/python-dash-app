from typing import List

import dash_bootstrap_components as dbc
from dash import html, dash_table


def interactive_datatable(component_id: str, data: List[dict], columns: List[dict],
                          select_mode: str = 'single') -> html.Div:
    return html.Div(
        children=[
            dash_table.DataTable(
                id=component_id,
                data=data,
                columns=columns,
                page_size=15, page_action='native',
                style_table={'height': '400px', 'overflowY': 'auto'},
                row_selectable=select_mode,
                selected_rows=[]
            )
        ],
        id='table'
    )


def schedule_table(data: List[dict], page_id: str) -> List[dbc.Row]:
    rows = []
    for i, row in enumerate(data):
        line = [
            dbc.Row(
                [
                    dbc.Col(html.Div(id=f'{page_id}-col0', children=f'{i + 1}'), width={"size": 1}),
                    dbc.Col(html.Div(id=f'{page_id}-col1', children=row['CNTNT_ID']), width={"size": 2}),
                    dbc.Col(html.Div(id=f'{page_id}-col2', children=row['CNTNT_CATG_NM']), width={"size": 2}),
                    dbc.Col(html.Div(id=f'{page_id}-col3', children=row['CNTNT_NM']), width={"size": 2}),
                    dbc.Col(html.Div(id=f'{page_id}-col4', children=row['INTC_CONT']), width={"size": 4})
                ]
            ),
            html.Hr()
        ]
        rows.extend(line)
    return rows
