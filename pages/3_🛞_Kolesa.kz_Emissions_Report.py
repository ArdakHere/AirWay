import streamlit as st

from utils.back_kolesa import download_car_webpage, read_remote_kolesa_page


st.set_page_config(
    layout="centered",
    page_title="Kolesa.kz Emissions Report",
    page_icon="🛞")

st.title('Kolesa Ecology Report Generator')
kolesa_link = st.text_input(
    'Paste the link to apartment/house/car listed on Kolesa.kz:', '')



if st.button('Generate Report'):


    if kolesa_link:
        link_html_code = download_car_webpage(kolesa_link)
        car_data = read_remote_kolesa_page(link_html_code)

        # solution to circular import, if removed the error will reappear
        from utils.plotter import generate_report_for_a_car

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
        if st.button("Contact Seller"):
            pass  # Perform action when button is clicked
        if st.button("Calculate Credit"):
            pass  # Perform action when button is clicked
        st.markdown('</div>', unsafe_allow_html=True)

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

else:
    st.text("Please enter a link before generating the car report.")
