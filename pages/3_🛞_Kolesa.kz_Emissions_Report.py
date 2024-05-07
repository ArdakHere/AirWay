import streamlit as st

from utils.back_kolesa import download_car_webpage, read_remote_kolesa_page
from utils.plotter import *


st.set_page_config(
    layout="centered",
    page_title="Kolesa.kz Emissions Report",
    page_icon="🛞")

st.title('Kolesa Ecology Report Generator')
kolesa_link = st.text_input(
    'Paste the link to apartment/house/car listed on Kolesa.kz:', '')

if st.button('Generate Report'):
    if kolesa_link:
        link_html_code = download_car_webpage(kolesa_link)
        car_data = read_remote_kolesa_page(link_html_code)

        st.image(
            generate_report_for_a_car(
                car_data["car_title"],
                car_data["generation"],
                car_data["engine_displacement"],
                car_data["distance run (km)"],
                car_data["N-wheel drive"]),
            caption='Airway',
            use_column_width=True)
else:
    st.text("Please enter a link before generating the car report.")
