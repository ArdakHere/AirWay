import re
import requests
from translate import Translator
from openai import OpenAI


client = OpenAI(
    api_key="")


def request_metrics_and_recommendations(
    car_metric_data: dict
) -> tuple[dict, str]:
    """_summary_

    Args:
        car_metric_data (dict): metrics from kolesa page

    Returns:
        tuple[dict, str]: dict: emissions values, str: recommendations
    """
    report_data = {
        "car_title": car_metric_data["car_title"],
        "generation": car_metric_data["generation"],
        "engine_displacement": car_metric_data["engine_displacement"],
        "distance run (km)": car_metric_data["distance run (km)"],
        "N-wheel drive": car_metric_data["N-wheel drive"],
    }

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Hey! I am going to provide a data on a car and I want you to provide the values of CO2, NOx, SO2 and PM2.5 "
                           "that the car emits when driving. You may not know the exact numbers, in this case provide approximate values "
                           " Then, provide recommendations below based on the values and the car related data that I will provide. Write each recommendation"
                           "on a new line, and each recommendation should be shorter than 7 words, add new line characters if the sentence is longer. Limit to maximum of 10 recommendations"
                           "Don't put periods at the ends of the sentences. START EACH RECOMMENDATION FROM THE NEWLINE"
                           "Provide the answer in the following format: "
                           "CO2 is equal to"
                           "NOx is equal to"
                           "SO2 is equal to"
                           "PM2.5 is equal to"
                           "Recommendations:"
                           "1."
                           "2."
                           "3."
            },
            {
                "role": "user",
                "content": f"Car brand and model: {report_data['car_title']}, Model generation: {report_data['generation']}."
                           f"Engine displacement: {report_data['engine_displacement']}, N-wheel drive: {report_data['N-wheel drive']}"
                           f"Mileage (km): {report_data['distance run (km)']}"
            }
        ],
        max_tokens=300
    )
    report = response.choices[0].message.content
    lines = report.split("\n")

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

    recommendations = ""
    recommendations_started = False
    for line in lines:
        if recommendations_started:
            recommendations += line.strip()
        if line == "Recommendations:":
            recommendations_started = True

    return emissions_values, recommendations


def read_local_kolesa_page(filepath: str) -> dict:
    """
    Reads the HTML file and extracts the necessary data from it

    Args:
    filepath (str): path to the HTML file

    Returns:
    dict: extracted data
    """
    car_info = {
        "car_title": None,
        "generation": None,
        "engine_displacement": None,
        "distance run (km)": None,
        "N-wheel drive": None,
    }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"An error occurred: {e}")

    pattern = r'<dt class="value-title" title="(.*?)">.*?<dd class="value">(.*?)</dd>'
    matches = re.findall(pattern, html_content, re.DOTALL)

    for match in matches:
        title = match[0]
        value = match[1]
        if title == "Поколение":
            car_info["generation"] = value.strip()
        if title == "Объем двигателя, л":
            car_info["engine_displacement"] = value.strip()
        if title == "Пробег":
            car_info["distance run (km)"] = value.strip()
        if title == "Привод":
            car_info["N-wheel drive"] = value.strip()

    name_pattern = r'"name":"(.*?)"'
    name_match = re.search(name_pattern, html_content)
    if name_match:
        car_info["car_title"] = name_match.group(1)
        car_info["car_title"] = car_info["car_title"].split(' г.')[0]

    translator = Translator(
        to_lang="en",
        from_lang="ru")
    i = 0
    for key, value in car_info.items():
        if i == 0:
            i = i + 1
        else:
            if value is not None:
                car_info[key] = translator.translate(value)
    return car_info


def read_remote_kolesa_page(html_car_data: str) -> dict:
    car_info = {
        "car_title": None,
        "generation": None,
        "engine_displacement": None,
        "distance run (km)": None,
        "N-wheel drive": None,
    }

    pattern = r'<dt class="value-title" title="(.*?)">.*?<dd class="value">(.*?)</dd>'
    matches = re.findall(pattern, html_car_data, re.DOTALL)
    data = {}
    for match in matches:
        title = match[0]
        value = match[1]
        if title == "Поколение":
            car_info["generation"] = value.strip()
        if title == "Объем двигателя, л":
            car_info["engine_displacement"] = value.strip()
        if title == "Пробег":
            car_info["distance run (km)"] = value.strip()
        if title == "Привод":
            car_info["N-wheel drive"] = value.strip()

    name_pattern = r'"name":"(.*?)"'
    name_match = re.search(name_pattern, html_car_data)
    if name_match:
        car_info["car_title"] = name_match.group(1)
        car_info["car_title"] = car_info["car_title"].split(' г.')[0]

    for key, value in zip(list(car_info.keys())[1:], data.values()):
        car_info[key] = value

    translator = Translator(to_lang="en", from_lang="ru")
    i = 0
    for key, value in car_info.items():
        if i == 0:
            i = i + 1
        else:
            if value is not None:
                car_info[key] = translator.translate(value)
    return car_info


def download_car_webpage(url: str) -> str | None:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
