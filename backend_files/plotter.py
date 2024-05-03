from PIL import Image, ImageFont, ImageDraw
from reportlab.lib.pagesizes import *
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from datetime import datetime
from backend_files.back_kolesa import *
import os

APARTMENT_IMAGE_PATH = "./apartmentReportTemplate.png"
CAR_IMAGE_PATH = "./carReportTemplate.png"
PICTOGRAMS_PATH = "./img/icons_for_report/"

def get_pm25_hour_history(filename: str):
    # Path to the src folder
    folder = "/Users/ardaka/Desktop/AirWay/pm25_history_graphs/hour_pm25_history/"
    # Construct the full file path
    file_path = folder + filename
    # Check if the file exists
    if os.path.exists(file_path):
        # File found, return the file path
        print(f"Found file: {file_path}")
        return file_path
    else:
        print(f"File not found: {file_path}")
        return None



def get_pm25_week_history(filename: str):
    # Path to the src folder
    folder = "/Users/ardaka/Desktop/AirWay/pm25_history_graphs/week_pm25_history/"

    # Construct the full file path
    file_path = folder + filename

    # Check if the file exists
    if os.path.exists(file_path):
        # File found, return the file path
        print(f"Found file: {file_path}")
        return file_path
    else:
        print(f"File not found: {file_path}")
        return None


def generate_report_for_an_apartment(aqIndex: int, aqIndexColor: list, pm25Color: list,
                                     pm10Color: list, coColor: list, pm25: int,
                                     pm10: int, co: int, text: str):
    try:
        template = Image.open(APARTMENT_IMAGE_PATH)
        drawCertificate = ImageDraw.Draw(template)
    except Exception:
        pass

    R = aqIndexColor[0]
    G = aqIndexColor[1]
    B = aqIndexColor[2]

    Rpm25 = pm25Color[0]
    Gpm25 = pm25Color[1]
    Bpm25 = pm25Color[2]

    Rpm10 = pm10Color[0]
    Gpm10 = pm10Color[1]
    Bpm10 = pm10Color[2]

    Rco = coColor[0]
    Gco = coColor[1]
    Bco = coColor[2]

    timestamp = datetime.now()

    pm25Pic = Image.open(PICTOGRAMS_PATH + "pm25.png")
    pm10Pic = Image.open(PICTOGRAMS_PATH + "pm10.png")
    coPic = Image.open(PICTOGRAMS_PATH + "co.png")
    pathToSave = "/Users/ardaka/Desktop/AirWay/reports/realestate_report/realestate_report.png"
    pathToPdf = "/Users/ardaka/Desktop/AirWay/reports/realestate_report/realestate_report_pdf"


    metricFont = ImageFont.truetype('./font/FreeMono.ttf', 90)
    aqFont = ImageFont.truetype('./font/FreeMono.ttf', 110)
    labelFont = ImageFont.truetype('./font/FreeMono.ttf', 50)
    textFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 40)

    # INDEX
    drawCertificate.text((470, 320), "Air Quality Index", font=labelFont, fill=(0, 0, 0))
    drawCertificate.text((650, 380), str(aqIndex), font=aqFont, fill=(R, G, B))

    # PM2.5
    if pm25 > 99:
        template.paste(pm25Pic, (580, 670))
        drawCertificate.text((650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((650, 600), str(pm25), font=metricFont, fill=(Rpm25, Gpm25, Bpm25))
    else:
        template.paste(pm25Pic, (590, 670))
        drawCertificate.text((650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((660, 600), str(pm25), font=metricFont, fill=(Rpm25, Gpm25, Bpm25))

    # PM10
    if pm10 > 99:
        template.paste(pm10Pic, (240, 670))
        drawCertificate.text((295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((270, 600), str(pm10), font=metricFont, fill=(Rpm10, Gpm10, Bpm10))
    else:
        template.paste(pm10Pic, (255, 670))
        drawCertificate.text((295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((300, 600), str(pm10), font=metricFont, fill=(Rpm10, Gpm10, Bpm10))

    # CO
    if co > 99:
        template.paste(coPic, (950, 670))
        drawCertificate.text((1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((1050, 600), str(co), font=metricFont, fill=(Rco, Gco, Bco))
    else:
        template.paste(coPic, (950, 670))
        drawCertificate.text((1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((1030, 600), str(co), font=metricFont, fill=(Rco, Gco, Bco))

    drawCertificate.text((50, 940), text, font=textFont, fill=(0, 0, 0), spacing=10)

    template.save(pathToSave)

    save_png_as_pdf(pathToSave, pathToPdf)

    return pathToSave

def generate_report_for_a_car(car_title: str, generation: str, engine_displacement: str, distance_run: str, Nwheel_drive: str):
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

    emissions_values, recommendations = gpt_metrics_caller(car_data)
    recommendations_list = re.split(r'\d+\.', recommendations)

    recommendations_list = [item.strip() for item in recommendations_list if item.strip()]

    pathToSave = "/Users/ardaka/Desktop/AirWay/reports/car_report/car_report.png"
    pathToPdf = "/Users/ardaka/Desktop/AirWay/reports/car_report/car_report"

    titleFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 65)
    metricFont = ImageFont.truetype('./font/FreeMono.ttf', 45)
    textFont = ImageFont.truetype('./font/FreeMono.ttf', 40)
    abbreviationFont = ImageFont.truetype('./font/FreeMono.ttf', 28)
    recommendationFont = ImageFont.truetype('./font/FreeMono.ttf', 40)

    second_lvl_heading = ImageFont.truetype('./font/FreeMonoBold.ttf', 55)
    print(drawCertificate)

    drawCertificate.text((230, 70), "Car Air Pollution Report", font=titleFont, fill=(0, 0, 0))

    drawCertificate.text((70, 170), "Car info:", font=second_lvl_heading, fill=(0, 0, 0))

    drawCertificate.text((100, 240), f"Car brand and model: {car_title}", font=textFont, fill=(0, 0, 0))
    drawCertificate.text((100, 290), f"Generation: {generation}", font=textFont, fill=(0, 0, 0))
    drawCertificate.text((100, 340), f"Engine displacement: {engine_displacement}", font=textFont, fill=(0, 0, 0))
    drawCertificate.text((100, 390), f"Distance run: {distance_run}", font=textFont, fill=(0, 0, 0))
    drawCertificate.text((100, 440), f"N-wheel drive: {Nwheel_drive}", font=textFont, fill=(0, 0, 0))

    drawCertificate.text((70, 510), "Produced chemicals:", font=second_lvl_heading, fill=(0, 0, 0))

    co2_val = emissions_values["CO2"]
    drawCertificate.text((290, 720), f"{co2_val}", font=textFont, fill=(0, 0, 0))

    nox_val = emissions_values["NOx"]
    drawCertificate.text((280, 890), f"{nox_val}", font=textFont, fill=(0, 0, 0))

    so2_val = emissions_values["SO2"]
    drawCertificate.text((850, 720), f"{so2_val}", font=textFont, fill=(0, 0, 0))


    pm25_val = emissions_values["PM2.5"]
    drawCertificate.text((850, 890), f"{pm25_val}", font=textFont, fill=(0, 0, 0))


    drawCertificate.text((70, 1000), "Recommendation:", font=second_lvl_heading, fill=(0, 0, 0))

    drawCertificate.text((100, 1080), recommendations_list[0], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1130), recommendations_list[1], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1180), recommendations_list[2], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1230), recommendations_list[3], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1280), recommendations_list[4], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1330), recommendations_list[5], font=recommendationFont, fill=(0, 0, 0))
    drawCertificate.text((100, 1380), recommendations_list[6], font=recommendationFont, fill=(0, 0, 0))


    template.save(pathToSave)

    save_png_as_pdf(pathToSave, pathToPdf)

    return pathToSave

def convert_png_to_pdf(png_path, pdf_path):
    # Create a canvas with the PDF path
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Draw the PNG onto the canvas
    c.drawImage(png_path, 0, 0, width=letter[0], height=letter[1])

    # Save the PDF
    c.save()


# Example usage
def save_png_as_pdf(path_to_png, path_to_save):
    pdf_path = path_to_save + ".pdf"  # Append '.pdf' to the file path
    convert_png_to_pdf(path_to_png, pdf_path)
    return pdf_path

def append_image_to_pdf(pdf_path: str, image_path: str) -> None:
    # Open the PDF in 'append' mode
    existing_pdf = PdfFileReader(open(pdf_path, "rb"))
    output = PdfFileWriter()

    # Add existing pages to the output
    for page in existing_pdf.pages:
        output.addPage(page)

    # Create a new page
    new_page = output.addBlankPage(width=letter[0], height=letter[1])

    # Draw the image onto the new page
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        page = output.getPage(output.getNumPages() - 1)
        page.mergeScaledTranslatedPage(new_page, scale=img_height / letter[1], tx=0, ty=0)
        page.mergePage(new_page)

    # Write the output PDF to file
    with open(pdf_path, "wb") as f:
        output.write(f)




