import os

import pandas as pd
import streamlit as st

from streamlit.common.utils import aggrid_interactive_table, get_image
from streamlit.model.gpt2 import get_model


@st.cache
def get_cntnt_dataset():
    dataset = pd.read_csv(os.path.join('data', 'cntnt_meta.csv'), index_col=0)
    dataset = dataset[dataset.ITEM_ID != -1]
    print('read dataset')
    return dataset


MODEL = get_model()
URL = 'https://image.hanatour.com/usr/cms/resize/800_0/2018/10/08/10000/fab8ffdc-8c4f-4a9b-a7fc-32b967c354a2.jpg'
DISPLAT_COL = ['CNTNT_ID', 'CNTNT_NM', 'INTC_CONT', 'CNTNT_CATG_NM', 'ITEM_ID']


def add_schedule(item_id, dataset):
    st.session_state.schedule_data.append(item_id)
    model_output = MODEL.step_generate(st.session_state.schedule_data, top_k=10)
    model_output = pd.DataFrame({'ITEM_ID': model_output}).merge(
        dataset[DISPLAT_COL], on='ITEM_ID', how='left'
    )
    st.session_state.next_place = model_output[DISPLAT_COL]


def select_table(dataset):
    if st.session_state.next_place is None:
        st.write("시작 일정")
        selection = aggrid_interactive_table(
            dataset[DISPLAT_COL], multiple=False
        )
        # if selection:
        st.session_state.schedule_data = []
        if st.button('일정 추가'):
            if selection["selected_rows"]:
                item_id = selection["selected_rows"][0]['ITEM_ID']
                add_schedule(item_id, dataset)

    else:
        st.write("다음 일정")
        selection = aggrid_interactive_table(st.session_state.next_place, multiple=False, height=300)
        if st.button('일정 추가'):
            if selection["selected_rows"]:
                item_id = selection["selected_rows"][0]['ITEM_ID']
                add_schedule(item_id, dataset)


def schedule_table(dataset):
    schedule = pd.DataFrame({'ITEM_ID': st.session_state.schedule_data})
    schedule = schedule.merge(
        dataset[['ITEM_ID', 'CNTNT_ID', 'CNTNT_CATG_NM', 'CNTNT_NM', 'INTC_CONT']],
        on='ITEM_ID', how='left', validate='m:m'
    )

    for idx, (_, row) in enumerate(schedule.iterrows()):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 1, 2, 1])
            with col1:
                # if idx == 0: st.header('No.')
                st.write(f'{idx + 1}')
            with col2:
                # if idx == 0: st.header('내용')
                st.write(row.CNTNT_CATG_NM)
            with col3:
                st.write(row.CNTNT_NM)
            with col4:
                st.write(row.INTC_CONT)
            with col5:
                # if idx == 0: st.header('이미지')
                st.image(get_image(URL), caption='image')


def main():
    if 'schedule_data' not in st.session_state:
        st.session_state.schedule_data = []

    if 'next_place' not in st.session_state:
        st.session_state.next_place = None

    dataset = get_cntnt_dataset()
    if st.button('Reset'):
        st.session_state.schedule_data = []
        st.session_state.next_place = None
    schedule_table(dataset=dataset)
    select_table(dataset=dataset)


if __name__ == '__main__':
    main()
