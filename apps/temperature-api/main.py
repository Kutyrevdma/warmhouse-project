from fastapi import FastAPI, Query
from random import uniform
from datetime import datetime

app = FastAPI()

@app.get("/temperature")
def get_temperature(location: str = Query(...)):
    value = round(uniform(15.0, 30.0), 1)  # случайное значение
    return {
        "location": location,
        "value": value,
        "unit": "C",
        "timestamp": datetime.utcnow().isoformat()
    }
