import streamlit as st


st.set_page_config(
    layout="centered",
    page_title="Car Manual Emissions Report",
    page_icon="🔧🛞")

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
car_data["generation"] = st.text_input(
    'Enter the generation or a production year')
car_data["engine_displacement"] = st.text_input(
    'Enter the engine displacement')
car_data["distance run (km)"] = st.text_input(
    'Enter the mileage (km)')
car_data["N-wheel drive"] = st.text_input(
    'Enter the wheel drive configuration')

if st.button('Generate Report'):

    # solution to circular import, if removed the error will reappear
    from utils.plotter import generate_report_for_a_car

    st.image(
        generate_report_for_a_car(
            car_data["car_title"],
            car_data["generation"],
            car_data["engine_displacement"],
            car_data["distance run (km)"],
            car_data["N-wheel drive"]),
        caption='Airway',
        use_column_width=True)
