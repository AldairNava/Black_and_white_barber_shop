from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from database import Base


class ModuleConfig(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    description = Column(Text, nullable=True)
    branch_default = Column(String(100), default="Black & White Barber")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    role = Column(String(30), nullable=False)  # SUPERADMIN | ADMIN | SUPERVISOR | STAFF
    specialty = Column(String(150), nullable=False)
    module_category = Column(String(100), nullable=False)  # Barber | Beauty | Academy
    branch = Column(String(100), nullable=False)  # Black & White Barber | Black & White Beauty | Black & White Academy
    phone = Column(String(30), nullable=True)
    email = Column(String(120), nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    pin = Column(String(50), default="1234")
    avatar_initials = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True)
    perm_metrics = Column(Boolean, default=False)
    perm_stock = Column(Boolean, default=False)
    perm_appointments = Column(Boolean, default=False)
    perm_users = Column(Boolean, default=False)
    work_days = Column(String(80), default="Lun, Mar, Jue, Vie, Sáb, Dom")
    work_start = Column(String(10), default="11:00")
    work_end = Column(String(10), default="20:00")
    commission_pct = Column(Float, default=50.0)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(180), nullable=False)
    category = Column(String(100), nullable=False)  # Barber | Beauty | Faciales | Academy
    branch = Column(String(100), nullable=False)  # Black & White Barber | Black & White Beauty | Black & White Academy
    duration_min = Column(Integer, nullable=False)
    price_mxn = Column(Float, nullable=False)
    regular_price_mxn = Column(Float, nullable=True)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(50), unique=True, index=True, nullable=False)
    wa_lid = Column(String(80), nullable=True, index=True)
    email = Column(String(120), nullable=True, index=True)
    notes = Column(Text, nullable=True)
    pin = Column(String(50), default="1234")
    visit_count = Column(Integer, default=0, nullable=False)
    last_visit_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    client_name = Column(String(120), nullable=False)
    client_phone = Column(String(50), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    service_code = Column(String(10), nullable=False)
    service_name = Column(String(180), nullable=False)
    category = Column(String(100), nullable=False)
    branch = Column(String(100), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    staff_name = Column(String(120), nullable=False)
    appointment_date = Column(String(20), nullable=False)  # YYYY-MM-DD
    appointment_time = Column(String(10), nullable=False)  # HH:MM
    status = Column(String(40), default="PENDIENTE")  # PENDIENTE | CONFIRMADA | COMPLETADA | CANCELADA
    price_mxn = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    category = Column(String(80), nullable=False)  # Barber | Beauty | Cuidado Capilar | Accesorios
    branch = Column(String(100), nullable=False)
    price_sell_mxn = Column(Float, nullable=False)
    stock_current = Column(Integer, default=0, nullable=False)
    stock_min = Column(Integer, default=5, nullable=False)
    is_active = Column(Boolean, default=True)


class IntegrationLog(Base):
    __tablename__ = "integration_logs"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False)  # OPENWA | WEBHOOK
    event_name = Column(String(80), nullable=False)
    recipient = Column(String(120), nullable=False)
    payload_json = Column(Text, nullable=False)
    status = Column(String(40), default="SENT")
    created_at = Column(DateTime, default=datetime.now)
