import os
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, SessionLocal, get_db, Base
from models import ModuleConfig, Staff, Service, Client, Appointment, Product, IntegrationLog
from seeder import seed_database
from integrations import WhatsAppDispatcher

app = FastAPI(
    title="Black & White Studio API",
    version="1.0.0",
    description="Backend para Black & White Barber, Beauty & Academy (Puerto 8003)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


# --- Pydantic Schemas ---
class AppointmentCreate(BaseModel):
    client_name: str
    client_phone: str
    service_id: int
    staff_id: int
    appointment_date: str
    appointment_time: str
    notes: Optional[str] = ""


class LoginRequest(BaseModel):
    identifier: str
    pin: Optional[str] = "1234"


# --- API Endpoints ---
@app.get("/api/health")
def health():
    return {
        "status": "online",
        "studio": "Black & White Studio",
        "divisions": ["Barber", "Beauty", "Academy"],
        "port": 8003,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/public-catalog")
def get_public_catalog(db: Session = Depends(get_db)):
    services = db.query(Service).filter_by(is_active=True).all()
    staff = db.query(Staff).filter_by(is_active=True).all()
    modules = db.query(ModuleConfig).filter_by(is_active=True).all()

    return {
        "studio": {
            "name": "Black & White Studio",
            "tagline": "Profesionalismo, experiencia y calidad",
            "address": "Amanecer Ranchero 93, Nezahualcóyotl, Estado de México, C.P. 57000",
            "phone": "56 1282 5970",
            "whatsapp": "5215612825970",
            "schedule": {
                "regular": "Lunes a Sábado: 11:00 AM - 8:00 PM (Miércoles cerrado)",
                "sunday": "Domingo: 12:00 PM - 5:00 PM",
            },
        },
        "modules": [
            {"id": m.id, "name": m.name, "slug": m.slug, "description": m.description}
            for m in modules
        ],
        "services": [
            {
                "id": s.id,
                "code": s.code,
                "name": s.name,
                "category": s.category,
                "branch": s.branch,
                "duration_min": s.duration_min,
                "price_mxn": s.price_mxn,
                "regular_price_mxn": s.regular_price_mxn,
                "description": s.description,
            }
            for s in services
        ],
        "staff": [
            {
                "id": st.id,
                "name": st.name,
                "specialty": st.specialty,
                "branch": st.branch,
                "avatar_initials": st.avatar_initials,
            }
            for st in staff
            if st.role in ["STAFF", "ADMIN", "SUPERADMIN"]
        ],
    }


@app.post("/api/appointments")
def create_appointment(req: AppointmentCreate, db: Session = Depends(get_db)):
    service = db.query(Service).filter_by(id=req.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    staff = db.query(Staff).filter_by(id=req.staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Especialista no encontrado")

    # Registrar o vincular cliente
    phone_clean = req.client_phone.strip()
    client = db.query(Client).filter_by(phone=phone_clean).first()
    if not client:
        client = Client(
            name=req.client_name.strip(),
            phone=phone_clean,
            visit_count=1,
            last_visit_at=datetime.now(),
        )
        db.add(client)
        db.commit()
        db.refresh(client)
    else:
        client.visit_count += 1
        client.last_visit_at = datetime.now()
        db.commit()

    appt = Appointment(
        client_id=client.id,
        client_name=req.client_name.strip(),
        client_phone=phone_clean,
        service_id=service.id,
        service_code=service.code,
        service_name=service.name,
        category=service.category,
        branch=service.branch,
        staff_id=staff.id,
        staff_name=staff.name,
        appointment_date=req.appointment_date,
        appointment_time=req.appointment_time,
        price_mxn=service.price_mxn,
        notes=req.notes or "",
        status="CONFIRMADA",
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)

    # Disparo de confirmación por WhatsApp en segundo plano
    appt_dict = {
        "client_name": appt.client_name,
        "client_phone": appt.client_phone,
        "service_name": appt.service_name,
        "branch": appt.branch,
        "staff_name": appt.staff_name,
        "appointment_date": appt.appointment_date,
        "appointment_time": appt.appointment_time,
        "price_mxn": appt.price_mxn,
    }
    WhatsAppDispatcher.notify_new_appointment(db, appt_dict)

    return {"status": "success", "appointment_id": appt.id, "message": "Cita confirmada"}


@app.get("/api/admin/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).order_by(Appointment.id.desc()).all()
    clients = db.query(Client).order_by(Client.id.desc()).all()
    services = db.query(Service).all()
    staff = db.query(Staff).all()

    total_income = sum(a.price_mxn for a in appointments if a.status in ["CONFIRMADA", "COMPLETADA"])

    return {
        "metrics": {
            "total_clients": len(clients),
            "total_appointments": len(appointments),
            "estimated_income_mxn": total_income,
            "services_count": len(services),
            "staff_count": len(staff),
        },
        "appointments": [
            {
                "id": a.id,
                "client_name": a.client_name,
                "client_phone": a.client_phone,
                "service_name": a.service_name,
                "branch": a.branch,
                "staff_name": a.staff_name,
                "appointment_date": a.appointment_date,
                "appointment_time": a.appointment_time,
                "status": a.status,
                "price_mxn": a.price_mxn,
            }
            for a in appointments
        ],
        "clients": [
            {
                "id": c.id,
                "name": c.name,
                "phone": c.phone,
                "visit_count": c.visit_count,
                "last_visit_at": c.last_visit_at.strftime("%Y-%m-%d %H:%M") if c.last_visit_at else "",
            }
            for c in clients[:50]  # Primeros 50 para rapidez
        ],
    }


# Frontend Servido directamente
FRONTEND_INDEX = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dist", "index.html")
)

@app.get("/", include_in_schema=False)
def serve_root():
    if os.path.isfile(FRONTEND_INDEX):
        return FileResponse(FRONTEND_INDEX)
    return HTMLResponse("<h1>Black & White Studio API activa en Puerto 8002</h1>")
