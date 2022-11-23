import streamlit as st
from streamlit.common.utils import get_image

url = 'https://image.hanatour.com/usr/cms/resize/400_0/2018/10/08/10000/fab8ffdc-8c4f-4a9b-a7fc-32b967c354a2.jpg'
st.image(
    get_image(url), caption='image',
)
