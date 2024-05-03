import re

import requests
from translate import Translator
import os
from openai import OpenAI

# apikey ChatGPT sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP,   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
# apikey GeminiAI AIzaSyAoDDOARP81gR1X8AGA82YKE8sXlzuVTJk

client = OpenAI(api_key="sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP")
kolesa_data = ""

def gpt_metrics_caller(data):
    api_key = 'sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP'

    endpoint = 'https://api.openai.com/v1/chat/completions'

    prompt = ("Hey! I need you help with getting all the information related to emissions rating of the following car"
              "and its eco-friendliness")

    additional_data = {
        "car_title": data["car_title"],
        "generation": data["generation"],
        "engine_displacement": data["engine_displacement"],
        "distance run (km)": data["distance run (km)"],
        "N-wheel drive": data["N-wheel drive"],
    }

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Hey! I am going to provide a data on a car and I want you to provide the values of CO2, NOx, SO2 and PM2.5 "
                           "that the car emits when driving. You may not know the exact numbers, in this case provide approximate values "
                           " Then, provide recommendations based on the values and the car related data that I will provide. Write each recommendation"
                           "on a new line, and each recommendation should be shorter than 7 words, add new lines if the sentence is longer. "
                           "Don't put periods at the ends of the sentences. "
                           "..."
                           "Provide the answer in the following format: "
                           "CO2 is equal to"
                           "NOx is equal to"
                           "SO2 is equal to"
                           "PM2.5 is equal to"
                           "..."
                           "Recommendations: are"
                           "1."
                           "2."
                           "3."
                           "..."
            },
            {
                "role": "user",
                "content": f"Car brand and model: {additional_data['car_title']}, Model generation: {additional_data['generation']}."
                           f"Engine displacement: {additional_data['engine_displacement']}, N-wheel drive: {additional_data['N-wheel drive']}"
                           f"Mileage (km): {additional_data['distance run (km)']}"

            }
        ],
        max_tokens=300
    )

    report = response.choices[0].message.content

    lines = report.split("\n")

    # Extracting emissions values
    emissions_values = {}
    for line in lines:
        if line.startswith("CO2"):
            key, value = line.split("is equal to")
            emissions_values[key.strip()] = value.strip()
        elif line.startswith("NOx"):
            key, value = line.split("is equal to")
            emissions_values[key.strip()] = value.strip()
        elif line.startswith("SO2"):
            key, value = line.split("is equal to")
            emissions_values[key.strip()] = value.strip()
        elif line.startswith("PM2.5"):
            key, value = line.split("is equal to")
            emissions_values[key.strip()] = value.strip()

    # Extracting recommendations
    recommendations = ""
    recommendations_started = False
    for line in lines:
        if recommendations_started:
            recommendations += line.strip()
        if line == "Recommendations:":
            recommendations_started = True

    return emissions_values, recommendations

def gpt_caller(data):
    # Supply the car name and ask for emissions and other stuff

    api_key = 'sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP'
    endpoint = 'https://api.openai.com/v1/chat/completions'

    prompt = ("Hey! I need you help with getting all the information related to emissions rating of the following car"
              "and its eco-friendliness")

    additional_data = {
        "car_title": data["car_title"],
        "generation": data["generation"],
        "engine_displacement": data["engine_displacement"],
        "distance run (km)": data["distance run (km)"],
        "N-wheel drive": data["N-wheel drive"],
    }


    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Hey! I am going to provide a data on a car and I want you to rate how safe for ecology it is on a scale 0-10 and find the CO2 emissions number."
                           " Then, explain what do these numbers and ratings mean. "
                           "Provide the asnwer in the following format: "
                           "- The N car is 5/10 in terms of it impact on ecology/air "
                           "- The N car has a X CO2 emissions number"
                           "- This information shows that this car is ..."
            },
            {
                "role": "user",
                "content": f"Car brand and model: {additional_data['car_title']}, Model generation: {additional_data['generation']}."
                        f"Engine displacement: {additional_data['engine_displacement']}, N-wheel drive: {additional_data['N-wheel drive']}"
                           f"Mileage (km): {additional_data['distance run (km)']}"


            }
        ],
        max_tokens=300
    )


    report = response.choices[0].message.content

    return report


##########################################################################################
##########################################################################################
##########################################################################################

def kolesa_html_reader_file(filename):
    car_dict = {
        "car_title": None,
        "generation": None,
        "engine_displacement": None,
        "distance run (km)": None,
        "N-wheel drive": None,
    }

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"An error occurred: {e}")


    pattern = r'<dt class="value-title" title="(.*?)">.*?<dd class="value">(.*?)</dd>'

    matches = re.findall(pattern, html_content, re.DOTALL)

    data = {}

    for match in matches:
        title = match[0]
        value = match[1]
        if title == "Поколение":
            car_dict["generation"] = value.strip()
        if title == "Объем двигателя, л":
            car_dict["engine_displacement"] = value.strip()
        if title == "Пробег":
            car_dict["distance run (km)"] = value.strip()
        if title == "Привод":
            car_dict["N-wheel drive"] = value.strip()

    name_pattern = r'"name":"(.*?)"'
    name_match = re.search(name_pattern, html_content)
    if name_match:
        car_dict["car_title"] = name_match.group(1)

        # Extract only the model name
        car_dict["car_title"] = car_dict["car_title"].split(' г.')[0]

    translator = Translator(to_lang="en", from_lang="ru")  # Translate to English, auto-detect input language
    i = 0
    for key, value in car_dict.items():
        # Translate each key and value
        if i == 0:
            i = i + 1
        else:
            if value != None:
                car_dict[key] = translator.translate(value)

    return car_dict


##########################################################################################
##########################################################################################
##########################################################################################


def kolesa_html_reader(car_data):
    car_dict = {
        "car_title": None,
        "generation": None,
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
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


