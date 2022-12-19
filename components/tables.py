from typing import List

import dash_bootstrap_components as dbc
from dash import html, dash_table


def interactive_datatable(component_id: str, data: List[dict], columns: List[dict],
                          select_mode: str = 'single', head_color='#d1d1cd') -> html.Div:
    return html.Div(
        children=[
            dash_table.DataTable(
                id=component_id,
                data=data,
                columns=columns,
                page_size=15, page_action='native',
                style_table={'height': '400px', 'overflowY': 'auto'},
                row_selectable=select_mode,
                selected_rows=[],
                style_header={
                    'backgroundColor': head_color,
                    'fontWeight': 'bold'
                },
            )
        ],
        id='table'
    )


def schedule_table(data: List[dict], page_id: str) -> dbc.Table:
    table_header = html.Thead(html.Tr(
        [html.Th('no'), html.Th('번호'), html.Th('카테고리'), html.Th('컨텐츠명'), html.Th('상세')]
    ))

    rows = []
    for i, row in enumerate(data):
        line = html.Tr([
            html.Td(f'{i + 1}', id=f'{page_id}-schedule-col0', ),
            html.Td(row['CNTNT_ID'], id=f'{page_id}-schedule-col1'),
            html.Td(row['CNTNT_CATG_NM'], id=f'{page_id}-schedule-col2'),
            html.Td(row['CNTNT_NM'], id=f'{page_id}-schedule-col3'),
            html.Td(row['INTC_CONT'], id=f'{page_id}-schedule-col4'),
        ])
        rows.append(line)

    table_body = html.Tbody(rows)
    return dbc.Table([table_header, table_body], bordered=True, dark=False, striped=True, style={})
