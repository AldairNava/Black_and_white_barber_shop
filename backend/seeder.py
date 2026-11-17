import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session
from models import ModuleConfig, Staff, Service, Client, Product

CSV_CONTACTS_PATH = r"c:\aldair\whatsapp\contactos_extraidos.csv"


def seed_database(db: Session):
    # 1. Modulos / Divisiones
    modules_data = [
        {"name": "Black & White Barber", "slug": "barber", "branch_default": "Black & White Barber", "description": "Barbería clásica y moderna para caballeros."},
        {"name": "Black & White Beauty", "slug": "beauty", "branch_default": "Black & White Beauty", "description": "Salón de belleza femenino, colorimetría y faciales."},
        {"name": "Black & White Academy", "slug": "academy", "branch_default": "Black & White Academy", "description": "Academia técnica de capacitación en barbería y estilismo."},
    ]
    for m in modules_data:
        if not db.query(ModuleConfig).filter_by(slug=m["slug"]).first():
            db.add(ModuleConfig(**m))

    # 2. Staff Inicial
    staff_data = [
        {
            "name": "Aldair Nava",
            "role": "SUPERADMIN",
            "specialty": "Dirección Tecnológica y Operativa",
            "module_category": "Barber & Beauty",
            "branch": "Black & White Studio",
            "phone": "55 1111 2222",
            "username": "aldair",
            "pin": "1234",
            "avatar_initials": "AN",
            "perm_metrics": True,
            "perm_stock": True,
            "perm_appointments": True,
            "perm_users": True,
        },
        {
            "name": "Administración Black & White",
            "role": "ADMIN",
            "specialty": "Dirección General y Gerencia",
            "module_category": "Barber & Beauty",
            "branch": "Black & White Studio",
            "phone": "56 1282 5970",
            "username": "admin",
            "pin": "1234",
            "avatar_initials": "BW",
            "perm_metrics": True,
            "perm_stock": True,
            "perm_appointments": True,
            "perm_users": True,
        },
        {
            "name": "Master Barber",
            "role": "STAFF",
            "specialty": "Fades, Grecas, Diseños y Barba",
            "module_category": "Barber",
            "branch": "Black & White Barber",
            "phone": "56 1282 5971",
            "username": "barbero1",
            "pin": "1234",
            "avatar_initials": "MB",
            "perm_appointments": True,
        },
        {
            "name": "Especialista Beauty",
            "role": "STAFF",
            "specialty": "Colorimetría, Balayage y Faciales",
            "module_category": "Beauty",
            "branch": "Black & White Beauty",
            "phone": "56 1282 5972",
            "username": "estilista1",
            "pin": "1234",
            "avatar_initials": "EB",
            "perm_appointments": True,
        },
    ]
    for s in staff_data:
        if not db.query(Staff).filter_by(username=s["username"]).first():
            db.add(Staff(**s))

    # 3. Servicios Iniciales (Barber + Beauty + Academy)
    services_data = [
        # Barber
        {"code": "BW-01", "name": "Corte Clásico / Tendencia", "category": "Barber", "branch": "Black & White Barber", "duration_min": 35, "price_mxn": 150.0, "regular_price_mxn": 180.0, "description": "Corte personalizado con acabado profesional a navaja."},
        {"code": "BW-02", "name": "Corte Fade / Desvanecido", "category": "Barber", "branch": "Black & White Barber", "duration_min": 45, "price_mxn": 180.0, "regular_price_mxn": 220.0, "description": "Desvanecido milimétrico (Low, Mid, High Fade) con navaja y peinado."},
        {"code": "BW-03", "name": "Corte con Diseño / Grecas", "category": "Barber", "branch": "Black & White Barber", "duration_min": 50, "price_mxn": 220.0, "regular_price_mxn": 260.0, "description": "Diseños personalizados, grecas artísticas y líneas definidas."},
        {"code": "BW-04", "name": "Ritual de Barba y Toalla Caliente", "category": "Barber", "branch": "Black & White Barber", "duration_min": 30, "price_mxn": 140.0, "regular_price_mxn": 170.0, "description": "Vaporización, aceites esenciales, toalla caliente y perfilado a navaja."},
        {"code": "BW-05", "name": "Combo Black & White (Corte + Barba)", "category": "Barber", "branch": "Black & White Barber", "duration_min": 60, "price_mxn": 280.0, "regular_price_mxn": 350.0, "description": "Servicio premium completo: Corte con desvanecido + ritual de barba completo."},
        {"code": "BW-06", "name": "Trenzas / Braids", "category": "Barber", "branch": "Black & White Barber", "duration_min": 60, "price_mxn": 250.0, "regular_price_mxn": 300.0, "description": "Estilo urbano en trenzas de alta definición y fijación."},
        # Beauty
        {"code": "BT-01", "name": "Colorimetría / Tinte Completo", "category": "Beauty", "branch": "Black & White Beauty", "duration_min": 90, "price_mxn": 450.0, "regular_price_mxn": 550.0, "description": "Aplicación de color profesional con cubrimiento de canas y brillo."},
        {"code": "BT-02", "name": "Balayage / Mechas Iluminación", "category": "Beauty", "branch": "Black & White Beauty", "duration_min": 150, "price_mxn": 850.0, "regular_price_mxn": 1100.0, "description": "Técnica de aclarado degradado con ampolleta de protección capilar."},
        {"code": "BT-03", "name": "Tratamiento Anti-Frizz y Recuperación", "category": "Beauty", "branch": "Black & White Beauty", "duration_min": 60, "price_mxn": 350.0, "regular_price_mxn": 450.0, "description": "Reestructuración profunda para cabello maltratado o con decoloración."},
        {"code": "BT-04", "name": "Diseño y Planchado de Ceja", "category": "Beauty", "branch": "Black & White Beauty", "duration_min": 30, "price_mxn": 120.0, "regular_price_mxn": 150.0, "description": "Depilación, diseño anatómico y planchado alisador para cejas perfectas."},
        {"code": "BT-05", "name": "Limpieza Facial Profunda y Mascarilla", "category": "Beauty", "branch": "Black & White Beauty", "duration_min": 45, "price_mxn": 220.0, "regular_price_mxn": 280.0, "description": "Exfoliación, extracción de impurezas, vapor y mascarilla descongestiva."},
        # Academy
        {"code": "AC-01", "name": "Curso de Barbería Profesional (Inicial)", "category": "Academy", "branch": "Black & White Academy", "duration_min": 120, "price_mxn": 950.0, "regular_price_mxn": 1200.0, "description": "Inscripción y primer módulo de barbería clásica, uso de tijeras y máquinas."},
        {"code": "AC-02", "name": "Taller Master Fade y Diseños Urbanos", "category": "Academy", "branch": "Black & White Academy", "duration_min": 180, "price_mxn": 650.0, "regular_price_mxn": 800.0, "description": "Taller intensivo de desvanecidos limpios, grecas y técnicas modernas."},
    ]
    for s in services_data:
        if not db.query(Service).filter_by(code=s["code"]).first():
            db.add(Service(**s))

    # 4. Importar Clientes del CSV de WhatsApp si existe
    if os.path.exists(CSV_CONTACTS_PATH):
        imported_count = 0
        with open(CSV_CONTACTS_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_name = (row.get("name") or "").strip()
                raw_id = (row.get("id") or "").strip()
                phone_candidate = raw_name if raw_name.startswith("+") else raw_id

                if not db.query(Client).filter_by(phone=phone_candidate).first():
                    db.add(
                        Client(
                            name=raw_name if not raw_name.startswith("+") else "Cliente WhatsApp",
                            phone=phone_candidate,
                            wa_lid=raw_id if raw_id.endswith("@lid") else None,
                            notes=f"Último mensaje: {row.get('lastMessage', '')[:200]}" if row.get("lastMessage") else "Importado de WhatsApp",
                            visit_count=1,
                            last_visit_at=datetime.now(),
                        )
                    )
                    imported_count += 1
        print(f"[SEEDER] Importados {imported_count} clientes de WhatsApp.")

    db.commit()
    print("[SEEDER] Base de datos Black & White inicializada con éxito.")
