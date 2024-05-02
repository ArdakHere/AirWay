import re

import requests
from translate import Translator
import os
from openai import OpenAI
import json
from plotter import *

# apikey ChatGPT sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP,   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
# apikey GeminiAI AIzaSyAoDDOARP81gR1X8AGA82YKE8sXlzuVTJk

client = OpenAI(api_key="sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP")
kolesa_data = ""

def gpt_caller(data):
    # Supply the car name and ask for emissions and other stuff
    # try:
    #     api_key = 'sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP'
    #     endpoint = 'https://api.openai.com/v1/chat/completions'

    #     prompt = ("Hey! I need you help with getting all the information related to emissions rating of the following car"
    #             "and its eco-friendliness")

    #     additional_data = {
    #         "car_title": data["car_title"],
    #         "generation": data["generation"],
    #         "engine_displacement": data["engine_displacement"],
    #         "distance run (km)": data["distance run (km)"],
    #         "N-wheel drive": data["N-wheel drive"],
    #     }


    #     response = client.chat.completions.create(
    #         model="gpt-4",
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": "Hey! I am going to provide a data on a car and I want you to rate how safe for ecology it is on a scale 0-10 and find the CO2 emissions number."
    #                             "If it is not possible to find the exact number, please provide an approximate value. Also, please provide the PM2.5 and PM10 emissions in the same format."
    #                         " Do not return anything else in the response, only provide the answer in the following format without any explanation text of fields. Only this struct: "
    #                         """ {
    #                                 "impact": "5/10",
    #                                 "recommendation": "some recommendation text here",
    #                                 "trees_killed": 11,
    #                                 "chemicals": {
    #                                     "co": 30,
    #                                     "no": 10,
    #                                     "so2": 5,
    #                                     "pm25": 5,
    #                             }"""
    #             },
    #             {
    #                 "role": "user",
    #                 "content": f"Car brand and model: {additional_data['car_title']}, Model generation: {additional_data['generation']}."
    #                         f"Engine displacement: {additional_data['engine_displacement']}, N-wheel drive: {additional_data['N-wheel drive']}"
    #                         f"Mileage (km): {additional_data['distance run (km)']}"


    #             }
    #         ],
    #         max_tokens=300
    #     )


    #     raw_report = response.choices[0].message.content

    #     encoded_report = json.loads(raw_report)

    #     return encoded_report
    # except Exception as e:
        return {
            "impact": "5/10",
            "recommendation": "Regular maintenance and tuning can improve fuel efficiency and reduce emissions. Consider using public transport, carpooling, or switching to electric vehicles to reduce emissions further.",
            "trees_killed": 11,
            "chemicals": {
                "co": 30,
                "no": 10,
                "so2": 5,
                "pm25": 5,
            },
        }



##########################################################################################
##########################################################################################
##########################################################################################

def kolesa_html_reader_file(filename):
    car_dict = {
        "car_title": None,
        "city": None,
        "generation": None,
        "body_type": None,
        "engine_displacement": None,
        "distance run (km)": None,
        "N-wheel drive": None,
    }

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
            print("HTML code read successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


    pattern = r'<dt class="value-title" title="(.*?)">.*?<dd class="value">(.*?)</dd>'

    matches = re.findall(pattern, html_content, re.DOTALL)

    data = {}

    for match in matches:
        title = match[0]
        value = match[1]
        data[title] = value.strip()                 ### Fix the problem when certain fields are not given and mess up the structure
                                                        ### of the car_dict

    name_pattern = r'"name":"(.*?)"'
    name_match = re.search(name_pattern, html_content)
    if name_match:
        car_dict["car_title"] = name_match.group(1)

        # Extract only the model name
        car_dict["car_title"] = car_dict["car_title"].split(' г.')[0]

    for key, value in zip(list(car_dict.keys())[1:], data.values()):

        car_dict[key] = value


    translator = Translator(to_lang="en", from_lang="ru")  # Translate to English, auto-detect input language
    i = 0
    for key, value in car_dict.items():
        # Translate each key and value
        if i == 0:
            i = i + 1
        else:
            if value != None:
                car_dict[key] = translator.translate(value)



##########################################################################################
##########################################################################################
##########################################################################################


def kolesa_html_reader(car_data):
    car_dict = {
        "car_title": None,
        "city": None,
        "generation": None,
        "body_type": None,
        "engine_displacement": None,
        "distance run (km)": None,  ## Mileage HAS to be specified
        "N-wheel drive": None,
    }


    pattern = r'<dt class="value-title" title="(.*?)">.*?<dd class="value">(.*?)</dd>'

    matches = re.findall(pattern, car_data, re.DOTALL)

    data = {}

    # Iterate over matches and store data in the dictionary
    for match in matches:
        title = match[0]
        value = match[1]
        data[title] = value.strip()



    # Print extracted data for the specified fields
    # print(data.values())
    name_pattern = r'"name":"(.*?)"'
    name_match = re.search(name_pattern, car_data)
    if name_match:
        car_dict["car_title"] = name_match.group(1)

        # Extract only the model name
        car_dict["car_title"] = car_dict["car_title"].split(' г.')[0]

    for key, value in zip(list(car_dict.keys())[1:], data.values()):
        car_dict[key] = value

    translator = Translator(to_lang="en", from_lang="ru")  # Translate to English, auto-detect input language
    i = 0


    for key, value in car_dict.items():
        # Translate each key and value
        if i == 0:
            i = i + 1
        else:
            car_dict[key] = translator.translate(value)

    return car_dict

def kolesa_html_download(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



##kolesa_html_download("https://kolesa.kz/a/show/169295605")

#kolesa_html_reader_file("car.txt")
