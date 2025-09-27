from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Devices Service")

class Device(BaseModel):
    id: str
    type: str
    location: str
    status: str = "off"  # "on" | "off"

class Command(BaseModel):
    action: str  # "on" | "off"

# простая in-memory "БД"
_db: Dict[str, Device] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/devices", response_model=Device)
def create_device(d: Device):
    _db[d.id] = d
    return d

@app.get("/devices", response_model=List[Device])
def list_devices():
    return list(_db.values())

@app.get("/devices/{device_id}", response_model=Device)
def get_device(device_id: str):
    d = _db.get(device_id)
    if not d:
        raise HTTPException(status_code=404, detail="not found")
    return d

@app.post("/devices/{device_id}/command", response_model=Device)
def command_device(device_id: str, cmd: Command):
    d = _db.get(device_id)
    if not d:
        raise HTTPException(status_code=404, detail="not found")
    act = cmd.action.lower()
    if act not in {"on", "off"}:
        raise HTTPException(status_code=400, detail="unknown action")
    d.status = act
    _db[device_id] = d
    return d
