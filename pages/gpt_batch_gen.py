from typing import List

import dash_bootstrap_components as dbc
from dash import html, Output, Input, State, dcc, ctx

from common.model.gpt2 import get_gtp_model
from common.utils import get_metadata, get_table_source
from components.app import APP
from components.tables import interactive_datatable, schedule_table

METADATA = get_metadata()
META, COLUMNS = get_table_source(METADATA)
GPT = get_gtp_model()
METADATA.index = METADATA['ITEM_ID']
ITEM_MAPPER = METADATA.to_dict('index')
PAGE_ID = 'gpt-batch'


@APP.callback(
    Output(component_id=f'{PAGE_ID}-schedule_display', component_property='children'),
    Input(component_id=f'{PAGE_ID}-submit-button', component_property='n_clicks'),
    Input(component_id=f'{PAGE_ID}-reset-button', component_property='n_clicks'),
    State(component_id=f'{PAGE_ID}-interactive-table', component_property='selected_row_ids'),
    prevent_initial_call=True
)
def update_schedule(submit_clicks: int, reset_clicks: int, selected_row_ids: List[int]) -> List[dbc.Row]:
    """ submit 버튼, reset 버튼 클릭 callback 함수

    Args:
        submit_clicks: submit 버튼 클린횟수 (사용안함)
        reset_clicks: reset 버튼 클린횟수 (사용안함)
        selected_row_ids: datatable 에서 선택한 컬럼 ID(ITEM_ID)

    Returns:
        schedule 테이블
    """
    if ctx.triggered_id == f'{PAGE_ID}-submit-button':
        output = GPT.generate(selected_row_ids, max_len=30)
        selected_item = [ITEM_MAPPER[o] for o in output]
        return schedule_table(data=selected_item, page_id=PAGE_ID)

    if ctx.triggered_id == f'{PAGE_ID}-reset-button':
        return schedule_table(data=[], page_id=PAGE_ID)

    raise ValueError(f'triggered_id: {ctx.triggered_id}')


def layout():
    """ 일괄 일정생성 페이지 레이아웃 """
    return html.Div(
        [
            dcc.Store(id=f'{PAGE_ID}-schedule-items', data=[]),
            html.H3("일괄 일정 테이블"),
            interactive_datatable(f'{PAGE_ID}-interactive-table', META, COLUMNS, select_mode="multi"),
            dbc.Row(
                [
                    dbc.Col(html.Button(children='Submit', id=f'{PAGE_ID}-submit-button', n_clicks=0),
                            width={"size": 1}),
                    dbc.Col(html.Button(children='Reset', id=f'{PAGE_ID}-reset-button', n_clicks=0)),
                ]
            ),
            html.Hr(),
            html.Div(
                id=f'{PAGE_ID}-schedule_display', children=''
            )
        ]
    )
