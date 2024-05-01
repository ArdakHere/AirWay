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
        


def generate_report_for_car_emission(
        impact, 
        co2, 
        pm25, 
        pm10, 
        recommendation, 
        trees_killed,
        impactColor,
):
    try:
        template = Image.open(IMAGE_PATH)
        drawCertificate = ImageDraw.Draw(template)    
    except Exception:
        pass

    timestamp = datetime.now()

    metricFont = ImageFont.truetype('./font/FreeMono.ttf', 90)
    aqFont = ImageFont.truetype('./font/FreeMono.ttf', 110)
    labelFont = ImageFont.truetype('./font/FreeMono.ttf', 50)
    textFont = ImageFont.truetype('./font/FreeMono.ttf', 20)


    R = impactColor[0]
    G = impactColor[1]
    B = impactColor[2]

    drawCertificate.text((150, 340), "Negative impact on environment out of 10", font=labelFont, fill=(0, 0, 0))
    drawCertificate.text((650, 400), str(impact), font=aqFont, fill=(R, G, B))
    
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
    if co2 > 99:
        drawCertificate.text((940, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((910, 600), str(co2), font=metricFont, fill=(0, 0, 0))
    else:
        drawCertificate.text((940, 540), "CO", font=labelFont, fill=(0, 0, 0))
        drawCertificate.text((920, 600), str(co2), font=metricFont, fill=(0, 0, 0))

    
    # Recommendation text
    drawCertificate.text((150, 830), "Recommendation:", font=labelFont, fill=(0, 0, 0))
    splitted_text = split_text(recommendation)
    for i, text in enumerate(splitted_text):
        drawCertificate.text((150, 900 + i*30), text, font=textFont, fill=(0, 0, 0), spacing=0)

    template.save("./report/plot.png")
    return "./report/plot.png"



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