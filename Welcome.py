import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


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

set_background("f0f0f0")

st.write("# We Help Bring Awareness to Almaty's Air Quality 👋")

st.sidebar.success("Select a demo above.")


st.markdown(
    """
    Select the report generator for Kolesa.kz/Krisha.kz on the LEFT and receive a comprehensive report on vehicle emissions or learn how 
    polluted the area is near the apartment/house
    
    ### Want to learn more about ecological situation in 🍎 Almaty?
    - How dangerous is Almaty's smog - [click](https://tengrinews.kz/kazakhstan_news/naskolko-opasen-almatinskiy-smog-kakie-bolezni-mojet-532004/)
    - How to protect yourself against polluted air? - [click](https://esquire.kz/ways-to-avoid-air-pollution/)
    - Dedicated blog about Almaty's ecology - [click](http://auagroup.kz/vozduh-v-almaty/)
    - Map of Almaty's air quality in real time - [click](https://www.iqair.com/air-quality-map/kazakhstan/almaty-qalasy/almaty)
    ### The project wouldn't be possible if it wasn't for:
    - SERGEK and their datasets
    - Almaty Ecology Challenge Organization Team
"""
)

