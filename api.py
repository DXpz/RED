#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API FastAPI para recibir el JSON de noticias desde Make
y regenerar automáticamente el sitio web. (RED Noticias)
"""

import json
import re
import subprocess
import logging
import urllib.request
import threading
import time
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse

# ── Configuración ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
NOTICIAS_JSON = BASE_DIR / "noticias.json"
LOG_FILE = BASE_DIR / "api.log"
API_KEY_FILE = BASE_DIR / ".api_key"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ── Cargar API key desde archivo ───────────────────────────────────────────────
if not API_KEY_FILE.exists():
    raise RuntimeError(f"Falta el archivo de API key: {API_KEY_FILE}")

API_KEY = API_KEY_FILE.read_text().strip()

MAKE_WEBHOOK_NOTIFICACION = ""
MAKE_WEBHOOK_CONFIRMACION = "https://hook.eu2.make.com/rvl9vaw5ylanuatzwftqxj6piwot8i2c"
MAKE_WEBHOOK_NEWSLETTER = ""

# Dejar desactivado el webhook inmediato (el que notifica "servidor actualizado").
ENVIAR_NOTIFICACION_WEBHOOK = False

# Dejar activo el webhook importante diferido (+5 min) con:
# {"status": "ok", "timestamp": "..."}
ENVIAR_CONFIRMACION_WEBHOOK = True


def obtener_fecha_actualizacion_ddmmyyyy() -> str:
    """
    Lee `config.fecha_actualizacion` desde `noticias.json` y lo convierte a DD/MM/YYYY.
    Ejemplo origen: "Jueves, 19 de marzo de 2026".
    """
    try:
        data = json.loads(NOTICIAS_JSON.read_text(encoding="utf-8"))
        fecha_str = (data.get("config") or {}).get("fecha_actualizacion") or ""
        # Captura: "19 de marzo de 2026" dentro de una frase más larga.
        m = re.search(
            r"(?P<dia>\d{1,2})\s+de\s+(?P<mes>[A-Za-záéíóúñÑ]+)\s+de\s+(?P<anio>\d{4})",
            fecha_str,
            flags=re.IGNORECASE,
        )
        if not m:
            raise ValueError(f"No se pudo parsear fecha_actualizacion: {fecha_str!r}")

        dia = int(m.group("dia"))
        mes_es = m.group("mes").lower()
        anio = int(m.group("anio"))

        meses = {
            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "setiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12,
        }

        if mes_es not in meses:
            raise ValueError(f"Mes no reconocido: {mes_es!r}")

        mes = meses[mes_es]
        return f"{dia:02d}/{mes:02d}/{anio:04d}"
    except Exception as e:
        logging.warning(f"No se pudo obtener fecha_actualizacion_ddmmyyyy: {e}")
        # Fallback: fecha actual del servidor.
        return datetime.now().strftime("%d/%m/%Y")


def llamar_webhook(url: str, payload: dict, nombre: str, timeout: int = 30):
    """Envía un POST JSON a un webhook de Make."""
    if not url:
        return
    data = json.dumps(payload).encode("utf-8")
    try:
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            logging.info(f"Webhook [{nombre}] notificado — status {resp.status}")
    except Exception as e:
        logging.warning(f"No se pudo notificar al webhook [{nombre}]: {e}")


def notificar_make(exito: bool, mensaje: str, timestamp: str):
    """Notifica ambos webhooks de Make al finalizar la actualización."""
    payload_notificacion = {
        "success": exito,
        "mensaje": mensaje,
        "timestamp": timestamp,
    }
    if ENVIAR_NOTIFICACION_WEBHOOK:
        llamar_webhook(MAKE_WEBHOOK_NOTIFICACION, payload_notificacion, "notificacion")

    if exito and ENVIAR_CONFIRMACION_WEBHOOK:
        def enviar_confirmacion_diferida():
            logging.info("Esperando 5 minutos antes de enviar confirmación final...")
            time.sleep(300)
            fecha_actualizacion_ddmmyyyy = obtener_fecha_actualizacion_ddmmyyyy()
            payload_confirmacion = {
                "status": "ok",
                "timestamp": datetime.now().isoformat(),
                "fecha_actualizacion_ddmmyyyy": fecha_actualizacion_ddmmyyyy,
            }
            llamar_webhook(MAKE_WEBHOOK_CONFIRMACION, payload_confirmacion, "confirmacion")

        hilo = threading.Thread(target=enviar_confirmacion_diferida, daemon=True)
        hilo.start()


# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="RED Noticias API",
    description="Recibe el JSON de noticias y regenera el sitio web.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verificar_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        logging.warning("Intento de acceso con API key inválida")
        raise HTTPException(status_code=403, detail="API key inválida")
    return key


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Comprueba que la API está activa."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/noticias")
def obtener_noticias(key: str = Security(verificar_api_key)):
    """Devuelve el contenido actual de noticias.json."""
    if not NOTICIAS_JSON.exists():
        raise HTTPException(status_code=404, detail="noticias.json no encontrado")
    try:
        datos = json.loads(NOTICIAS_JSON.read_text(encoding="utf-8"))
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer noticias.json: {e}")


@app.post("/api/actualizar")
async def actualizar_noticias(request: Request, key: str = Security(verificar_api_key)):
    """
    Recibe el JSON de noticias desde Make, lo guarda y regenera el sitio.
    Header requerido: X-API-Key
    Body: JSON con la lista de noticias
    """
    try:
        datos = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="El body no es JSON válido")

    # Guardar noticias.json
    try:
        NOTICIAS_JSON.write_text(json.dumps(datos, ensure_ascii=False, indent=2))
        logging.info(f"noticias.json actualizado — {len(datos) if isinstance(datos, list) else '?'} entradas")
    except Exception as e:
        logging.error(f"Error al guardar noticias.json: {e}")
        raise HTTPException(status_code=500, detail=f"Error al guardar noticias.json: {e}")

    # Ejecutar script maestro
    errores = []
    resultado = subprocess.run(
        ["python3", str(BASE_DIR / "actualizar_todo.py")],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
    )
    if resultado.returncode != 0:
        msg = f"Error en actualizar_todo.py: {resultado.stderr.strip()}"
        logging.error(msg)
        errores.append(msg)
    else:
        logging.info("actualizar_todo.py ejecutado correctamente")

    timestamp = datetime.now().isoformat()

    if errores:
        notificar_make(False, f"Errores en scripts: {'; '.join(errores)}", timestamp)
        return JSONResponse(status_code=207, content={
            "status": "parcial",
            "mensaje": "noticias.json guardado pero hubo errores en los scripts",
            "errores": errores,
        })

    logging.info("Sitio regenerado correctamente")
    notificar_make(True, "Sitio actualizado correctamente", timestamp)
    return {"status": "ok", "mensaje": "Sitio actualizado correctamente", "timestamp": timestamp}


@app.post("/api/newsletter")
async def suscribir_newsletter(request: Request):
    """
    Recibe el correo del usuario y delega el envío al flujo de Make.
    El usuario final solo ve una confirmación simple, no la respuesta del webhook.
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Body JSON inválido")

    correo = (data or {}).get("correo")
    if not correo or "@" not in correo:
        raise HTTPException(status_code=400, detail="Correo inválido")

    timestamp = datetime.now().isoformat()
    payload = {
        "accion": "suscripcion",
        "correo": correo,
        "timestamp": timestamp,
        "origen": "web",
    }
    llamar_webhook(MAKE_WEBHOOK_NEWSLETTER, payload, "newsletter")
    return {"status": "ok", "mensaje": "Suscripción recibida"}
