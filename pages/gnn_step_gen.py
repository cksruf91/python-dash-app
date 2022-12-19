from typing import List, Tuple

import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, Output, Input, State, dcc, ctx

from common.utils import get_metadata, get_table_source, get_gnn_model
from components.app import APP
from components.tables import interactive_datatable, schedule_table

METADATA = get_metadata()
META, COLUMNS = get_table_source(METADATA)
MODEL = get_gnn_model()
METADATA.index = METADATA['ITEM_ID']
ITEM_MAPPER = METADATA.to_dict('index')
PAGE_ID = 'gnn-step'


@APP.callback(
    Output(component_id=f'{PAGE_ID}-interactive-table', component_property='selected_rows'),
    Output(component_id=f'{PAGE_ID}-schedule-items', component_property='data'),
    Output(component_id=f'{PAGE_ID}-interactive-table', component_property='data'),
    Input(component_id=f'{PAGE_ID}-submit-button', component_property='n_clicks'),
    Input(component_id=f'{PAGE_ID}-reset-button', component_property='n_clicks'),
    State(component_id=f'{PAGE_ID}-interactive-table', component_property='selected_row_ids'),
    State(component_id=f'{PAGE_ID}-schedule-items', component_property='data'),
    prevent_initial_call=True
)
def summit_callback(submit_clicks: int, reset_clicks: int, selected_row_ids: List, schedule_items: List) -> Tuple[
    List, List[int], List[dict]]:
    """ submit 버튼, reset 버튼 클릭 callback 함수

    Args:
        submit_clicks: submit 버튼 클린횟수 (사용안함)
        reset_clicks: reset 버튼 클린횟수 (사용안함)
        selected_row_ids: datatable 에서 선택한 컬럼 ID(ITEM_ID)
        schedule_items: 이전에 선택된 아이템 아이디

    Returns:
        selected_rows: 항상 빈 list, 초기 선택값을 제거 하기 위함
        schedule_items: 단계별로 선택된 아이템 아이디
        source: 일정 테이블 생성 데이터
    """
    if selected_row_ids is None:
        selected_row_ids = []

    if ctx.triggered_id == f'{PAGE_ID}-submit-button':
        schedule_items += selected_row_ids
        pred_items: List[int] = MODEL.step_generate(batch=schedule_items, top_k=10)
        next_item_df = pd.DataFrame(
            [ITEM_MAPPER[item] for item in pred_items]
        )
        next_item_df.index = next_item_df['ITEM_ID']
        source, _ = get_table_source(next_item_df)
        return [], schedule_items, source

    if ctx.triggered_id == f'{PAGE_ID}-reset-button':
        schedule_items = []
        source = META.copy()
        return [], schedule_items, source

    raise ValueError(f'triggered_id: {ctx.triggered_id}')


@APP.callback(
    Output(component_id=f'{PAGE_ID}-schedule_display', component_property='children'),
    Input(component_id=f'{PAGE_ID}-schedule-items', component_property='data'),
    prevent_initial_call=True
)
def update_schedule(data: List[int]):
    """ 스케줄 테이블 업데이트 callback,
    summit_callback 에서 {page_id}-schedule-items 의 data 를 업데이트 했을때 동작

    Args:
        data: 스케줄 아이템 아이디 리스트

    Returns: 스케줄 테이블
    """
    selected_item = [ITEM_MAPPER[item] for item in data]
    return schedule_table(data=selected_item, page_id=PAGE_ID)


def layout() -> html.Div:
    """ 단계별 일정생성 페이지 레이아웃 """
    return html.Div(
        [
            dcc.Store(id=f'{PAGE_ID}-schedule-items', data=[]),
            html.H3("GNN 단계별 일정 테이블"),
            interactive_datatable(f'{PAGE_ID}-interactive-table', META, COLUMNS),
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
