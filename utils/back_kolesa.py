import csv
import re
import requests
from translate import Translator
from openai import OpenAI


client = None  # Define client outside the function

def define_openAI_client_with_key_kolesa(key: str):

    global client  # Use the global keyword to modify the global variable inside the function
    client = OpenAI(api_key=key)


def get_car_recommendations(price: int) -> str:
    non_ev_recommendations = []
    ev_recommendations = []

    # Open the CSV file
    with open('./assets/datasets/car_dataset.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV file
        for row in reader:
            car_price = int(row['price (KZT)'])
            car_brand = row['brand']
            car_model = row['model']
            car_type = row['type']

            # Check if the car price is within the desired range
            if int(price) - 1200000 <= car_price <= int(price) + 1200000:
                # Check if it's an electric or non-electric car
                if car_type == 'non-ev':
                    if len(non_ev_recommendations) < 2:
                        non_ev_recommendations.append(f"{car_brand} {car_model} - {car_price:,} KZT")
                elif car_type == 'ev':
                    if len(ev_recommendations) < 2:
                        ev_recommendations.append(f"{car_brand} {car_model} - {car_price:,} KZT")

            # Break if we have found at least 2 recommendations for both non-ev and ev cars
            if len(non_ev_recommendations) >= 2 and len(ev_recommendations) >= 2:
                break

    # Format the recommendations
    non_ev_recommendations_str = "\n".join(non_ev_recommendations)
    ev_recommendations_str = "\n".join(ev_recommendations)

    # Combine non-ev and ev recommendations into a single string
    recommendations_str = f"Non-Electric Cars:\n{non_ev_recommendations_str}\n\nElectric Cars:\n{ev_recommendations_str}"

    return recommendations_str

def read_remote_kolesa_page(html_car_data: str) -> dict:
    car_info = {
        "car_title": None,
        "generation": None,
        "engine_displacement": None,
        "distance run (km)": None,
        "N-wheel drive": None,
        "price": None,
    }

    # Extracting unitPrice from JavaScript object in HTML data
    match = re.search(r"\"unitPrice\":\s*(\d+\.?\d*)", html_car_data)

    if match:
        car_info["price"] = match.group(1)
        print("Unit Price:", car_info["price"])
    else:
        print("No unit price found in the HTML.")


    # Extracting other car information from HTML
    pattern = r'<dt class="value-title" title="(.*?)">.*?<dd class="value">(.*?)</dd>'
    matches = re.findall(pattern, html_car_data, re.DOTALL)
    for match in matches:
        title = match[0]
        value = match[1]
        if title == "Поколение":
            car_info["generation"] = value.strip()
        elif title == "Объем двигателя, л":
            car_info["engine_displacement"] = value.strip()
        elif title == "Пробег":
            car_info["distance run (km)"] = value.strip()
        elif title == "Привод":
            car_info["N-wheel drive"] = value.strip()

    name_pattern = r'"name":"(.*?)"'
    name_match = re.search(name_pattern, html_car_data)
    if name_match:
        car_info["car_title"] = name_match.group(1)
        car_info["car_title"] = car_info["car_title"].split(' г.')[0]

    # Translating car information
    translator = Translator(to_lang="en", from_lang="ru")
    for key, value in car_info.items():
        if value is not None:
            car_info[key] = translator.translate(value)

    return car_info


def extract_co2_emissions(co2_emissions_str):
    # Use regular expression to extract the numeric value
    match = re.search(r'\b(\d+(\.\d+)?)(?:-(\d+(\.\d+)?))?\s*g', co2_emissions_str, re.IGNORECASE)
    if match:
        # Extract the matched numeric values
        emissions_start = float(match.group(1))
        print(emissions_start)
        return int(emissions_start)
    else:
        return None  # Return None if no match is found

def extract_gas_mileage(gas_mileage_str):
    # Use regular expression to extract the numeric value
    match = re.search(r'\b(\d+(\.\d+)?)(?:\s*-\s*(\d+(\.\d+)?))?\s*[lLgG]', gas_mileage_str, re.IGNORECASE)

    if match:
        # Extract the matched numeric values
        mileage_start = float(match.group(1))
        print(mileage_start)
        return int(mileage_start)
    else:
        return None  # Return None if no match is found


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
                           "on a new line, and each recommendation should be shorter than 7 words, add new line characters if the sentence is longer. Limit to maximum of 5 recommendations"
                           "Don't put periods at the ends of the sentences. START EACH RECOMMENDATION FROM THE NEWLINE"
                           "Provide the answer in the following format and do not use words such as approximately, just give the number: "
                           "Gas expenditure is equal to"
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
        elif line.startswith("Gas expenditure"):
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
