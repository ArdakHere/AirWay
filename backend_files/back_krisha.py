import requests
import re
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from backend_files.plotter import *
from openai import OpenAI

client = OpenAI(api_key="sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP")

def sergek_reader():
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet("/Users/ardaka/Desktop/data_sensor.parquet")

    # Filter relevant columns
    filtered_df = df[['location_id', 'Latitude', 'Longtitude', 'pm25', 'pm10', 'co']]

    # Group the data by location_id and calculate the mean for pm25, pm10, and co
    averages = filtered_df.groupby('location_id').agg({'pm25': 'mean', 'pm10': 'mean', 'co': 'mean'})

    # Merge with the original DataFrame to keep latitude and longitude
    result = pd.merge(averages, filtered_df[['location_id', 'Latitude', 'Longtitude']], on='location_id',
                      how='left').drop_duplicates()

    # Set float format to print full length latitude and longitude
    pd.set_option('display.float_format', lambda x: '%.8f' % x)

    pd.set_option('display.width', 200)
    pd.set_option('display.max_columns', 10)

    # Print the result
    result_str = result.to_string(index=False)
    result_df = pd.DataFrame([x.split() for x in result_str.split('\n')], columns=result.columns)

    return result_df

def gpt_text_generator(data):
    api_key = 'sk-proj-wfFWlYv6WmIRmwCRiGhPT3BlbkFJQ59sSlLRjpHSSYlwykOP'
    endpoint = 'https://api.openai.com/v1/chat/completions'


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Hey! Based on the values of PM2.5, PM10 and CO in the air provide a realestate_report overview of the area of the real estate I am thinking of buying. Also add recommendations on living in the area with polluted air. Write each sentence"
                           "on a new line, and each sentence should be shorter than 7 words, add new lines if the sentence is longer. Don't put periods at the ends of the sentences. "
                           "Explain each value and explain what they mean"
                           "Provide the answer in the following format: "
                           "-PM2.5 rating shows that ... "
                           "..."
                           "-PM10 rating shows that ... "
                           "..."
                           "-CO rating shows that ... "
                           "..."
                           "Recommendations are:"
                           "1."
                           "2."
                           "3."
                           "..."
            },
            {
                "role": "user",
                "content": f"PM2.5 value {data['pm25']}, PM10 value {data['pm10']},"
                           f"CO value: {data['co']}"

            }
        ],
        max_tokens=300
    )

    report = response.choices[0].message.content

    return report

def index_calculator(metrics_data):
    aq_index = 0
    pm25_weight = 0.5
    pm10_weight = 0.3
    co_weight = 0.2

    for key in metrics_data:
        if key == "pm25":
            aq_index = pm25_weight*float(metrics_data[key]) + aq_index
        if key == "pm10":
            aq_index = pm10_weight*float(metrics_data[key]) + aq_index
        if key == "co":
            aq_index = co_weight*float(metrics_data[key]) + aq_index

    color = ""
    color_pm25 = ""
    color_pm10 = ""
    color_co = ""


    if aq_index >= 100: # Orange
        color = [255, 119, 0]
    if aq_index >= 85:   #dark yellow
        color = [255, 189, 55]
    if aq_index >= 45 and aq_index < 85:  # yellow
        color = [255, 224, 18]
    if aq_index < 30:   # dark green
        color = [67, 166, 0]
    if aq_index >= 30 and aq_index < 45: #brighter green
        color = [161, 219, 0]

    ##### pm25 color
    if float(metrics_data["pm25"]) >= 100: # Orange
        color_pm25 = [255, 119, 0]
    if float(metrics_data["pm25"]) >= 85:   #dark yellow
        color_pm25 = [255, 189, 55]
    if float(metrics_data["pm25"]) >= 45 and float(metrics_data["pm25"]) < 85:  # yellow
        color_pm25 = [255, 224, 18]
    if float(metrics_data["pm25"]) < 30:   # dark green
        color_pm25 = [67, 166, 0]
    if float(metrics_data["pm25"]) >= 30 and float(metrics_data["pm25"]) < 45: #brighter green
        color_pm25 = [161, 219, 0]

    ##### pm10 color
    if float(metrics_data["pm10"]) >= 100:  # Orange
        color_pm10 = [255, 119, 0]
    if float(metrics_data["pm10"]) >= 85:  # dark yellow
        color_pm10 = [255, 189, 55]
    if float(metrics_data["pm10"]) >= 45 and aq_index < 85:  # yellow
        color_pm10 = [255, 224, 18]
    if float(metrics_data["pm10"]) < 30:  # dark green
        color_pm10 = [67, 166, 0]
    if float(metrics_data["pm10"]) >= 30 and float(metrics_data["pm10"]) < 45:  # brighter green
        color_pm10 = [161, 219, 0]

    ##### pm10 color
    if float(metrics_data["co"]) >= 100:  # Orange
        color_co = [255, 119, 0]
    if float(metrics_data["co"]) >= 85:  # dark yellow
        color_co = [255, 189, 55]
    if float(metrics_data["co"]) >= 45 and aq_index < 85:  # yellow
        color_co = [255, 224, 18]
    if float(metrics_data["co"]) < 30:  # dark green
        color_co = [67, 166, 0]
    if float(metrics_data["co"]) >= 30 and float(metrics_data["co"]) < 45:  # brighter green
        color_co = [161, 219, 0]

    index_dict = {
        "aq_index_numeric": int(aq_index),
        "aq_index_color": color,
        "color_pm25": color_pm25,
        "color_pm10": color_pm10,
        "color_co": color_co
    }

    return index_dict

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c  # Earth radius in kilometers

    return distance


def find_closest_sensor(sensor_locations, provided_location):
    closest_sensor = None
    min_distance = float('inf')

    for _, sensor_location in sensor_locations.iterrows():

        distance = haversine(float(provided_location['Latitude']), float(provided_location['Longitude']),
                             float(sensor_location['Latitude']), float(sensor_location['Longtitude']))
        if distance < min_distance:
            min_distance = distance
            closest_sensor = sensor_location

    return closest_sensor

## data that has to be collected:
# location, physical data(street, floor number, year of construction, area)
def krisha_html_reader(filename):

    realestate_dict = {
        "location": None,
        "street": None,
        "floor number": None,
        "area": None,
        "room_type": None,
        "year of construction": None,
    }
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
            print("HTML code read successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Location added
    phys_data = get_phys_data(html_content)

    realestate_dict["location"] = get_coordinates(html_content)
    realestate_dict["floor number"] = phys_data["floor number"]
    realestate_dict["street"] = phys_data["street"]
    realestate_dict["area"] = phys_data["area"]
    realestate_dict["room_type"] = phys_data["room_type"]
    realestate_dict["year of construction"] = phys_data["year of construction"]

    return realestate_dict

# TEMPORARY NOT NEEDED
def krisha_html_download(url):

    realestate_dict = {
        "location": None,
        "street": None,
        "floor number": None,
        "area": None,
        "room_type": None,
        "year of construction": None,
    }

    html_content = ""

    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

        # Location added
    phys_data = get_phys_data(html_content)

    realestate_dict["location"] = get_coordinates(html_content)
    realestate_dict["floor number"] = phys_data["floor number"]
    realestate_dict["street"] = phys_data["street"]
    realestate_dict["area"] = phys_data["area"]
    realestate_dict["room_type"] = phys_data["room_type"]
    realestate_dict["year of construction"] = phys_data["year of construction"]

    return realestate_dict


def get_phys_data(data):

    # Define a regular expression pattern to extract the desired data
    pattern = r'(\d+-комнатная квартира), (\d+ м²), (\d+/\d+ этаж), ([^,]+) за'
    pattern_construction_date = r'<div class="offer__info-item" data-name="house.year">.*?<div class="offer__advert-short-info">(\d+)</div>'

    phys_data_dict = {
        "street": None,
        "floor number": None,
        "year of construction": None,
        "area": None,
        "room_type": None
    }
    # Search for the pattern in the text
    match = re.search(pattern_construction_date, data, re.DOTALL)

    if match:
        year = match.group(1)
        phys_data_dict["year of construction"] = year
    else:
        print("Year data not found.")

    # Search for the pattern in the text
    match = re.search(pattern, data)

    if match:
        room_type = match.group(1)
        area = match.group(2)
        floor = match.group(3)
        street = match.group(4)
        phys_data_dict["street"] = street
        phys_data_dict["floor number"] = floor
        phys_data_dict["area"] = area
        phys_data_dict["room_type"] = room_type

    else:
        print("Data not found.")

    return phys_data_dict

def get_coordinates(data):
    pattern = r'"lat":(-?\d+\.\d+),"lon":(-?\d+\.\d+)'
    match = re.search(pattern, data)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        lat_lon_combined = f"{lat},{lon}"
        return lat_lon_combined
    else:
        print("Latitude and longitude data not found.")

def MANUAL_get_sensor_location_id(location):
    sensor_dataframe = sergek_reader()  # Read the SERGEK's dataset

    sensor_locations_df = pd.DataFrame(sensor_dataframe)
    sensor_locations_df = sensor_locations_df.drop(sensor_locations_df.index[0])

    # Provided location
    provided_location = location  # Example provided location
    latitude, longitude = map(float, provided_location.split(','))

    provided_location_dict = {
        "Latitude": latitude,
        "Longitude": longitude
    }

    closest_sensor = find_closest_sensor(sensor_locations_df, provided_location_dict)

    closest_sensor_dict = closest_sensor.to_dict()
    return closest_sensor_dict["location_id"]

def get_sensor_location_id(url):
    sensor_dataframe = sergek_reader()  # Read the SERGEK's dataset
    phys_data = krisha_html_download(url)  # Get coordinates and other physical data

    sensor_locations_df = pd.DataFrame(sensor_dataframe)
    sensor_locations_df = sensor_locations_df.drop(sensor_locations_df.index[0])

    # Provided location
    provided_location = phys_data["location"]  # Example provided location
    latitude, longitude = map(float, provided_location.split(','))

    provided_location_dict = {
        "Latitude": latitude,
        "Longitude": longitude
    }

    closest_sensor = find_closest_sensor(sensor_locations_df, provided_location_dict)

    closest_sensor_dict = closest_sensor.to_dict()

    return closest_sensor_dict["location_id"]

def MANUAL_report_handler(location):
    sensor_dataframe = sergek_reader()  # Read the SERGEK's dataset

    sensor_locations_df = pd.DataFrame(sensor_dataframe)
    sensor_locations_df = sensor_locations_df.drop(sensor_locations_df.index[0])

    # Provided location
    provided_location = location # Example provided location
    latitude, longitude = map(float, provided_location.split(','))

    provided_location_dict = {
        "Latitude": latitude,
        "Longitude": longitude
    }

    closest_sensor = find_closest_sensor(sensor_locations_df, provided_location_dict)

    closest_sensor_dict = closest_sensor.to_dict()

    data_processed = index_calculator(closest_sensor_dict)

    aq_metrics_for_gpt_report = {
        "pm25": closest_sensor_dict['pm25'],
        "pm10": closest_sensor_dict['pm10'],
        "co": closest_sensor_dict['co']
    }

    data_processed.update({'pm25': int(float(closest_sensor_dict['pm25']))})
    data_processed.update({'pm10': int(float(closest_sensor_dict['pm10']))})
    data_processed.update({'co': int(float(closest_sensor_dict['co']))})

    data_processed.update({"realestate_report": gpt_text_generator(aq_metrics_for_gpt_report)})

    return generate_report_for_an_apartment(int(data_processed["aq_index_numeric"]),
                                            data_processed["aq_index_color"],
                                            data_processed["color_pm25"],
                                            data_processed["color_pm10"],
                                            data_processed["color_co"],
                                            data_processed["pm25"],
                                            data_processed["pm10"],
                                            data_processed["co"],
                                            data_processed["realestate_report"])

def report_handler(url):
    sensor_dataframe = sergek_reader()  # Read the SERGEK's dataset
    phys_data = krisha_html_download(url)  # Get coordinates and other physical data

    sensor_locations_df = pd.DataFrame(sensor_dataframe)
    sensor_locations_df = sensor_locations_df.drop(sensor_locations_df.index[0])

    # Provided location
    provided_location = phys_data["location"] # Example provided location
    latitude, longitude = map(float, provided_location.split(','))

    provided_location_dict = {
        "Latitude": latitude,
        "Longitude": longitude
    }

    closest_sensor = find_closest_sensor(sensor_locations_df, provided_location_dict)

    closest_sensor_dict = closest_sensor.to_dict()

    data_processed = index_calculator(closest_sensor_dict)

    aq_metrics_for_gpt_report = {
        "pm25": closest_sensor_dict['pm25'],
        "pm10": closest_sensor_dict['pm10'],
        "co": closest_sensor_dict['co']
    }

    data_processed.update({'pm25': int(float(closest_sensor_dict['pm25']))})
    data_processed.update({'pm10': int(float(closest_sensor_dict['pm10']))})
    data_processed.update({'co': int(float(closest_sensor_dict['co']))})

    data_processed.update({"realestate_report": gpt_text_generator(aq_metrics_for_gpt_report)})

    return generate_report_for_an_apartment(int(data_processed["aq_index_numeric"]),
                                            data_processed["aq_index_color"],
                                            data_processed["color_pm25"],
                                            data_processed["color_pm10"],
                                            data_processed["color_co"],
                                            data_processed["pm25"],
                                            data_processed["pm10"],
                                            data_processed["co"],
                                            data_processed["realestate_report"])

def temp_func():
    sensor_dataframe = sergek_reader()   # Read the SERGEK's dataset
    phys_data = krisha_html_reader("../dummy_files_for_testing/apartment.txt")    # Get coordinates and other physical data

    sensor_locations_df = pd.DataFrame(sensor_dataframe)
    sensor_locations_df = sensor_locations_df.drop(sensor_locations_df.index[0])
    # Provided location
    provided_location = phys_data["location"]  # Example provided location
    latitude, longitude = map(float, provided_location.split(','))

    provided_location_dict = {
        "Latitude": latitude,
        "Longitude": longitude
    }

    closest_sensor = find_closest_sensor(sensor_locations_df, provided_location_dict)

    closest_sensor_dict = closest_sensor.to_dict()

    data_processed = index_calculator(closest_sensor_dict)

    aq_metrics_for_gpt_report = {
        "pm25": int(float(closest_sensor_dict['pm25'])),
        "pm10": int(float(closest_sensor_dict['pm10'])),
        "co": int(float(closest_sensor_dict['co']))
    }

    data_processed.update({'pm25': int(float(closest_sensor_dict['pm25']))})
    data_processed.update({'pm10': int(float(closest_sensor_dict['pm10']))})
    data_processed.update({'co': int(float(closest_sensor_dict['co']))})

    data_processed.update({"realestate_report": gpt_text_generator(aq_metrics_for_gpt_report)})

    return generate_report_for_an_apartment(int(data_processed["aq_index_numeric"]), data_processed["aq_index_color"], data_processed["color_pm25"],
                                            data_processed["color_pm10"], data_processed["color_co"], data_processed["pm25"],
                                            data_processed["pm10"], data_processed["co"], data_processed["realestate_report"])
