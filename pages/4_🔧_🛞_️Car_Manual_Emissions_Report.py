import streamlit as st

from back_kolesa import kolesa_html_download, kolesa_html_reader, gpt_caller
st.set_page_config(layout="centered", page_title="Car Manual Emissions Report", page_icon="🔧🛞")

st.write("")

st.title('Car Ecology Report Generator (Manual entering)')


car_data = {
    "car_title": None,
    "generation": None,
    "engine_displacement": None,
    "distance run (km)": None,
    "N-wheel drive": None,
}

car_data["car_title"] = st.text_input('Enter the car brand and model')
car_data["generation"] = st.text_input('Enter the generation or a production year')
car_data["engine_displacement"] = st.text_input('Enter the engine displacement')
car_data["distance run (km)"] = st.text_input('Enter the mileage (km)')
car_data["N-wheel drive"] = st.text_input('Enter the wheel drive configuration')

report = gpt_caller(car_data)

if st.button('Generate Report'):
    report = gpt_caller(car_data)

    if report:
        # Display HTML content with taller st.text
        st.text_area(label="Report", value=report, height=500, max_chars=None, key=None)

