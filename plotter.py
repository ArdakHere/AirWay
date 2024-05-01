from PIL import Image, ImageFont, ImageDraw
from datetime import datetime

IMAGE_PATH = "./pages/reportTemplate.png"

def generate_report_for_krisha(aqIndex, aqIndexColor, pm25, pm10, co, text):
    try:
        template = Image.open(IMAGE_PATH)
        drawCertificate = ImageDraw.Draw(template)    
    except Exception:
        pass
    
    R = aqIndexColor[0]
    G = aqIndexColor[1]
    B = aqIndexColor[2]
    
    timestamp = datetime.now()
    
    metricFont = ImageFont.truetype('./font/FreeMono.ttf', 90)
    aqFont = ImageFont.truetype('./font/FreeMono.ttf', 110)
    labelFont = ImageFont.truetype('./font/FreeMono.ttf', 50)
    textFont = ImageFont.truetype('./font/FreeMonoBold.ttf', 45)

    # INDEX
    drawCertificate.text((470, 340), "Air Quality Index", font=labelFont, fill=(0, 0, 0))
    drawCertificate.text((650, 400), str(aqIndex), font=aqFont, fill=(R, G, B))
    
    # PM2.5
    if pm25 > 99:
        drawCertificate.text((650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((650, 600), str(pm25), font=metricFont, fill=(0, 0, 0))
    else:
        drawCertificate.text((650, 540), "PM2.5", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((660, 600), str(pm25), font=metricFont, fill=(0, 0, 0))
    
    # PM10
    if pm10 > 99:
        drawCertificate.text((380, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((355, 600), str(pm10), font=metricFont, fill=(0, 0, 0))
    else:
        drawCertificate.text((380, 540), "PM10", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((375, 600), str(pm10), font=metricFont, fill=(0, 0, 0))
    
    # CO
    if co > 99:
        drawCertificate.text((940, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((910, 600), str(co), font=metricFont, fill=(0, 0, 0))
    else:
        drawCertificate.text((940, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((920, 600), str(co), font=metricFont, fill=(0, 0, 0))



    # TEXT
    drawCertificate.text((50, 1000), text, font=textFont, fill=(0, 0, 0), spacing=10)

    template.save("./report/plot.png")
    return "./report/plot.png"
        

