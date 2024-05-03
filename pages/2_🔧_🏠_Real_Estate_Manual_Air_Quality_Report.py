import streamlit as st

from back_krisha import *
from plotter import *
st.set_page_config(layout="centered", page_title="Real Estate Manual Emissions Report", page_icon="🔧🏠")

st.write("")

st.title('Real Estate  Ecology Report Generator (Manual entering)')


realestate_data = {
    "location": None,
    "area": None,
    "floor": None,
}

realestate_data["location"] = st.text_input('Enter the location (latitude, longitude)')
# realestate_data["area"] = st.text_input('Enter the area of a real estate (sq. meters)')
# realestate_data["floor"] = st.text_input('Enter the floor')

if st.button('Generate Report'):

        st.image(MANUAL_report_handler(realestate_data["location"]), caption='Airway', use_column_width=True)

        hour_history_path = get_pm25_hour_history(MANUAL_get_sensor_location_id(realestate_data["location"]) + ".png")
        st.title("The history of PM2.5 rating over the last 24 hours")
        st.image(hour_history_path, use_column_width=True)
        append_image_to_pdf("./report/report.pdf",get_pm25_hour_history(MANUAL_get_sensor_location_id(realestate_data["location"]) + ".png"))

        week_history_path = get_pm25_week_history(MANUAL_get_sensor_location_id(realestate_data["location"]) + ".png")
        st.title("The history of PM2.5 rating over the last week")
        st.image(week_history_path, use_column_width=True)
        append_image_to_pdf("./report/report.pdf",get_pm25_week_history(MANUAL_get_sensor_location_id(realestate_data["location"]) + ".png"))


