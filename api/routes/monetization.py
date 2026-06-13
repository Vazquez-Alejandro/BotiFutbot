from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from shared.database import get_db
from shared.models import Usuario
from shared.models_monetization import Suscripcion, Click, Conversion, EventoAnalytics
from shared.affiliates import AFILIADOS, registrar_click, get_enlace_afiliado, get_estadisticas_afiliados

router = APIRouter(prefix="/api/monetization", tags=["monetization"])

PLANES = {
    "free": {
        "nombre": "Gratuito",
        "precio": 0,
        "equipos_max": 3,
        "notificaciones_delay": 60,
        "ads": True,
        "predicciones": False,
        "estadisticas_avanzadas": False,
    },
    "premium": {
        "nombre": "Premium",
        "precio": 499,
        "equipos_max": 20,
        "notificaciones_delay": 0,
        "ads": False,
        "predicciones": True,
        "estadisticas_avanzadas": True,
    },
    "pro": {
        "nombre": "Pro",
        "precio": 999,
        "equipos_max": 50,
        "notificaciones_delay": 0,
        "ads": False,
        "predicciones": True,
        "estadisticas_avanzadas": True,
        "api_access": True,
        "webhook": True,
    },
}


@router.get("/plans")
def get_plans():
    return {"plans": PLANES}


@router.get("/affiliates")
def get_affiliates():
    return {"affiliates": AFILIADOS}


@router.post("/affiliates/click")
def track_affiliate_click(
    usuario_id: int,
    afiliado: str,
    origen: str,
    db: Session = Depends(get_db),
):
    click_id = registrar_click(db, usuario_id, afiliado, origen)
    url = get_enlace_afiliado(afiliado, str(usuario_id))
    return {"click_id": click_id, "url": url}


@router.get("/stats/{usuario_id}")
def get_user_stats(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    suscripcion = db.query(Suscripcion).filter(
        Suscripcion.usuario_id == usuario_id,
    ).first()

    plan = PLANES.get(suscripcion.plan, PLANES["free"]) if suscripcion else PLANES["free"]

    afiliado_stats = get_estadisticas_afiliados(db, usuario_id)

    eventos = db.query(EventoAnalytics).filter(
        EventoAnalytics.usuario_id == usuario_id,
    ).count()

    return {
        "plan": plan,
        "suscripcion": {
            "activa": suscripcion.activa if suscripcion else False,
            "fecha_fin": suscripcion.fecha_fin if suscripcion else None,
        } if suscripcion else None,
        "afiliados": [
            {"afiliado": a.afiliado, "clicks": a.clicks, "ingresos": float(a.ingresos)}
            for a in afiliado_stats
        ],
        "eventos_totales": eventos,
    }


@router.post("/suscribir")
def crear_suscripcion(
    usuario_id: int,
    plan: str,
    db: Session = Depends(get_db),
):
    if plan not in PLANES:
        raise HTTPException(400, "Plan inválido")

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    suscripcion = db.query(Suscripcion).filter(
        Suscripcion.usuario_id == usuario_id,
    ).first()

    if suscripcion:
        suscripcion.plan = plan
        suscripcion.activa = True
    else:
        from datetime import timedelta
        suscripcion = Suscripcion(
            usuario_id=usuario_id,
            plan=plan,
            fecha_fin=datetime.utcnow() + timedelta(days=30),
            activa=True,
        )
        db.add(suscripcion)

    db.commit()
    return {"ok": True, "plan": plan}


@router.post("/event")
def track_event(
    usuario_id: int,
    tipo: str,
    pagina: str,
    metadata: Optional[str] = None,
    db: Session = Depends(get_db),
):
    evento = EventoAnalytics(
        usuario_id=usuario_id,
        tipo=tipo,
        pagina=pagina,
        metadata=metadata,
    )
    db.add(evento)
    db.commit()
    return {"ok": True}
