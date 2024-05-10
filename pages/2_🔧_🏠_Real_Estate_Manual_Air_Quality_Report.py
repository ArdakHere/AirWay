import streamlit as st
from utils.back_krisha import create_apartment_report_from_manual_input, get_sensor_location_id_from_manual_input
from utils.plotter import get_pm25_hour_history, get_pm25_week_history

st.set_page_config(
    layout="centered",
    page_title="Real Estate Manual Emissions Report",
    page_icon="🔧🏠")

st.write("")
st.title('Генерация Эко Репорта для Недвижимости (Ручной ввод)')

realestate_data = {
    "location": None,
    "area": None,
    "floor": None,
}

realestate_data["location"] = st.text_input(
    'Введите координаты недвижимости (долгота, широта)')


if st.button('Сгенерировать отчет'):
    st.image(
        create_apartment_report_from_manual_input(realestate_data["location"]),
        caption='Airway',
        use_column_width=True)

    hour_history_path = get_pm25_hour_history(
        get_sensor_location_id_from_manual_input(realestate_data["location"]) + ".png")
    st.title("На сколько загрязнен воздух за последние 24 часа (Сильное загрязнение > 90)")
    st.image(hour_history_path, use_column_width=True)

    week_history_path = get_pm25_week_history(
        get_sensor_location_id_from_manual_input(realestate_data["location"]) + ".png")
    st.title("На сколько загрязнен воздух за последнюю неделю (Сильное загрязнение > 90)")
    st.image(week_history_path, use_column_width=True)
