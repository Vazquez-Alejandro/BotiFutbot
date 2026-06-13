import os
import sys
import json
from datetime import datetime, timedelta
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from shared.database import SessionLocal, engine, Base
from shared.models import AnalyticsEvent, MetricaDiaria, BotUsuario


def _get_session() -> Session:
    return SessionLocal()


def init_analytics():
    Base.metadata.create_all(bind=engine)


def registrar_evento(chat_id: int, accion: str, detalle: str = ""):
    session = _get_session()
    try:
        session.add(AnalyticsEvent(chat_id=chat_id, accion=accion, detalle=detalle))
        session.flush()

        hoy = datetime.now().strftime("%Y-%m-%d")
        metrica = session.query(MetricaDiaria).filter(MetricaDiaria.fecha == hoy).first()
        if not metrica:
            metrica = MetricaDiaria(fecha=hoy)
            session.add(metrica)
            session.flush()

        if accion == "usuario_nuevo":
            metrica.usuarios_nuevos = (metrica.usuarios_nuevos or 0) + 1
        elif accion == "click_link":
            metrica.clicks_links = (metrica.clicks_links or 0) + 1
        elif accion == "conversion":
            metrica.conversiones = (metrica.conversiones or 0) + 1
        elif accion in ("start", "buscar", "noticias", "equipos"):
            metrica.usuarios_activos = (metrica.usuarios_activos or 0) + 1

        session.commit()
    finally:
        session.close()


registrar_accion = registrar_evento


def obtener_usuarios_activos(dias: int = 7) -> int:
    session = _get_session()
    try:
        fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d %H:%M:%S")
        count = session.query(AnalyticsEvent).filter(
            AnalyticsEvent.created_at >= fecha_limite
        ).distinct(AnalyticsEvent.chat_id).count()
        return count
    finally:
        session.close()


def obtener_total_usuarios() -> int:
    session = _get_session()
    try:
        return session.query(BotUsuario).count()
    finally:
        session.close()


def obtener_clicks_links(dias: int = 30) -> int:
    session = _get_session()
    try:
        fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d %H:%M:%S")
        return session.query(AnalyticsEvent).filter(
            AnalyticsEvent.accion == "click_link",
            AnalyticsEvent.created_at >= fecha_limite,
        ).count()
    finally:
        session.close()


def obtener_conversiones(dias: int = 30) -> int:
    session = _get_session()
    try:
        fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d %H:%M:%S")
        return session.query(AnalyticsEvent).filter(
            AnalyticsEvent.accion == "conversion",
            AnalyticsEvent.created_at >= fecha_limite,
        ).count()
    finally:
        session.close()


def obtener_metricas_diarias(dias: int = 7) -> list:
    session = _get_session()
    try:
        fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
        rows = session.query(MetricaDiaria).filter(
            MetricaDiaria.fecha >= fecha_limite
        ).order_by(MetricaDiaria.fecha.desc()).all()
        return [
            {
                "fecha": r.fecha,
                "usuarios_nuevos": r.usuarios_nuevos or 0,
                "usuarios_activos": r.usuarios_activos or 0,
                "clicks_links": r.clicks_links or 0,
                "conversiones": r.conversiones or 0,
                "mensajes_enviados": r.mensajes_enviados or 0,
            }
            for r in rows
        ]
    finally:
        session.close()


def obtener_top_equipos(limit: int = 5) -> list:
    session = _get_session()
    try:
        rows = session.query(BotUsuario).filter(BotUsuario.activo == True).all()
        conteo = {}
        for row in rows:
            equipos = json.loads(row.equipos)
            for eq in equipos:
                nombre = eq.get("nombre", "")
                conteo[nombre] = conteo.get(nombre, 0) + 1
        ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
        return ordenados[:limit]
    finally:
        session.close()
