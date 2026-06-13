import json
import os
import sys
from typing import Optional
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from shared.database import SessionLocal, engine, Base
from shared.models import BotUsuario, EventoEnviado, NoticiaEnviada, PartidoProgramado


@dataclass
class Usuario:
    chat_id: int
    username: Optional[str]
    equipos: list
    activo: bool = True


def init_db():
    from shared.database import DATABASE_URL
    if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def _get_session() -> Session:
    return SessionLocal()


def guardar_usuario(chat_id: int, username: Optional[str] = None):
    session = _get_session()
    try:
        existing = session.query(BotUsuario).filter(BotUsuario.chat_id == chat_id).first()
        if not existing:
            session.add(BotUsuario(chat_id=chat_id, username=username))
            session.commit()
    finally:
        session.close()


def obtener_usuario(chat_id: int) -> Optional[Usuario]:
    session = _get_session()
    try:
        row = session.query(BotUsuario).filter(BotUsuario.chat_id == chat_id).first()
        if row:
            return Usuario(
                chat_id=row.chat_id,
                username=row.username,
                equipos=json.loads(row.equipos),
                activo=bool(row.activo),
            )
        return None
    finally:
        session.close()


def agregar_equipo(chat_id: int, equipo_id: int, equipo_nombre: str):
    session = _get_session()
    try:
        row = session.query(BotUsuario).filter(BotUsuario.chat_id == chat_id).first()
        if not row:
            row = BotUsuario(chat_id=chat_id)
            session.add(row)
            session.flush()

        equipos = json.loads(row.equipos)
        equipo_info = {"id": equipo_id, "nombre": equipo_nombre}
        if not any(e["id"] == equipo_id for e in equipos):
            equipos.append(equipo_info)
            row.equipos = json.dumps(equipos)
            session.commit()
    finally:
        session.close()


def eliminar_equipo(chat_id: int, equipo_id: int) -> list:
    session = _get_session()
    try:
        row = session.query(BotUsuario).filter(BotUsuario.chat_id == chat_id).first()
        if not row:
            return []
        equipos = json.loads(row.equipos)
        equipos = [e for e in equipos if e["id"] != equipo_id]
        row.equipos = json.dumps(equipos)
        session.commit()
        return equipos
    finally:
        session.close()


def obtener_todos_los_usuarios() -> list[Usuario]:
    session = _get_session()
    try:
        rows = session.query(BotUsuario).filter(BotUsuario.activo == True).all()
        return [
            Usuario(
                chat_id=row.chat_id,
                username=row.username,
                equipos=json.loads(row.equipos),
                activo=bool(row.activo),
            )
            for row in rows
        ]
    finally:
        session.close()


def verificar_evento_enviado(chat_id: int, evento_id: str) -> bool:
    session = _get_session()
    try:
        count = session.query(EventoEnviado).filter(
            EventoEnviado.chat_id == chat_id,
            EventoEnviado.evento_id == evento_id,
        ).count()
        return count > 0
    finally:
        session.close()


def registrar_evento_enviado(chat_id: int, evento_id: str, tipo: str):
    session = _get_session()
    try:
        session.add(EventoEnviado(chat_id=chat_id, evento_id=evento_id, tipo=tipo))
        session.commit()
    finally:
        session.close()


def verificar_noticia_enviada(chat_id: int, noticia_url: str) -> bool:
    session = _get_session()
    try:
        count = session.query(NoticiaEnviada).filter(
            NoticiaEnviada.chat_id == chat_id,
            NoticiaEnviada.noticia_url == noticia_url,
        ).count()
        return count > 0
    finally:
        session.close()


def registrar_noticia_enviada(chat_id: int, noticia_url: str):
    session = _get_session()
    try:
        existing = session.query(NoticiaEnviada).filter(
            NoticiaEnviada.noticia_url == noticia_url
        ).first()
        if not existing:
            session.add(NoticiaEnviada(chat_id=chat_id, noticia_url=noticia_url))
            session.commit()
    finally:
        session.close()


def programar_partido(chat_id: int, equipo_id: int, equipo_nombre: str,
                      fixture_id: str, fecha_utc: str, local: str,
                      visitante: str, liga: str):
    from datetime import datetime
    session = _get_session()
    try:
        existing = session.query(PartidoProgramado).filter(
            PartidoProgramado.fixture_id == fixture_id
        ).first()
        if not existing:
            try:
                fecha_dt = datetime.fromisoformat(fecha_utc.replace("Z", "+00:00"))
            except Exception:
                fecha_dt = datetime.utcnow()
            session.add(PartidoProgramado(
                chat_id=chat_id, equipo_id=equipo_id, equipo_nombre=equipo_nombre,
                fixture_id=fixture_id, fecha_utc=fecha_dt,
                local=local, visitante=visitante, liga=liga,
            ))
            session.commit()
    finally:
        session.close()


def obtener_partidos_para_chequear() -> list:
    session = _get_session()
    try:
        rows = session.query(PartidoProgramado).filter(
            PartidoProgramado.en_vivo == False
        ).all()
        return [_partido_to_tuple(r) for r in rows]
    finally:
        session.close()


def obtener_partidos_en_vivo() -> list:
    session = _get_session()
    try:
        rows = session.query(PartidoProgramado).filter(
            PartidoProgramado.en_vivo == True
        ).all()
        return [_partido_to_tuple(r) for r in rows]
    finally:
        session.close()


def _partido_to_tuple(r) -> tuple:
    return (
        r.id, r.chat_id, r.equipo_id, r.equipo_nombre, r.fixture_id,
        r.fecha_utc.isoformat() if r.fecha_utc else "",
        r.local, r.visitante, r.liga,
        1 if r.notificado_inicio else 0,
        1 if r.notificado_15min else 0,
        1 if r.notificado_manana else 0,
        1 if r.en_vivo else 0,
        r.goles_local, r.goles_visitante, r.estado, ""
    )


def marcar_partido_en_vivo(fixture_id: str):
    session = _get_session()
    try:
        session.query(PartidoProgramado).filter(
            PartidoProgramado.fixture_id == fixture_id
        ).update({"en_vivo": True})
        session.commit()
    finally:
        session.close()


def actualizar_estado_partido(fixture_id: str, estado: str,
                              goles_local: int, goles_visitante: int):
    session = _get_session()
    try:
        session.query(PartidoProgramado).filter(
            PartidoProgramado.fixture_id == fixture_id
        ).update({
            "estado": estado,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
        })
        session.commit()
    finally:
        session.close()


_CAMPO_MAP = {
    "notificado_inicio": "notificado_inicio",
    "notificado_15min": "notificado_15min",
    "notificado_manana": "notificado_manana",
    "notificado_lineup": "notificado_lineup",
    "notificado_ht": "notificado_ht",
    "notificado_2h": "notificado_2h",
}


def marcar_notificado(fixture_id: str, campo: str):
    col = _CAMPO_MAP.get(campo)
    if not col:
        return
    session = _get_session()
    try:
        session.query(PartidoProgramado).filter(
            PartidoProgramado.fixture_id == fixture_id
        ).update({col: True})
        session.commit()
    finally:
        session.close()


def verificar_notificado(fixture_id: str, campo: str) -> bool:
    col = _CAMPO_MAP.get(campo)
    if not col:
        return False
    session = _get_session()
    try:
        row = session.query(PartidoProgramado).filter(
            PartidoProgramado.fixture_id == fixture_id
        ).first()
        if row:
            return bool(getattr(row, col, False))
        return False
    finally:
        session.close()


def eliminar_partido(fixture_id: str):
    session = _get_session()
    try:
        session.query(PartidoProgramado).filter(
            PartidoProgramado.fixture_id == fixture_id
        ).delete()
        session.commit()
    finally:
        session.close()
