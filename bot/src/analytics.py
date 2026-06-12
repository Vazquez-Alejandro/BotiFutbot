import sqlite3
from datetime import datetime, timedelta
from typing import Optional

DB_PATH = "data/botifutbol.db"


def init_analytics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            accion TEXT,
            detalle TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metricas_diarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            usuarios_nuevos INTEGER DEFAULT 0,
            usuarios_activos INTEGER DEFAULT 0,
            clicks_links INTEGER DEFAULT 0,
            conversiones INTEGER DEFAULT 0,
            mensajes_enviados INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def registrar_accion(chat_id: int, accion: str, detalle: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analytics (chat_id, accion, detalle) VALUES (?, ?, ?)",
        (chat_id, accion, detalle),
    )

    hoy = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT id FROM metricas_diarias WHERE fecha = ?", (hoy,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO metricas_diarias (fecha) VALUES (?)", (hoy,))

    if accion == "usuario_nuevo":
        cursor.execute(
            "UPDATE metricas_diarias SET usuarios_nuevos = usuarios_nuevos + 1 WHERE fecha = ?",
            (hoy,),
        )
    elif accion == "click_link":
        cursor.execute(
            "UPDATE metricas_diarias SET clicks_links = clicks_links + 1 WHERE fecha = ?",
            (hoy,),
        )
    elif accion == "conversion":
        cursor.execute(
            "UPDATE metricas_diarias SET conversiones = conversiones + 1 WHERE fecha = ?",
            (hoy,),
        )
    elif accion in ("start", "buscar", "noticias", "equipos"):
        cursor.execute(
            "UPDATE metricas_diarias SET usuarios_activos = usuarios_activos + 1 WHERE fecha = ?",
            (hoy,),
        )

    conn.commit()
    conn.close()


def obtener_usuarios_activos(dias: int = 7) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT COUNT(DISTINCT chat_id) FROM analytics WHERE created_at >= ?",
        (fecha_limite,),
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


def obtener_total_usuarios() -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def obtener_clicks_links(dias: int = 30) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT COUNT(*) FROM analytics WHERE accion = 'click_link' AND created_at >= ?",
        (fecha_limite,),
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


def obtener_conversiones(dias: int = 30) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT COUNT(*) FROM analytics WHERE accion = 'conversion' AND created_at >= ?",
        (fecha_limite,),
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


def obtener_metricas_diarias(dias: int = 7) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT * FROM metricas_diarias WHERE fecha >= ? ORDER BY fecha DESC",
        (fecha_limite,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "fecha": r[1],
            "usuarios_nuevos": r[2],
            "usuarios_activos": r[3],
            "clicks_links": r[4],
            "conversiones": r[5],
            "mensajes_enviados": r[6],
        }
        for r in rows
    ]


def obtener_top_equipos(limit: int = 5) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT equipos FROM usuarios WHERE activo = 1")
    rows = cursor.fetchall()
    conn.close()

    conteo = {}
    for row in rows:
        import json

        equipos = json.loads(row[0])
        for eq in equipos:
            nombre = eq.get("nombre", "")
            conteo[nombre] = conteo.get(nombre, 0) + 1

    ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    return ordenados[:limit]
