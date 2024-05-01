import streamlit as st

from back_krisha import *

st.set_page_config(layout="centered", page_title="Krisha.kz Air Quality Report", page_icon="🏠")

st.title('Krisha Air Quality Report Generator')

keyword = st.text_input('Paste the link to apartment/house listed on Krisha.kz:', '')


# Button to trigger the action
if st.button('Generate Report'):
    if keyword:

        st.image(report_handler(keyword), caption='Airway', use_column_width=True)

        st.title("The history of PM2.5 rating over the last 24 hours")
        st.image(get_pm25_hour_history(get_sensor_location_id(keyword) + ".png"), use_column_width=True)

        st.title("The history of PM2.5 rating over the last week")
        st.image(get_pm25_week_history(get_sensor_location_id(keyword) + ".png"), use_column_width=True)


        #st.image(report_hanlder(keyword), caption='Airway', use_column_width=True)
    else:
        st.text("Please enter a link before generating")


# Set background color
