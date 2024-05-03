import streamlit as st

from backend_files.plotter import *


st.set_page_config(layout="centered", page_title="Kolesa.kz Emissions Report", page_icon="🛞")

st.title('Kolesa Ecology Report Generator')


kolesa_link = st.text_input('Paste the link to apartment/house/car listed on Kolesa.kz:', '')

# Button to trigger the action
if st.button('Generate Report'):
    # Check if keyword is not empty
    if kolesa_link:
        # Download HTML content and display it

        link_html_code = kolesa_html_download(kolesa_link)
        car_data = kolesa_html_reader(link_html_code)

        st.image(generate_report_for_a_car(car_data["car_title"], car_data["generation"],
                                  car_data["engine_displacement"], car_data["distance run (km)"],
                                  car_data["N-wheel drive"]), caption='Airway', use_column_width=True)



else:
    st.text("Please enter a link before generating the car report.")

