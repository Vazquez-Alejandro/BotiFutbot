import logging
from datetime import datetime, timedelta, timezone
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from src.config import TELEGRAM_TOKEN
from src.database import (
    init_db, obtener_todos_los_usuarios, obtener_usuario,
    programar_partido, obtener_partidos_para_chequear, obtener_partidos_en_vivo,
    marcar_partido_en_vivo, actualizar_estado_partido, marcar_notificado,
    verificar_notificado, eliminar_partido,
    verificar_noticia_enviada, registrar_noticia_enviada,
)
from src.api_client import football_client
from src.handlers import (
    start, mis_equipos, buscar_equipo,
    seleccionar_continente, seleccionar_pais, seleccionar_liga,
    agregar_equipo_handler, eliminar_equipo_handler,
    noticias, ayuda, menu_principal,
    cmd_equipos, cmd_buscar, cmd_noticias, cmd_stats,
)
from src.analytics import init_analytics

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception: {context.error}")


async def sync_fixtures(context: ContextTypes.DEFAULT_TYPE):
    try:
        usuarios = obtener_todos_los_usuarios()
        for usuario in usuarios:
            if not usuario.equipos:
                continue
            for equipo in usuario.equipos:
                try:
                    partidos = football_client.obtener_proximos_partidos(equipo["id"])
                except Exception:
                    continue

                for p in partidos:
                    fixture = p.get("fixture", {})
                    fixture_id = str(fixture.get("id", ""))
                    fecha_str = fixture.get("date", "")
                    estado = fixture.get("status", {}).get("short", "")

                    if not fixture_id or not fecha_str:
                        continue

                    if verificar_notificado(fixture_id, "notificado_manana"):
                        continue

                    try:
                        fecha_dt = datetime.fromisoformat(
                            fecha_str.replace("Z", "+00:00")
                        )
                    except Exception:
                        continue

                    local = p.get("teams", {}).get("home", {}).get("name", "")
                    visitante = p.get("teams", {}).get("away", {}).get("name", "")
                    liga = fixture.get("league", {}).get("name", "")

                    programar_partido(
                        chat_id=usuario.chat_id,
                        equipo_id=equipo["id"],
                        equipo_nombre=equipo["nombre"],
                        fixture_id=fixture_id,
                        fecha_utc=fecha_str,
                        local=local,
                        visitante=visitante,
                        liga=liga,
                    )

    except Exception as e:
        logger.error(f"Error en sync_fixtures: {e}")


async def check_match_notifications(context: ContextTypes.DEFAULT_TYPE):
    try:
        app = context.bot
        now = datetime.now(timezone.utc)
        partidos = obtener_partidos_para_chequear()

        for row in partidos:
            _id, chat_id, equipo_id, equipo_nombre, fixture_id, fecha_utc, \
                local, visitante, liga, not_ini, not_15, not_man, \
                en_vivo, gl, gv, estado, _env = row

            try:
                fecha_dt = datetime.fromisoformat(fecha_utc.replace("Z", "+00:00"))
            except Exception:
                continue

            diff = (fecha_dt - now).total_seconds()
            usuario = obtener_usuario(chat_id)
            nombre = usuario.username if usuario else "amigo"

            if diff > 0 and diff <= 30 * 60 and not verificar_notificado(fixture_id, "notificado_manana"):
                if 0 < diff <= 24 * 60 * 60:
                    try:
                        hora_local = fecha_dt.astimezone(
                            timezone(timedelta(hours=-3))
                        ).strftime("%H:%H")
                        await app.send_message(
                            chat_id=chat_id,
                            text=(
                                f"🌅 ¡Buenos días {nombre}!\n\n"
                                f"Acordate que hoy juega *{equipo_nombre}*\n"
                                f"📍 {local} vs {visitante}\n"
                                f"🏆 {liga}\n"
                                f"🕐 A las {hora_local} (hora ARG)"
                            ),
                            parse_mode="Markdown",
                        )
                        marcar_notificado(fixture_id, "notificado_manana")
                    except Exception as e:
                        logger.error(f"Error notificación mañana: {e}")

            if diff > 0 and diff <= 15 * 60 and diff > 0 and not verificar_notificado(fixture_id, "notificado_15min"):
                try:
                    await app.send_message(
                        chat_id=chat_id,
                        text=(
                            f"⏰ *Faltan 15 minutos!*\n\n"
                            f"⚽ {local} vs {visitante}\n"
                            f"🏆 {liga}"
                        ),
                        parse_mode="Markdown",
                    )
                    marcar_notificado(fixture_id, "notificado_15min")
                except Exception as e:
                    logger.error(f"Error notificación 15min: {e}")

            if diff <= 0 and not verificar_notificado(fixture_id, "notificado_inicio"):
                try:
                    await app.send_message(
                        chat_id=chat_id,
                        text=(
                            f"🟢 *¡Comenzó el partido!*\n\n"
                            f"⚽ {local} vs {visitante}\n"
                            f"🏆 {liga}"
                        ),
                        parse_mode="Markdown",
                    )
                    marcar_notificado(fixture_id, "notificado_inicio")
                    marcar_partido_en_vivo(fixture_id)
                except Exception as e:
                    logger.error(f"Error notificación inicio: {e}")

    except Exception as e:
        logger.error(f"Error en check_match_notifications: {e}")


async def check_live_matches(context: ContextTypes.DEFAULT_TYPE):
    try:
        app = context.bot
        partidos = obtener_partidos_en_vivo()

        for row in partidos:
            _id, chat_id, equipo_id, equipo_nombre, fixture_id, fecha_utc, \
                local, visitante, liga, not_ini, not_15, not_man, \
                en_vivo, gl, gv, estado, _env = row

            try:
                partidos_data = football_client.obtener_partidos_en_vivo_por_equipo(
                    equipo_id
                )
            except Exception:
                continue

            partido_actual = None
            for p in partidos_data:
                f_id = str(p.get("fixture", {}).get("id", ""))
                if f_id == fixture_id:
                    partido_actual = p
                    break

            if not partido_actual:
                continue

            fixture = partido_actual.get("fixture", {})
            estado_actual = fixture.get("status", {}).get("short", "")
            goles_local_actual = partido_actual.get("goals", {}).get("home", 0)
            goles_visitante_actual = partido_actual.get("goals", {}).get("away", 0)
            minuto = fixture.get("status", {}).get("elapsed", 0)

            goles_anteriores = gl + gv
            goles_actuales = goles_local_actual + goles_visitante_actual

            if estado_actual == "FT":
                try:
                    await app.send_message(
                        chat_id=chat_id,
                        text=(
                            f"🏁 *¡Final del partido!*\n\n"
                            f"*{local}* {goles_local_actual} - {goles_visitante_actual} *{visitante}*\n\n"
                            f"🏆 {liga}"
                        ),
                        parse_mode="Markdown",
                    )
                    eliminar_partido(fixture_id)
                except Exception as e:
                    logger.error(f"Error final: {e}")
                continue

            if estado_actual == "HT" and not verificar_notificado(fixture_id, "notificado_ht"):
                try:
                    await app.send_message(
                        chat_id=chat_id,
                        text=(
                            f"⏸️ *Medio tiempo*\n\n"
                            f"*{local}* {goles_local_actual} - {goles_visitante_actual} *{visitante}*\n"
                            f"⏱️ Minuto {minuto}'"
                        ),
                        parse_mode="Markdown",
                    )
                    marcar_notificado(fixture_id, "notificado_ht")
                except Exception as e:
                    logger.error(f"Error HT: {e}")

            if estado_actual == "2H" and verificar_notificado(fixture_id, "notificado_ht") \
                    and not verificar_notificado(fixture_id, "notificado_2h"):
                try:
                    await app.send_message(
                        chat_id=chat_id,
                        text="▶️ *Comienza el segundo tiempo!*",
                        parse_mode="Markdown",
                    )
                    marcar_notificado(fixture_id, "notificado_2h")
                except Exception as e:
                    logger.error(f"Error 2H: {e}")

            if goles_actuales > goles_anteriores:
                try:
                    goles_nuevos = goles_actuales - goles_anteriores
                    for _ in range(goles_nuevos):
                        await app.send_message(
                            chat_id=chat_id,
                            text=(
                                f"⚽ *¡GOOOOOOL!*\n\n"
                                f"*{local}* {goles_local_actual} - {goles_visitante_actual} *{visitante}*\n"
                                f"⏱️ Minuto {minuto}'"
                            ),
                            parse_mode="Markdown",
                        )
                except Exception as e:
                    logger.error(f"Error gol: {e}")

            try:
                eventos = football_client.obtener_eventos_partido(int(fixture_id))
                for ev in eventos:
                    ev_tipo = ev.get("type", "")
                    ev_detail = ev.get("detail", "")
                    ev_team = ev.get("team", {}).get("name", "")
                    ev_player = ev.get("player", {}).get("name", "")
                    ev_time = ev.get("time", {}).get("elapsed", 0)
                    ev_key = f"{fixture_id}_{ev_tipo}_{ev_detail}_{ev_time}"

                    if verificar_notificado(ev_key, "notificado_"):
                        continue

                    if ev_detail == "Red Card":
                        await app.send_message(
                            chat_id=chat_id,
                            text=(
                                f"🟥 *¡TARJETA ROJA!*\n\n"
                                f"👤 {ev_player}\n"
                                f"📍 {ev_team}\n"
                                f"⏱️ Minuto {ev_time}'"
                            ),
                            parse_mode="Markdown",
                        )
                        marcar_notificado(ev_key, "notificado_")

                    elif ev_detail == "Penalty" and ev_tipo == "Goal":
                        await app.send_message(
                            chat_id=chat_id,
                            text=(
                                f"🥅 *¡PENAL!*\n\n"
                                f"⚽ {ev_player}\n"
                                f"📍 {ev_team}\n"
                                f"⏱️ Minuto {ev_time}'"
                            ),
                            parse_mode="Markdown",
                        )
                        marcar_notificado(ev_key, "notificado_")

            except Exception as e:
                logger.error(f"Error eventos: {e}")

            actualizar_estado_partido(
                fixture_id, estado_actual,
                goles_local_actual, goles_visitante_actual
            )

    except Exception as e:
        logger.error(f"Error en check_live_matches: {e}")


async def check_news(context: ContextTypes.DEFAULT_TYPE):
    try:
        from src.news_client import news_client
        app = context.bot
        usuarios = obtener_todos_los_usuarios()
        for usuario in usuarios:
            if not usuario.equipos:
                continue
            for equipo in usuario.equipos:
                try:
                    articulos = news_client.obtener_noticias_equipo(
                        equipo["nombre"], page_size=3
                    )
                except Exception:
                    continue
                for art in articulos:
                    url = art.get("url", "")
                    if not url or verificar_noticia_enviada(usuario.chat_id, url):
                        continue
                    titulo = art.get("titulo", "Sin título")
                    fuente = art.get("fuente", "")
                    msg = (
                        f"📰 *Nueva noticia - {equipo['nombre']}*\n\n"
                        f"*{titulo}*\n\n"
                        f"📡 {fuente}\n🔗 {url}"
                    )
                    try:
                        await app.send_message(
                            chat_id=usuario.chat_id,
                            text=msg,
                            parse_mode="Markdown",
                        )
                        registrar_noticia_enviada(usuario.chat_id, url)
                    except Exception as e:
                        logger.error(f"Error noticia: {e}")
    except Exception as e:
        logger.error(f"Error en check_news: {e}")


def main():
    init_db()
    init_analytics()
    logger.info("Iniciando BotifutBot...")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("equipos", cmd_equipos))
    app.add_handler(CommandHandler("buscar", cmd_buscar))
    app.add_handler(CommandHandler("noticias", cmd_noticias))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("stats", cmd_stats))

    app.add_handler(CallbackQueryHandler(menu_principal, pattern="^menu_principal$"))
    app.add_handler(CallbackQueryHandler(mis_equipos, pattern="^mis_equipos$"))
    app.add_handler(CallbackQueryHandler(buscar_equipo, pattern="^buscar_equipo$"))
    app.add_handler(CallbackQueryHandler(seleccionar_continente, pattern="^cont_"))
    app.add_handler(CallbackQueryHandler(seleccionar_pais, pattern="^pais_"))
    app.add_handler(CallbackQueryHandler(seleccionar_liga, pattern="^liga_"))
    app.add_handler(CallbackQueryHandler(noticias, pattern="^noticias$"))
    app.add_handler(CallbackQueryHandler(ayuda, pattern="^ayuda$"))
    app.add_handler(CallbackQueryHandler(agregar_equipo_handler, pattern="^agregar_"))
    app.add_handler(CallbackQueryHandler(eliminar_equipo_handler, pattern="^eliminar_"))

    app.add_error_handler(error_handler)

    job_queue = app.job_queue
    job_queue.run_repeating(sync_fixtures, interval=6 * 60 * 60, first=10)
    job_queue.run_repeating(check_match_notifications, interval=60, first=15)
    job_queue.run_repeating(check_live_matches, interval=60, first=30)
    job_queue.run_repeating(check_news, interval=30 * 60, first=60)

    logger.info("BotifutBot está corriendo! 🚀")
    app.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
