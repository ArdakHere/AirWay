import streamlit as st

from back_kolesa import kolesa_html_download, kolesa_html_reader, gpt_caller
st.set_page_config(layout="centered", page_title="Kolesa.kz Emissions Report", page_icon="🛞")

st.title('Kolesa Ecology Report Generator')


keyword = st.text_input('Paste the link to apartment/house/car listed on Kolesa.kz:', '')

# Button to trigger the action
if st.button('Generate Report'):
    # Check if keyword is not empty
    if keyword:
        # Download HTML content and display it
        html_code = kolesa_html_download(keyword)
        car_data = kolesa_html_reader(html_code)
        report = gpt_caller(car_data)

        if report:
            # Display HTML content with taller st.text
            st.text_area(label="Report", value=report, height=500, max_chars=None, key=None)


else:
    st.text("Please enter a link before generating the report.")

