import os

import streamlit as st
import pandas as pd


@st.cache
def get_cntnt_datset():
    dataset = pd.read_csv(os.path.join('data', 'cntnt_meta.csv'), index_col=0)
    print('read dataset')
    return dataset


st.text_input("CNTNT_NM like", key="cntnt_nm")

cntnt_meta = get_cntnt_datset()
cntnt_meta = cntnt_meta[cntnt_meta.CNTNT_NM.map(
    lambda x: st.session_state.cntnt_nm in x
)]
st.write("## Content table")
st.write(cntnt_meta)

cntnt_meta = get_cntnt_datset()

