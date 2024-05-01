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
    raw_report = gpt_caller(car_data)
    # {
    #     "impact": "5/10",
    #     "co2": 1920, 
    #     "pm2_5": 192, 
    #     "pm10": 56, 
    #     "recommendation": "Regular maintenance and tuning can improve fuel efficiency and reduce emissions. Consider using public transport, carpooling, or switching to electric vehicles to reduce emissions further.", 
    #     "trees_killed": 11
    # }

    # generate_report_for_car_emission

    if report:
        st.image(gpt_caller(car_data), caption='Report', use_column_width=True)
        # Display HTML content with taller st.text

