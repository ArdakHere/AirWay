from PIL import Image, ImageFont, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

APARTMENT_IMAGE_PATH = "./pages/apartmentReportTemplate.png"
CAR_IMAGE_PATH = "./pages/carReportTemplate.png"
PICTOGRAMS_PATH = "./pictograms/"
IMAGE_PATH = "./pages/reportTemplate.png"


def generate_report_for_an_apartment(aqIndex: int, aqIndexColor: list, pm25Color: list, pm10Color: list, coColor: list, pm25: int, pm10: int, co: int, text: str) -> str:
    try:
        template = Image.open(IMAGE_PATH)
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
    print(coColor)

    timestamp = datetime.now()

    pm25Pic = Image.open(PICTOGRAMS_PATH + "pm25.png")
    pm10Pic = Image.open(PICTOGRAMS_PATH + "pm10.png")
    coPic = Image.open(PICTOGRAMS_PATH + "co.png")
    pathToSave = "./report/plot.png"
    pathToPdf = "./report/plot_in_pdf"

    
    metricFont = ImageFont.truetype('./font/FreeMono.ttf', 90)
    aqFont = ImageFont.truetype('./font/FreeMono.ttf', 110)
    labelFont = ImageFont.truetype('./font/FreeMono.ttf', 50)
    textFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 45)

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

def generate_report_for_a_car(aqIndex: int, aqIndexColor: list, pm25: int, pm10: int, co: int, text: str) -> str:
    pass


#generate_report_for_an_apartment(25, [0, 0, 0], 25, 25, 25, "haha")

