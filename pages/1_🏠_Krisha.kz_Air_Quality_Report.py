import streamlit as st
from backend_files.back_krisha import create_apartment_report_from_link, get_sensor_location_id
from backend_files.plotter import get_pm25_hour_history, get_pm25_week_history


st.set_page_config(
    layout="centered",
    page_title="Krisha.kz Air Quality Report", page_icon="🏠")


def set_background(color):
    hex_color = f'#{color}'
    html = f"""
        <style>
            body {{
                background-color: {hex_color};
            }}
        </style>
    """
    st.markdown(html, unsafe_allow_html=True)


set_background("ffffff")
st.title('Krisha Air Quality Report Generator')
keyword = st.text_input(
    'Paste the link to apartment/house listed on Krisha.kz:', '')


if st.button('Generate Report'):
    if keyword:
        st.image(
            create_apartment_report_from_link(keyword), caption='Airway', use_column_width=True)
        st.title("The history of PM2.5 rating over the last 24 hours")
        st.image(
            get_pm25_hour_history(
                get_sensor_location_id(keyword) + ".png"),
            use_column_width=True)

        st.title("The history of PM2.5 rating over the last week")
        st.image(
            get_pm25_week_history(
                get_sensor_location_id(keyword) + ".png"),
            use_column_width=True)
    else:
        st.text("Please enter a link before generating")
