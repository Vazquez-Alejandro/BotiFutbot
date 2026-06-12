import sqlite3
import json
import os
from typing import Optional
from dataclasses import dataclass

DB_PATH = "data/botifutbol.db"


@dataclass
class Usuario:
    chat_id: int
    username: Optional[str]
    equipos: list
    activo: bool = True


def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            chat_id INTEGER PRIMARY KEY,
            username TEXT,
            equipos TEXT DEFAULT '[]',
            activo INTEGER DEFAULT 1,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos_enviados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            evento_id TEXT,
            tipo TEXT,
            enviado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES usuarios(chat_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS noticias_enviadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            noticia_url TEXT UNIQUE,
            enviado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidos_programados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            equipo_id INTEGER,
            equipo_nombre TEXT,
            fixture_id TEXT,
            fecha_utc TIMESTAMP,
            local TEXT,
            visitante TEXT,
            liga TEXT,
            notificado_inicio INTEGER DEFAULT 0,
            notificado_15min INTEGER DEFAULT 0,
            notificado_manana INTEGER DEFAULT 0,
            en_vivo INTEGER DEFAULT 0,
            goles_local INTEGER DEFAULT 0,
            goles_visitante INTEGER DEFAULT 0,
            estado TEXT DEFAULT '',
            enviado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES usuarios(chat_id)
        )
    """)
    conn.commit()
    conn.close()


def guardar_usuario(chat_id: int, username: Optional[str] = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (chat_id, username) VALUES (?, ?)",
        (chat_id, username),
    )
    conn.commit()
    conn.close()


def obtener_usuario(chat_id: int) -> Optional[Usuario]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Usuario(
            chat_id=row[0],
            username=row[1],
            equipos=json.loads(row[2]),
            activo=bool(row[3]),
        )
    return None


def agregar_equipo(chat_id: int, equipo_id: int, equipo_nombre: str):
    usuario = obtener_usuario(chat_id)
    if not usuario:
        guardar_usuario(chat_id)
        usuario = obtener_usuario(chat_id)

    equipos = usuario.equipos
    equipo_info = {"id": equipo_id, "nombre": equipo_nombre}
    if not any(e["id"] == equipo_id for e in equipos):
        equipos.append(equipo_info)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET equipos = ? WHERE chat_id = ?",
            (json.dumps(equipos), chat_id),
        )
        conn.commit()
        conn.close()
    return equipos


def eliminar_equipo(chat_id: int, equipo_id: int) -> list:
    usuario = obtener_usuario(chat_id)
    if not usuario:
        return []

    equipos = [e for e in usuario.equipos if e["id"] != equipo_id]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET equipos = ? WHERE chat_id = ?",
        (json.dumps(equipos), chat_id),
    )
    conn.commit()
    conn.close()
    return equipos


def obtener_todos_los_usuarios() -> list[Usuario]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE activo = 1")
    rows = cursor.fetchall()
    conn.close()
    return [
        Usuario(
            chat_id=row[0],
            username=row[1],
            equipos=json.loads(row[2]),
            activo=bool(row[3]),
        )
        for row in rows
    ]


def verificar_evento_enviado(chat_id: int, evento_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM eventos_enviados WHERE chat_id = ? AND evento_id = ?",
        (chat_id, evento_id),
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def registrar_evento_enviado(chat_id: int, evento_id: str, tipo: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO eventos_enviados (chat_id, evento_id, tipo) VALUES (?, ?, ?)",
        (chat_id, evento_id, tipo),
    )
    conn.commit()
    conn.close()


def verificar_noticia_enviada(chat_id: int, noticia_url: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM noticias_enviadas WHERE chat_id = ? AND noticia_url = ?",
        (chat_id, noticia_url),
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def registrar_noticia_enviada(chat_id: int, noticia_url: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO noticias_enviadas (chat_id, noticia_url) VALUES (?, ?)",
            (chat_id, noticia_url),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def programar_partido(chat_id: int, equipo_id: int, equipo_nombre: str,
                      fixture_id: str, fecha_utc: str, local: str,
                      visitante: str, liga: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT OR IGNORE INTO partidos_programados
           (chat_id, equipo_id, equipo_nombre, fixture_id, fecha_utc,
            local, visitante, liga)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (chat_id, equipo_id, equipo_nombre, fixture_id, fecha_utc,
         local, visitante, liga),
    )
    conn.commit()
    conn.close()


def obtener_partidos_para_chequear() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM partidos_programados WHERE en_vivo = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows


def obtener_partidos_en_vivo() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM partidos_programados WHERE en_vivo = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows


def marcar_partido_en_vivo(fixture_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE partidos_programados SET en_vivo = 1 WHERE fixture_id = ?",
        (fixture_id,),
    )
    conn.commit()
    conn.close()


def actualizar_estado_partido(fixture_id: str, estado: str,
                              goles_local: int, goles_visitante: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE partidos_programados
           SET estado = ?, goles_local = ?, goles_visitante = ?
           WHERE fixture_id = ?""",
        (estado, goles_local, goles_visitante, fixture_id),
    )
    conn.commit()
    conn.close()


def marcar_notificado(fixture_id: str, campo: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE partidos_programados SET {campo} = 1 WHERE fixture_id = ?",
        (fixture_id,),
    )
    conn.commit()
    conn.close()


def verificar_notificado(fixture_id: str, campo: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {campo} FROM partidos_programados WHERE fixture_id = ?",
        (fixture_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else False


def eliminar_partido(fixture_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM partidos_programados WHERE fixture_id = ?",
        (fixture_id,),
    )
    conn.commit()
    conn.close()
