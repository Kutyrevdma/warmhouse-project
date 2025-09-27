from fastapi import FastAPI
from random import uniform

app = FastAPI()

@app.get("/temperature")
def get_temperature(location: str = "", sensorId: str = ""):
    
    location = location.title() if location else location

    if not location:
        if sensorId == "1":
            location = "Living Room"
        elif sensorId == "2":
            location = "Bedroom"
        elif sensorId == "3":
            location = "Kitchen"
        else:
            location = "Unknown"

    if not sensorId:
        if location == "Living Room":
            sensorId = "1"
        elif location == "Bedroom":
            sensorId = "2"
        elif location == "Kitchen":
            sensorId = "3"
        else:
            sensorId = "0"

    value = round(uniform(-30.0, 30.0), 1)
    
    return {
        "sensorId": sensorId,
        "location": location,
        "value": value
    }

    

# Для работы монолита

@app.get("/temperature/{param}")
def get_temperature_by_path(param: str):
    if param.isdigit():
        return get_temperature(sensorId=param)
    loc = param.replace("%20", " ").replace("_", " ").strip().title()
    return get_temperature(location=loc)