from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

app = FastAPI(title="Telemetry Service")

class TelemetryPoint(BaseModel):
    sensorId: str
    location: Optional[str] = None
    value: float
    ts: Optional[str] = None

# Простое хранилище "последних значений" в памяти
_latest: Dict[str, TelemetryPoint] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/telemetry")
def ingest(p: TelemetryPoint):
    # Заполним время и локацию по умолчанию, если не пришли
    p.ts = p.ts or datetime.utcnow().isoformat()
    if not p.location:
        mapping = {"1": "Living Room", "2": "Bedroom", "3": "Kitchen"}
        p.location = mapping.get(p.sensorId, "Unknown")
    _latest[p.sensorId] = p
    return {"status": "ok"}

@app.get("/telemetry/{sensor_id}/latest")
def latest(sensor_id: str):
    if sensor_id not in _latest:
        raise HTTPException(status_code=404, detail="no data")
    return _latest[sensor_id]

# Совместимость с прежним temperature-api: GET /temperature?sensorId=2 | ?location=Bedroom
@app.get("/temperature")
def temperature(sensorId: Optional[str] = None, location: Optional[str] = None):
    if not sensorId and not location:
        raise HTTPException(status_code=400, detail="sensorId or location required")
    if not sensorId:
        rev = {"Living Room": "1", "Bedroom": "2", "Kitchen": "3"}
        sensorId = rev.get(location, "0")

    p = _latest.get(sensorId)
    if not p:
        return {"sensorId": sensorId, "location": location or "Unknown", "value": 0.0}

    # Возвращаем ровно те же поля, что и старый сервис
    return {"sensorId": p.sensorId, "location": p.location, "value": p.value}

