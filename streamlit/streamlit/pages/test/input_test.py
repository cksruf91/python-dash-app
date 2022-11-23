import pandas as pd
import streamlit as st

if 'temp' not in st.session_state:
    st.session_state.temp = []

print('loop')
genre = st.radio(
    "What's your favorite movie genre",
    ('Comedy', 'Drama', 'Documentary'), options=[1,2,3]
)


if genre:
    st.session_state.temp.append(genre)

if st.button('summit'):
    dataset = pd.DataFrame(
        {'genre': st.session_state.temp}
    )
    st.write(dataset)