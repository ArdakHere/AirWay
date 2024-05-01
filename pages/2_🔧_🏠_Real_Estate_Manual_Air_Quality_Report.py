import streamlit as st

from back_kolesa import kolesa_html_download, kolesa_html_reader, gpt_caller
st.set_page_config(layout="centered", page_title="Real Estate Manual Emissions Report", page_icon="🔧🏠")

st.write("")

st.title('Real Estate  Ecology Report Generator (Manual entering)')


realestate_data = {
    "location": None,
    "area": None,
    "floor": None,
}

realestate_data["location"] = st.text_input('Enter the location (latitude, longitude)')
realestate_data["area"] = st.text_input('Enter the area of a real estate (sq. meters)')
realestate_data["floor"] = st.text_input('Enter the floor')

if st.button('Generate Report'):

    report = realestate_data

    if report:
        # Display HTML content with taller st.text
        st.text_area(label="Report", value=report, height=500, max_chars=None, key=None)

