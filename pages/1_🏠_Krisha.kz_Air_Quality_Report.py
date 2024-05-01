import streamlit as st

from back_krisha import *

st.set_page_config(layout="centered", page_title="Krisha.kz Air Quality Report", page_icon="🏠")

st.title('Krisha Air Quality Report Generator')

keyword = st.text_input('Paste the link to apartment/house listed on Krisha.kz:', '')

# Button to trigger the action
if st.button('Generate Report'):
    if keyword:
        st.image(temp_func(), caption='Airway', use_column_width=True)
        #st.image(report_hanlder(keyword), caption='Airway', use_column_width=True)
    else:
        st.text("Please enter a link before generating")