from PIL import Image, ImageFont, ImageDraw
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from backend_files.back_kolesa import request_metrics_and_recommendations
import os
import re


APARTMENT_IMAGE_PATH = "./apartmentReportTemplate.png"
CAR_IMAGE_PATH = "./carReportTemplate.png"
PICTOGRAMS_PATH = "./img/icons_for_report/"


def get_pm25_hour_history(sensor_name: str) -> str | None:
    """Get the path to the hourly PM2.5 history graph with the given filename.

    Args:
        filename (str): The name of the file to find."""
    folder = "/Users/daniyarkakimbekov/Workspaces/AirWay/pm25_history_graphs/hour_pm25_history/"
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
    folder = "/Users/daniyarkakimbekov/Workspaces/AirWay/pm25_history_graphs/week_pm25_history/"
    file_path = folder + filename
    if os.path.exists(file_path):
        print(f"Found file: {file_path}")
        return file_path
    else:
        print(f"File not found: {file_path}")
        return None


def generate_report_for_an_apartment(
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
    try:
        template = Image.open(APARTMENT_IMAGE_PATH)
        drawCertificate = ImageDraw.Draw(template)
    except Exception:
        pass

    R, G, B = aqIndexColor[0], aqIndexColor[1], aqIndexColor[2]
    Rpm25, Gpm25, Bpm25 = pm25Color[0], pm25Color[1], pm25Color[2]
    Rpm10, Gpm10, Bpm10 = pm10Color[0], pm10Color[1], pm10Color[2]
    Rco, Gco, Bco = coColor[0], coColor[1], coColor[2]
    pm25Pic = Image.open(PICTOGRAMS_PATH + "pm25.png")
    pm10Pic = Image.open(PICTOGRAMS_PATH + "pm10.png")
    coPic = Image.open(PICTOGRAMS_PATH + "co.png")
    pathToSave = "/Users/daniyarkakimbekov/Workspaces/AirWay/reports/realestate_report/realestate_report.png"
    pathToPdf = "/Users/daniyarkakimbekov/Workspaces/AirWay/reports/realestate_report/realestate_report_pdf"
    metricFont = ImageFont.truetype('./font/FreeMono.ttf', 90)
    aqFont = ImageFont.truetype('./font/FreeMono.ttf', 110)
    labelFont = ImageFont.truetype('./font/FreeMono.ttf', 50)
    textFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 40)

    drawCertificate.text(
        (470, 320),
        "Air Quality Index",
        font=labelFont,
        fill=(0, 0, 0))
    drawCertificate.text(
        (650, 380),
        str(aqIndex),
        font=aqFont,
        fill=(R, G, B))

    if pm25 > 99:
        template.paste(pm25Pic, (580, 670))
        drawCertificate.text(
            (650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text(
            (650, 600), str(pm25), font=metricFont, fill=(Rpm25, Gpm25, Bpm25))
    else:
        template.paste(pm25Pic, (590, 670))
        drawCertificate.text(
            (650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text(
            (660, 600), str(pm25), font=metricFont, fill=(Rpm25, Gpm25, Bpm25))

    if pm10 > 99:
        template.paste(pm10Pic, (240, 670))
        drawCertificate.text(
            (295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text(
            (270, 600), str(pm10), font=metricFont, fill=(Rpm10, Gpm10, Bpm10))
    else:
        template.paste(pm10Pic, (255, 670))
        drawCertificate.text(
            (295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text(
            (300, 600), str(pm10), font=metricFont, fill=(Rpm10, Gpm10, Bpm10))

    if co > 99:
        template.paste(coPic, (950, 670))
        drawCertificate.text(
            (1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text(
            (1050, 600), str(co), font=metricFont, fill=(Rco, Gco, Bco))
    else:
        template.paste(coPic, (950, 670))
        drawCertificate.text(
            (1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text(
            (1030, 600), str(co), font=metricFont, fill=(Rco, Gco, Bco))

    drawCertificate.text(
        (50, 940), text, font=textFont, fill=(0, 0, 0), spacing=10)
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

    pathToSave = "/Users/daniyarkakimbekov/Workspaces/AirWay/reports/car_report/car_report.png"
    pathToPdf = "/Users/daniyarkakimbekov/Workspaces/AirWay/reports/car_report/car_report"

    titleFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 65)
    textFont = ImageFont.truetype('./font/FreeMono.ttf', 40)
    recommendationFont = ImageFont.truetype('./font/FreeMono.ttf', 40)

    second_lvl_heading = ImageFont.truetype('./font/FreeMonoBold.ttf', 55)
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
        (70, 510), "Produced chemicals:",
        font=second_lvl_heading, fill=(0, 0, 0))
    co2_val = emissions_values["CO2"]
    drawCertificate.text(
        (290, 720), f"{co2_val}", font=textFont, fill=(0, 0, 0))
    nox_val = emissions_values["NOx"]
    drawCertificate.text(
        (280, 890), f"{nox_val}", font=textFont, fill=(0, 0, 0))
    so2_val = emissions_values["SO2"]
    drawCertificate.text(
        (850, 720), f"{so2_val}", font=textFont, fill=(0, 0, 0))
    pm25_val = emissions_values["PM2.5"]
    drawCertificate.text(
        (850, 890), f"{pm25_val}", font=textFont, fill=(0, 0, 0))

    drawCertificate.text((70, 1000), "Recommendation:", font=second_lvl_heading, fill=(0, 0, 0))
    drawCertificate.text((100, 1080), recommendations_list[0], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1130), recommendations_list[1], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1180), recommendations_list[2], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1230), recommendations_list[3], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1280), recommendations_list[4], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1330), recommendations_list[5], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1380), recommendations_list[6], font=recommendationFont, fill=(0, 0, 0))

    aq_index = 23
    if aq_index >= 80:
        R, G, B = 0, 196, 26
    if aq_index >= 60 and aq_index < 80:
        R, G, B = 255, 242, 117
    if aq_index < 30 and aq_index < 60:
        R, G, B = 249, 177, 8
    if aq_index >= 0 and aq_index <= 30:
        R, G, B = 183, 5, 5

    drawCertificate.text((650, 1460), "23", font=titleFont, fill=(R, G, B))
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
