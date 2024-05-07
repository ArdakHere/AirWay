import streamlit as st
from utils.back_krisha import get_sensor_location_id_from_manual_input, create_apartment_report_from_manual_input
from utils.plotter import get_pm25_hour_history, get_pm25_week_history

st.set_page_config(
    layout="centered",
    page_title="Real Estate Manual Emissions Report",
    page_icon="🔧🏠")

st.write("")
st.title('Real Estate  Ecology Report Generator (Manual entering)')

realestate_data = {
    "location": None,
    "area": None,
    "floor": None,
}

realestate_data["location"] = st.text_input(
    'Enter the location (latitude, longitude)')


if st.button('Generate Report'):
    st.image(
        create_apartment_report_from_manual_input(realestate_data["location"]),
        caption='Airway',
        use_column_width=True)

    hour_history_path = get_pm25_hour_history(
        get_sensor_location_id_from_manual_input(realestate_data["location"]) + ".png")
    st.title("The history of PM2.5 rating over the last 24 hours")
    st.image(hour_history_path, use_column_width=True)

    week_history_path = get_pm25_week_history(
        get_sensor_location_id_from_manual_input(realestate_data["location"]) + ".png")
    st.title("The history of PM2.5 rating over the last week")
    st.image(week_history_path, use_column_width=True)
