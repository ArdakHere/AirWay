import streamlit as st
from utils.back_krisha import *
from utils.plotter import get_pm25_hour_history, get_pm25_week_history


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
st.title('Генерация Эко Репорта для Квартиры (Krisha.kz)')
keyword = st.text_input(
    'Введите ссылку на объявление Krisha.kz:', '')


if st.button('Generate Report'):
    if keyword:

        apartment_info = download_apartment_webpage(keyword)

        st.markdown("""
                    <style>
                        .button-container {
                            display: flex;
                            flex-direction: row;
                            justify-content: center;
                        }
                        .stButton {
                            scale: 1.2;
                            margin-left: 320px;
                            justify-content: center;
                        }
                    </style>
                """, unsafe_allow_html=True)

        # Display buttons in a row
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("Связаться с продавцом"):
            pass  # Perform action when button is clicked
        if st.button("Посчитать кредит"):
            pass  # Perform action when button is clicked
        st.markdown('</div>', unsafe_allow_html=True)

        st.image(
            create_apartment_report_from_link(keyword), caption='Airway', use_column_width=True)
        st.title("На сколько загрязнен воздух за последние 24 часа (Сильное загрязнение > 90)")
        st.image(
            get_pm25_hour_history(
                get_sensor_location_id(keyword) + ".png"),
            use_column_width=True)

        st.title("На сколько загрязнен воздух за последнюю неделю (Сильное загрязнение > 90)")
        st.image(
            get_pm25_week_history(
                get_sensor_location_id(keyword) + ".png"),
            use_column_width=True)
    else:
        st.text("Введите ссылку для генерации отчета")
