import os
import json
import urllib.request
from datetime import datetime
from sqlalchemy.orm import Session
from models import IntegrationLog

OPENWA_HOST = os.getenv("OPENWA_HOST", "http://localhost:2785")
OPENWA_API_KEY = os.getenv("OPENWA_API_KEY", "owa_k1_5694480ac51cb9a682b338dc16a76b2a87374d560a6f1e095c2dc2b982bdf66d")
OPENWA_SESSION_ID = os.getenv("OPENWA_SESSION_ID", "2ad723f8-472e-4340-a0e2-0015ad6e2a51")  # agente-blackwhite


class WhatsAppDispatcher:
    """Envío real de notificaciones WhatsApp a través de OpenWA."""

    @classmethod
    def send_whatsapp(cls, recipient: str, text: str) -> dict:
        url = f"{OPENWA_HOST}/api/sessions/{OPENWA_SESSION_ID}/messages/send-text"
        payload = json.dumps({"chatId": recipient, "text": text}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": OPENWA_API_KEY,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                res_body = response.read().decode("utf-8")
                return {"status": "success", "response": json.loads(res_body)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @classmethod
    def notify_new_appointment(cls, db: Session, appointment_data: dict):
        text = (
            f"✨ ¡Hola {appointment_data['client_name']}!\n"
            f"Tu cita en *Black & White Studio* ha sido agendada con éxito:\n\n"
            f"✂️ *Servicio:* {appointment_data['service_name']}\n"
            f"💈 *División:* {appointment_data['branch']}\n"
            f"👤 *Especialista:* {appointment_data['staff_name']}\n"
            f"📅 *Fecha:* {appointment_data['appointment_date']}\n"
            f"⏰ *Hora:* {appointment_data['appointment_time']}\n"
            f"💵 *Total:* ${appointment_data['price_mxn']:.0f} MXN\n\n"
            f"📍 Amanecer Ranchero 93, Nezahualcóyotl, Estado de México.\n"
            f"¡Te esperamos con el mejor servicio!"
        )

        recipient = appointment_data["client_phone"]
        # Enviar WhatsApp si no es lid desconocido
        res = cls.send_whatsapp(recipient, text)

        # Log en base de datos
        log = IntegrationLog(
            provider="OPENWA",
            event_name="APPOINTMENT_CONFIRMED",
            recipient=recipient,
            payload_json=json.dumps({"text": text, "result": res}, ensure_ascii=False),
            status=res["status"].upper(),
        )
        db.add(log)
        db.commit()
        return res
