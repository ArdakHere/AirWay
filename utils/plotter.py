from PIL import Image, ImageFont, ImageDraw
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from utils.back_krisha import *
from utils.back_kolesa import *
import os
import re


APARTMENT_IMAGE_PATH = "./assets/img/template_for_reports/apartmentReportTemplate.png"
CAR_IMAGE_PATH = "./assets/img/template_for_reports/carReportTemplate.png"
PICTOGRAMS_PATH = "./assets/img/icons_for_report/"


def get_pm25_hour_history(sensor_name: str) -> str | None:
    """Get the path to the hourly PM2.5 history graph with the given filename.

    Args:
        filename (str): The name of the file to find."""
    folder = "./assets/pm25_history_graphs/hour_pm25_history/"
    file_path = folder + sensor_name
    if os.path.exists(file_path):
        print(f"Found file: {file_path}")
        return file_path
    else:
        print(f"File not found: {file_path}")
        return None


def get_pm25_week_history(filename: str) -> str | None:
    """Get the path to the weekly PM2.5 history graph with the given filename.

    Args:
        filename (str): The name of the file to find.

    Returns:
        str | None: The path to the file if it exists, otherwise None."""
    folder = "./assets/pm25_history_graphs/week_pm25_history/"
    file_path = folder + filename
    if os.path.exists(file_path):
        print(f"Found file: {file_path}")
        return file_path
    else:
        print(f"File not found: {file_path}")
        return None


def generate_report_for_an_apartment(
    latitude: float,
    longitude: float,
    aqIndex: int,
    aqIndexColor: list,
    pm25Color: list,
    pm10Color: list,
    coColor: list,
    pm25: int,
    pm10: int,
    co: int,
    text: str
) -> str:
    """
    Generate a report for an apartment with the given metrics and text.

    Args:
        aqIndex (int): The Air Quality Index.
        aqIndexColor (list): The color for the Air Quality Index.
        pm25Color (list): The color for the PM2.5.
        pm10Color (list): The color for the PM10.
        coColor (list): The color for the CO.
        pm25 (int): The PM2.5 value.
        pm10 (int): The PM10 value.
        co (int): The CO value.
        text (str): The text to include in the report.

    Returns:
        str: The path to the saved report."""

    # try:
    #     template = Image.open(APARTMENT_IMAGE_PATH)
    #     drawCertificate = ImageDraw.Draw(template)
    # except Exception:
    #     pass
    print(latitude)
    print(longitude)
    template = Image.open(APARTMENT_IMAGE_PATH)
    drawCertificate = ImageDraw.Draw(template)


    R, G, B = aqIndexColor[0], aqIndexColor[1], aqIndexColor[2]
    Rpm25, Gpm25, Bpm25 = pm25Color[0], pm25Color[1], pm25Color[2]
    Rpm10, Gpm10, Bpm10 = pm10Color[0], pm10Color[1], pm10Color[2]
    Rco, Gco, Bco = coColor[0], coColor[1], coColor[2]
    pm25Pic = Image.open(PICTOGRAMS_PATH + "pm25.png")
    pm10Pic = Image.open(PICTOGRAMS_PATH + "pm10.png")
    coPic = Image.open(PICTOGRAMS_PATH + "co.png")
    pathToSave = "./assets/reports/realestate_report/realestate_report.png"
    pathToPdf = "./assets/reports/realestate_report/realestate_report_pdf"
    metricFont = ImageFont.truetype('./assets/font/FreeMono.ttf', 90)
    aqFont = ImageFont.truetype('./assets/font/FreeMono.ttf', 110)
    labelFont = ImageFont.truetype('./assets/font/FreeMonoBold.ttf', 60)
    textFont = ImageFont.truetype('./assets/font/FreeMonoBold.ttf', 40)
    indexWarnFont = ImageFont.truetype('./assets/font/FreeMonoBold.ttf', 95)

    drawCertificate.text(
        (270, 280),
        "How polluted the air is?",
        font=labelFont,
        fill=(0, 0, 0))
    drawCertificate.text((125, 550), "Concentration of harmful particles", font=labelFont, fill=(0, 0, 0))

    if aqIndex <= 40:
        emoji_image = Image.open("./assets/img/icons_for_report/emojis/star_eyes_emoji.png")
        emoji_width = int(emoji_image.width * 0.2)
        emoji_height = int(emoji_image.height * 0.2)
        emoji_image.thumbnail((emoji_width, emoji_height))
        template.paste(emoji_image, (630, 370))
        drawCertificate.text((450, 630), "Minimal, air is clean", font=indexWarnFont, fill=(Rpm25, Gpm25, Bpm25))
    if 50 >= aqIndex > 40:
        emoji_image = Image.open("./assets/img/icons_for_report/emojis/slighty_smiling_emoji.png")
        emoji_width = int(emoji_image.width * 0.2)
        emoji_height = int(emoji_image.height * 0.2)
        emoji_image.thumbnail((emoji_width, emoji_height))
        template.paste(emoji_image, (630, 370))

        drawCertificate.text((450, 630), "Doesn't pose risk", font=indexWarnFont, fill=(Rpm25, Gpm25, Bpm25))
    if 70 >= aqIndex > 50:
        emoji_image = Image.open("./assets/img/icons_for_report/emojis/neutral_emoji.png")
        emoji_width = int(emoji_image.width * 0.2)
        emoji_height = int(emoji_image.height * 0.2)
        emoji_image.thumbnail((emoji_width, emoji_height))
        template.paste(emoji_image, (630, 370))

        drawCertificate.text((480, 630), "Average", font=indexWarnFont, fill=(Rpm25, Gpm25, Bpm25))
    if 80 >= aqIndex > 70:
        emoji_image = Image.open("./assets/img/icons_for_report/emojis/unhappy_emoji.png")
        emoji_width = int(emoji_image.width * 0.2)
        emoji_height = int(emoji_image.height * 0.2)
        emoji_image.thumbnail((emoji_width, emoji_height))
        template.paste(emoji_image, (630, 370))

        drawCertificate.text((480, 630), "Elevated", font=indexWarnFont, fill=(Rpm25, Gpm25, Bpm25))
    if 90 > aqIndex > 80:
        emoji_image = Image.open("./assets/img/icons_for_report/emojis/confounded_emoji.png")
        emoji_width = int(emoji_image.width * 0.2)
        emoji_height = int(emoji_image.height * 0.2)
        emoji_image.thumbnail((emoji_width, emoji_height))
        template.paste(emoji_image, (630, 370))

        drawCertificate.text((480, 630), "High", font=indexWarnFont, fill=(255, 0, 0))
    if aqIndex >= 90:
        emoji_image = Image.open("./assets/img/icons_for_report/emojis/mask_emoji.png")
        emoji_width = int(emoji_image.width * 0.2)
        emoji_height = int(emoji_image.height * 0.2)
        emoji_image.thumbnail((emoji_width, emoji_height))
        template.paste(emoji_image, (630, 370))

        drawCertificate.text((460, 630), "Dangerous", font=indexWarnFont, fill=(154, 14, 14))

    # The commented code below is for displaying metrics in numbers
    # if pm25 > 99:
    #     template.paste(pm25Pic, (580, 670))
    #     drawCertificate.text(
    #         (650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
    #     drawCertificate.text(
    #         (650, 600), str(pm25), font=metricFont, fill=(Rpm25, Gpm25, Bpm25))
    # else:
    #     template.paste(pm25Pic, (590, 670))
    #     drawCertificate.text(
    #         (650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
    #     drawCertificate.text(
    #         (660, 600), str(pm25), font=metricFont, fill=(Rpm25, Gpm25, Bpm25))
    #
    # if pm10 > 99:
    #     template.paste(pm10Pic, (240, 670))
    #     drawCertificate.text(
    #         (295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
    #     drawCertificate.text(
    #         (270, 600), str(pm10), font=metricFont, fill=(Rpm10, Gpm10, Bpm10))
    # else:
    #     template.paste(pm10Pic, (255, 670))
    #     drawCertificate.text(
    #         (295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
    #     drawCertificate.text(
    #         (300, 600), str(pm10), font=metricFont, fill=(Rpm10, Gpm10, Bpm10))
    #
    # if co > 99:
    #     template.paste(coPic, (950, 670))
    #     drawCertificate.text(
    #         (1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
    #     drawCertificate.text(
    #         (1050, 600), str(co), font=metricFont, fill=(Rco, Gco, Bco))
    # else:
    #     template.paste(coPic, (950, 670))
    #     drawCertificate.text(
    #         (1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
    #     drawCertificate.text(
    #         (1030, 600), str(co), font=metricFont, fill=(Rco, Gco, Bco))

    drawCertificate.text(
        (50, 800), text, font=textFont, fill=(0, 0, 0), spacing=10)

    # solution to circular import, if removed the error will reappear
    from utils.back_krisha import make_2gis_request_and_return_object_count

    park_num = make_2gis_request_and_return_object_count(
        "",
        latitude,
        longitude,
        500,
        "парк")

    charger_num = make_2gis_request_and_return_object_count(
         "",
         latitude,
         longitude,
         500,
         "зарядка автомобилей")

    park_icon = Image.open("./assets/img/icons_for_report/park_icon.png")

    park_width = int(park_icon.width * 2)
    park_height = int(park_icon.height * 2)
    park_icon.thumbnail((park_width, park_height))

    template.paste(park_icon, (620, 1180))
    drawCertificate.text((740, 1175), f"{park_num}", font=aqFont, fill=(0, 153, 0))

    drawCertificate.text(
        (320, 1315), "Parks within the 5 min walk", font=textFont, fill=(0, 0, 0))

    charger_icon = Image.open("./assets/img/icons_for_report/charger_icon.png")

    template.paste(charger_icon, (620, 1380))
    drawCertificate.text((740, 1375), f"{charger_num}", font=aqFont, fill=(0, 153, 0))

    drawCertificate.text(
        (210, 1515), "Electric Vehicle chargers close by (300m)", font=textFont, fill=(0, 0, 0))

    template.save(pathToSave)
    save_png_as_pdf(pathToSave, pathToPdf)

    return pathToSave


def generate_report_for_a_car(
    car_title: str,
    generation: str,
    engine_displacement: str,
    distance_run: str,
    Nwheel_drive: str
) -> str:
    """
    Generate a report for a car with the given metrics.

    Args:
        car_title (str): The title of the car.
        generation (str): The generation of the car.
        engine_displacement (str): The engine displacement of the car.
        distance_run (str): The distance run by the car.
        Nwheel_drive (str): The number of wheels driven by the car.

    Returns:
        str: The path to the saved report."""
    try:
        template = Image.open(CAR_IMAGE_PATH)
        drawCertificate = ImageDraw.Draw(template)
    except Exception:
        pass
    car_data = {
        "car_title": car_title,
        "generation": generation,
        "engine_displacement": engine_displacement,
        "distance run (km)": distance_run,
        "N-wheel drive": Nwheel_drive,
    }
    emissions_values, recommendations = request_metrics_and_recommendations(
        car_data)
    recommendations_list = re.split(r'\d+\.', recommendations)
    recommendations_list = [
        item.strip() for item in recommendations_list if item.strip()]

    pathToSave = "./assets/reports/car_report/car_report.png"
    pathToPdf = "./assets/reports/car_report/car_report"

    indexWarnFont = ImageFont.truetype('./assets/font/FreeMonoBold.ttf', 60)
    titleFont = ImageFont.truetype('./assets/font/FreeMonoBold.ttf', 65)
    textFont = ImageFont.truetype('./assets/font/FreeMono.ttf', 40)
    recommendationFont = ImageFont.truetype('./assets/font/FreeMono.ttf', 40)

    second_lvl_heading = ImageFont.truetype('./assets/font/FreeMonoBold.ttf', 55)

    drawCertificate.text(
        (230, 70), "Car Air Pollution Report", font=titleFont, fill=(0, 0, 0))
    drawCertificate.text(
        (70, 170), "Car info:", font=second_lvl_heading, fill=(0, 0, 0))
    drawCertificate.text(
        (100, 240),
        f"Car brand and model: {car_title}", font=textFont, fill=(0, 0, 0))
    drawCertificate.text(
        (100, 290), f"Generation: {generation}", font=textFont, fill=(0, 0, 0))
    drawCertificate.text(
        (100, 340),
        f"Engine displacement: {engine_displacement}",
        font=textFont, fill=(0, 0, 0))
    drawCertificate.text(
        (100, 390), f"Distance run: {distance_run}",
        font=textFont, fill=(0, 0, 0))
    drawCertificate.text(
        (100, 440), f"N-wheel drive: {Nwheel_drive}",
        font=textFont, fill=(0, 0, 0))
    drawCertificate.text(
        (70, 510), "Gas mileage/The car pollutes \n the air to this level:",
        font=second_lvl_heading, fill=(0, 0, 0))

    gas_mileage_icon = Image.open(PICTOGRAMS_PATH + "gas_mileage_icon.png")
    ecology_index_icon = Image.open(PICTOGRAMS_PATH + "ecology_index_icon.png")

    gas_mileage = emissions_values["Gas expenditure"]
    co2_val = emissions_values["CO2"]

    gas_mileage_number = extract_gas_mileage(gas_mileage)
    co2_val_number = extract_co2_emissions(co2_val)
    ecofriendly_index_car = ((gas_mileage_number*10) + co2_val_number)/1000
    print(gas_mileage_number)
    if ecofriendly_index_car >= 0.5:
        R, G, B = 131, 0, 0

        drawCertificate.text(
            (160, 820), f"{gas_mileage_number} L/100km", font=indexWarnFont, fill=(R, G, B))
        template.paste(gas_mileage_icon, (270, 695))
        drawCertificate.text(
            (860, 820), "Dangerous", font=indexWarnFont, fill=(R, G, B))
        template.paste(ecology_index_icon, (935, 695))

    if ecofriendly_index_car >= 0.3 and ecofriendly_index_car < 0.5:
        R, G, B = 255, 225, 20

        drawCertificate.text(
            (160, 820), f"{gas_mileage_number} L/100km", font=indexWarnFont, fill=(R, G, B))
        template.paste(gas_mileage_icon, (270, 695))

        drawCertificate.text(
            (870, 820), "High", font=indexWarnFont, fill=(R, G, B))
        template.paste(ecology_index_icon, (935, 695))
    if ecofriendly_index_car >= 0.2 and ecofriendly_index_car < 0.3:
        R, G, B = 198, 239, 86
        drawCertificate.text(
            (160, 820), f"{gas_mileage_number} L/100km", font=indexWarnFont, fill=(R, G, B))
        template.paste(gas_mileage_icon, (270, 695))

        drawCertificate.text(
            (710, 820), "Moderate pollution", font=indexWarnFont, fill=(R, G, B))
        template.paste(ecology_index_icon, (935, 695))
    if ecofriendly_index_car >= 0 and ecofriendly_index_car < 0.2:
        R, G, B = 27, 152, 3
        drawCertificate.text(
            (160, 820), f"{gas_mileage_number} L/100km", font=indexWarnFont, fill=(R, G, B))
        template.paste(gas_mileage_icon, (270, 695))

        drawCertificate.text(
            (730, 820), "Low pollution", font=indexWarnFont, fill=(R, G, B))
        template.paste(ecology_index_icon, (935, 695))

    



    drawCertificate.text((70, 1000), "Recommendations:", font=second_lvl_heading, fill=(0, 0, 0))

    y_val = 1080
    for recommendation in recommendations_list:
        drawCertificate.text((100, y_val), recommendation, font=recommendationFont, fill=(0, 0, 0))
        y_val+=50

    template.save(pathToSave)
    save_png_as_pdf(pathToSave, pathToPdf)

    return pathToSave


def convert_png_to_pdf(png_path: str, pdf_path: str) -> None:
    """
    Convert a PNG image to a PDF file.

    Args:
        png_path (str): The path to the PNG image.
        pdf_path (str): The path to save the PDF file.

    Returns:
        None"""
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawImage(png_path, 0, 0, width=letter[0], height=letter[1])
    c.save()


def save_png_as_pdf(path_to_report_image: str, path_to_save: str) -> str:
    """
    Save the given report image as a PDF file.

    Args:
        path_to_report_image (str): The path to the report image.
        path_to_save (str): The path to save the PDF file.

    Returns:
        str: The path to the saved PDF file."""
    pdf_path = path_to_save + ".pdf"
    convert_png_to_pdf(path_to_report_image, pdf_path)

    return pdf_path


def append_image_to_pdf(pdf_path: str, image_path: str) -> None:
    """
    Append the given image to the given PDF file.

    Args:
        pdf_path (str): The path to the PDF file.
        image_path (str): The path to the image to append.

    Returns:
        None"""
    existing_pdf = PdfFileReader(open(pdf_path, "rb"))
    output = PdfFileWriter()
    for page in existing_pdf.pages:
        output.addPage(page)
    new_page = output.addBlankPage(width=letter[0], height=letter[1])

    with Image.open(image_path) as img:
        img_width, img_height = img.size
        page = output.getPage(output.getNumPages() - 1)
        page.mergeScaledTranslatedPage(
            new_page, scale=img_height / letter[1], tx=0, ty=0)
        page.mergePage(new_page)

    with open(pdf_path, "wb") as f:
        output.write(f)
