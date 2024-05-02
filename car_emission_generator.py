from PIL import Image, ImageFont, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import streamlit as st

APARTMENT_IMAGE_PATH = "./pages/apartmentReportTemplate.png"
CAR_IMAGE_PATH = "./pages/carReportTemplate.png"
PICTOGRAMS_PATH = "./pictograms/"
IMAGE_PATH = "./pages/car_report_template.png"


def generate_report_for_car_emission(
        data,
        car_data,
):
    impactColor = color_calculator(data["chemicals"])

    try:
        template = Image.open(IMAGE_PATH)
        drawCertificate = ImageDraw.Draw(template)    
    except Exception:
        pass

    timestamp = datetime.now()

    pathToSave = "./report/car_report.png"
    pathToPdf = "./report/car_report_in_pdf"

    topTitleFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 55)
    titleFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 40)
    textFont = ImageFont.truetype('./font/FreeMono.ttf', 25)
    chemFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 55)

    R = impactColor[0]
    G = impactColor[1]
    B = impactColor[2]

    impact = data["impact"]
    co = data["chemicals"]["co"]
    recommendation = data["recommendation"]

    # TITLE
    drawCertificate.text((320, 120), "Car Air Pollution Report", font=topTitleFont, fill=(0, 0, 0))

    # CAR DETAILS
    drawCertificate.text((50, 250), "Car details:", font=titleFont, fill=(0, 0, 0))
    for i, key in enumerate(car_data):
        drawCertificate.text((70, 320 + i*40), f"{key}: {car_data[key]}", font=textFont, fill=(0, 0, 0))

    ## chemicals
    drawCertificate.text((50, 560), "Contained chemicals: ", font=titleFont, fill=(0, 0, 0))
    drawCertificate.text((450, 640), f"{data['chemicals']['co']}", font=chemFont, fill=(R, G, B))
    drawCertificate.text((450, 820), f"{data['chemicals']['no']}", font=chemFont, fill=(R, G, B))
    drawCertificate.text((1040, 640), f"{data['chemicals']['so2']}", font=chemFont, fill=(R, G, B))
    drawCertificate.text((1040, 820), f"{data['chemicals']['pm25']}", font=chemFont, fill=(R, G, B))

    ## recommendation
    splitted_text = split_text(recommendation)
    drawCertificate.text((50, 1000), "Recommendation: ", font=titleFont, fill=(0, 0, 0))
    for i, line in enumerate(splitted_text):
        drawCertificate.text((70, 1050 + i*50), line, font=textFont, fill=(0, 0, 0))


    ## overall negativity
    drawCertificate.text((50, 1250), "Overall negtivity out of 10: ", font=titleFont, fill=(0, 0, 0))
    drawCertificate.text((770, 1250), str(impact), font=titleFont, fill=(R, G, B))

    ## overall tax on environment
    drawCertificate.text((50, 1300), "Overall tax on environment: ", font=titleFont, fill=(0, 0, 0))
    tax = calculate_tax(data)
    drawCertificate.text((770, 1300), f"{tax} kzt", font=titleFont, fill=(R, G, B))

    template.save(pathToSave)

    pdf_path = save_png_as_pdf(pathToSave, pathToPdf)

    data["report_path"] = pathToSave
    data["report_path_pdf"] = pdf_path
    return data


def calculate_tax(data):
    trees_killed = data["trees_killed"]
    per_tree_tax = 10000
    return trees_killed * per_tree_tax

def split_text(text, word_per_line=70):
    splitted_text = []
    words = text.split()
    line = ""
    for word in words:
        if len(line) + len(word) < word_per_line:
            line += word + " "
        else:
            splitted_text.append(line)
            line = word + " "
    splitted_text.append(line)
    return splitted_text


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



def color_calculator(metrics_data):
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

    return color
