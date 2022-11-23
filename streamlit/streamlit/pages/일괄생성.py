import os

import pandas as pd
import streamlit as st

from streamlit.common.utils import get_image, aggrid_interactive_table
from streamlit.model.gpt2 import get_model

model = get_model()
url = 'https://image.hanatour.com/usr/cms/resize/800_0/2018/10/08/10000/fab8ffdc-8c4f-4a9b-a7fc-32b967c354a2.jpg'


@st.cache
def get_cntnt_dataset():
    dataset = pd.read_csv(os.path.join('data', 'cntnt_meta.csv'), index_col=0)
    dataset = dataset[dataset.ITEM_ID != -1]
    print('read dataset')
    return dataset


def main():
    # col1, col2, col3, col4 = st.columns([2, 0.5, 3, 0.5])

    dataset = get_cntnt_dataset()
    selection = aggrid_interactive_table(
        dataset[['CNTNT_ID', 'CNTNT_CATG_NM', 'CNTNT_NM', 'INTC_CONT', 'ITEM_ID']]
    )
    model_output = None

    if st.button('Reset'):
        selection = None
        model_output = None

    if selection:
        st.write("You selected:")
        selected_rows = [
            {'CNTNT_ID': rows['CNTNT_ID'],
             'CNTNT_NM': rows['CNTNT_NM'],
             'ITEM_ID': rows['ITEM_ID']
             } for rows in selection["selected_rows"]
        ]
        st.table(pd.DataFrame(selected_rows))

        selected_item_id = [row['ITEM_ID'] for row in selected_rows]
        model_output = model.generate(selected_item_id, max_len=10)

    if model_output is not None:
        schedule = pd.DataFrame({'ITEM_ID': model_output})
        schedule = schedule.merge(
            dataset[['ITEM_ID', 'CNTNT_ID', 'CNTNT_CATG_NM', 'CNTNT_NM', 'INTC_CONT']],
            on='ITEM_ID', how='left', validate='m:m'
        )
        for idx, (_, row) in enumerate(schedule.iterrows()):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 2, 1])
                with col1:
                    # if idx == 0: st.header('No.')
                    st.write(f'일정 {idx + 1}')
                with col2:
                    # if idx == 0: st.header('내용')
                    st.write(row.CNTNT_CATG_NM)
                with col3:
                    st.write(row.CNTNT_NM)
                with col4:
                    st.write(row.INTC_CONT)
                with col5:
                    # if idx == 0: st.header('이미지')
                    st.image(get_image(url), caption='image')


if __name__ == '__main__':
    main()
