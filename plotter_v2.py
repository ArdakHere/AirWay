from PIL import Image, ImageFont, ImageDraw
from datetime import datetime

APARTMENT_IMAGE_PATH = "./pages/apartmentReportTemplate.png"
CAR_IMAGE_PATH = "./pages/carReportTemplate.png"
PICTOGRAMS_PATH = "./pictograms/"

def generate_report_for_an_apartment(aqIndex: int, aqIndexColor: list, pm25: int, pm10: int, co: int, text: str) -> str:
    
    try:
        template = Image.open(APARTMENT_IMAGE_PATH)
        drawCertificate = ImageDraw.Draw(template)    
    except Exception:
        pass
    
    # Path to save the final image at, will also be returned
    pathToSave = "./report/plot.png"
    
    # Pictograms

    pm25Pic = Image.open(PICTOGRAMS_PATH + "pm25.png")
    pm10Pic = Image.open(PICTOGRAMS_PATH + "pm10.png")
    coPic = Image.open(PICTOGRAMS_PATH + "co.png")

    # indexPic = Image.open(PICTOGRAMS_PATH + "index.png")
    
    timestamp = datetime.now()
    
    # Air Quality index font
    aqFont = ImageFont.truetype('./font/FreeMono.ttf', 110)
    # Font for all the other metrics
    metricFont = ImageFont.truetype('./font/FreeMono.ttf', 90)
    # Font for labels
    labelFont = ImageFont.truetype('./font/FreeMono.ttf', 50)
    # BOLD TEXT font
    textFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 45) 

    # INDEX
    # template.paste(indexPic, (580, 100))
    drawCertificate.text((470, 340), "Air Quality Index", font=labelFont, fill=(0, 0, 0))
    drawCertificate.text((650, 400), str(aqIndex), font=aqFont, fill=(aqIndexColor[0], aqIndexColor[1], aqIndexColor[2]))
    
    # PM2.5
    if pm25 > 99:
        template.paste(pm25Pic, (580, 670))
        drawCertificate.text((650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((650, 600), str(pm25), font=metricFont, fill=(0, 0, 0))
    else:
        template.paste(pm25Pic, (590, 670))
        drawCertificate.text((650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((660, 600), str(pm25), font=metricFont, fill=(0, 0, 0))
    
    # PM10
    if pm10 > 99:
        template.paste(pm10Pic, (240, 670))
        drawCertificate.text((295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((270, 600), str(pm10), font=metricFont, fill=(0, 0, 0))
    else:
        template.paste(pm10Pic, (255, 670))
        drawCertificate.text((295, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((300, 600), str(pm10), font=metricFont, fill=(0, 0, 0))
    
    # CO
    if co > 99:
        template.paste(coPic, (950, 670))
        drawCertificate.text((1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((1050, 600), str(co), font=metricFont, fill=(0, 0, 0))
    else:
        template.paste(coPic, (950, 670))
        drawCertificate.text((1050, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((1030, 600), str(co), font=metricFont, fill=(0, 0, 0))

    # TEXT
    drawCertificate.text((50, 1000), text, font=textFont, fill=(0, 0, 0), spacing=10)
    
    template.save(pathToSave)
    
    return pathToSave
        
def generate_report_for_a_car(aqIndex: int, aqIndexColor: list, pm25: int, pm10: int, co: int, text: str) -> str:
    
    pass


generate_report_for_an_apartment(25, [0, 0 , 0], 25, 25, 25, "haha")
