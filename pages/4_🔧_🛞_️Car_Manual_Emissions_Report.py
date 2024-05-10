import streamlit as st


st.set_page_config(
    layout="centered",
    page_title="Car Manual Emissions Report",
    page_icon="🔧🛞")

st.write("")
st.title('Генерация Эко Репорта для Автомобиля (Ручной ввод)')
car_data = {
    "car_title": None,
    "generation": None,
    "engine_displacement": None,
    "distance run (km)": None,
    "N-wheel drive": None,
    "price": None
}
car_data["car_title"] = st.text_input('Введите название автомобиля')
car_data["generation"] = st.text_input(
    'Введите поколение или год выпуска автомобиля')
car_data["engine_displacement"] = st.text_input(
    'Введите объем двигателя (л)')
car_data["distance run (km)"] = st.text_input(
    'Введите пробег (км)')
car_data["N-wheel drive"] = st.text_input(
    'Введите привод автомобиля (4WD, 2WD, AWD, FWD)')
car_data["price"] = st.text_input(
    'Введите примерную цену в тенге')



if st.button('Сгенерировать отчет'):

    # solution to circular import, if removed the error will reappear
    from utils.plotter import generate_report_for_a_car

    st.image(
        generate_report_for_a_car(
            car_data["car_title"],
            car_data["generation"],
            car_data["engine_displacement"],
            car_data["distance run (km)"],
            car_data["N-wheel drive"],
            car_data["price"]),
        caption='Airway',
        use_column_width=True)
