from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import subprocess
import platform
import psutil

from db import Base, engine, get_db
from models import Incident, EventLog
from logging_config import setup_logging

Base.metadata.create_all(bind=engine)
logger = setup_logging()

app = FastAPI(title="IT Automation & Incident Response System (ITAIRS)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SystemInfo(BaseModel):
    hostname: str
    os: str
    uptime_seconds: float
    cpu_percent: float
    memory_percent: float
    disk_percent: float


class PingRequest(BaseModel):
    target: str


class PingResult(BaseModel):
    target: str
    success: bool
    output: str


class IncidentCreate(BaseModel):
    severity: str
    source: str
    category: str
    message: str


class IncidentOut(BaseModel):
    id: int
    severity: str
    source: str
    category: str
    message: str
    created_at: datetime

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    level: str
    source: str
    message: str


class EventOut(BaseModel):
    id: int
    level: str
    source: str
    message: str
    created_at: datetime

    class Config:
        orm_mode = True


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/system/info", response_model=SystemInfo)
def system_info():
    boot_time = psutil.boot_time()
    uptime = datetime.utcnow().timestamp() - boot_time

    cpu = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    info = SystemInfo(
        hostname=platform.node(),
        os=f"{platform.system()} {platform.release()}",
        uptime_seconds=uptime,
        cpu_percent=cpu,
        memory_percent=mem,
        disk_percent=disk,
    )
    return info


@app.post("/api/network/ping", response_model=PingResult)
def ping_host(payload: PingRequest):
    target = payload.target.strip()
    if not target:
        return PingResult(target=target, success=False, output="empty target")

    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "3", target],
            capture_output=True,
            text=True,
            timeout=10,
        )
        success = result.returncode == 0
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        success = False
        output = str(e)

    logger.info(f"Ping to {target} success={success}")
    return PingResult(target=target, success=success, output=output)


@app.post("/api/incidents", response_model=IncidentOut)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(
        severity=payload.severity,
        source=payload.source,
        category=payload.category,
        message=payload.message,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    logger.info(f"Incident created: {incident.severity} {incident.source} {incident.category}")
    return incident


@app.get("/api/incidents", response_model=List[IncidentOut])
def list_incidents(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    severity: Optional[str] = None,
):
    query = db.query(Incident).order_by(Incident.created_at.desc())
    if severity:
        query = query.filter(Incident.severity == severity)
    incidents = query.limit(limit).all()
    return incidents


@app.post("/api/events", response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    evt = EventLog(
        level=payload.level,
        source=payload.source,
        message=payload.message,
    )
    db.add(evt)
    db.commit()
    db.refresh(evt)
    logger.info(f"Event logged: {evt.level} {evt.source}")
    return evt


@app.get("/api/events", response_model=List[EventOut])
def list_events(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000),
):
    events = (
        db.query(EventLog)
        .order_by(EventLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return events


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
