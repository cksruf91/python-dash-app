import os
from typing import List

import pandas as pd
from dash import Dash, dash_table, html, State
from dash.dependencies import Input, Output

DASH = Dash(__name__)


def get_metadata():
    data = pd.read_csv(os.path.join('../../data', 'cntnt_meta.csv'), index_col=0)
    data = data[data.ITEM_ID != -1].copy()
    return data


META_DATA = get_metadata()


def get_table_source(dataset: pd.DataFrame) -> tuple[list[dict], list[dict[str]]]:
    columns = [{"name": i, "id": i} for i in dataset.columns]
    source = []
    for row in dataset.to_dict('records'):
        row['id'] = row['ITEM_ID']
        source.append(row)
    return source, columns


def interactive_datatable(data: pd.DataFrame, columns: List) -> html.Div:
    return html.Div(
        children=[
            dash_table.DataTable(
                id='interactive-table',
                data=data,
                columns=columns,
                page_size=30, page_action='native',
                style_table={'height': '300px', 'overflowY': 'auto'},
                row_selectable="multi",
            )
        ],
        id='table'
    )


@DASH.callback(
    Output(component_id='interactive-table', component_property='data'),
    Input(component_id='submit-button', component_property='n_clicks'),
    State(component_id='interactive-table', component_property='selected_row_ids')
)
def update_table(n_clicks: int, selected_row_ids: List):
    if selected_row_ids is None:
        selected_row_ids = []
    data = META_DATA[META_DATA['ITEM_ID'].isin(selected_row_ids) == False]
    data, _ = get_table_source(data)
    return data


@DASH.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='submit-button', component_property='n_clicks'),
    State(component_id='interactive-table', component_property='selected_row_ids')
)
def button_callback(n_clicks, selected_row_ids):
    return f'{n_clicks}, {selected_row_ids}'


def main():
    meta, columns = get_table_source(META_DATA)

    # metadata = interactive_datatable(meta)
    DASH.layout = html.Div(
        [
            html.H3("일정 테이블"),
            interactive_datatable(meta, columns),
            html.Button(children='Submit', id='submit-button', n_clicks=0),
            html.Br(),
            html.Div(id='my-output', children='hello friends'),
        ]
    )
    return DASH


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
