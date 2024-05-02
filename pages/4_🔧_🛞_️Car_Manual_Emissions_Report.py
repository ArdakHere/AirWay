import streamlit as st
import matplotlib.pyplot as plt

from back_kolesa import kolesa_html_download, kolesa_html_reader, gpt_caller
from car_emission_generator import generate_report_for_car_emission

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
    if report:
        data = gpt_caller(car_data)
        report = generate_report_for_car_emission(data, car_data)

        labels = []
        values = []
        explode = ()
        for i, key in enumerate(data["chemicals"]):
            labels.append(key.upper())
            values.append(data["chemicals"][key])
            explode += (0,)
            val = data["chemicals"][key]

        fig1, ax1 = plt.subplots()
        ax1.pie(values, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        with open(data['report_path_pdf'], "rb") as file:
                st.download_button(
                    label="Download Report as PDF",
                    data=file,
                    file_name=f"car_report_{car_data['car_title']}.pdf",
                    mime="image/png"
                )
            
        st.image(data['report_path'], caption='Report', use_column_width=True)
