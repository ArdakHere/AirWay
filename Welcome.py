from utils.back_krisha import define_openAI_client_with_key_krisha
from utils.plotter import define_two_gis_key
from utils.back_kolesa import define_openAI_client_with_key_kolesa

from utils.plotter import *

openai_api_key = input("Enter your ChatGPT API key: ")
gis_api_key = input("Enter your 2GIS API key: ")

define_openAI_client_with_key_krisha(openai_api_key)
define_openAI_client_with_key_kolesa(openai_api_key)
define_two_gis_key(gis_api_key)

import streamlit as st
from utils.change_background_color import *

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

set_background("f0f0f0")

st.write("# We Help Bring Awareness to Almaty's Air Quality 👋")
st.sidebar.success("Select a demo above.")


st.markdown(
    """
    Select the report generator for Kolesa.kz/Krisha.kz on the LEFT and receive a comprehensive on vehicle emissions or learn how 
    polluted the area is near the apartment/house

    ### Want to learn more about ecological situation in 🍎 Almaty?
    - How is Air Quality measured? - [click](https://www.unep.org/news-and-stories/story/how-air-quality-measured)
    - How dangerous is Almaty's smog - [click](https://tengrinews.kz/kazakhstan_news/naskolko-opasen-almatinskiy-smog-kakie-bolezni-mojet-532004/)
    - How to protect yourself against polluted air? - [click](https://esquire.kz/ways-to-avoid-air-pollution/)
    - Dedicated blog about Almaty's ecology - [click](http://auagroup.kz/vozduh-v-almaty/)
    - Map of Almaty's air quality in real time - [click](https://www.iqair.com/air-quality-map/kazakhstan/almaty-qalasy/almaty)
    ### The project wouldn't be possible if it wasn't for:
    - SERGEK and their datasets
    - Almaty Ecology Challenge Organization Team
"""
)
