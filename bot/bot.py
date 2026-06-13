import logging
from datetime import datetime, timedelta, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)
from src.config import TELEGRAM_TOKEN, API_FOOTBALL_KEY
from src.database import (
    init_db, obtener_todos_los_usuarios, obtener_usuario,
    programar_partido, obtener_partidos_para_chequear, obtener_partidos_en_vivo,
    marcar_partido_en_vivo, actualizar_estado_partido, marcar_notificado,
    verificar_notificado, eliminar_partido,
    verificar_noticia_enviada, registrar_noticia_enviada,
    agregar_equipo, eliminar_equipo,
)
from src.api_client import football_client
from src.handlers import (
    start, mis_equipos, buscar_equipo,
    seleccionar_continente, seleccionar_pais, seleccionar_liga,
    agregar_equipo_handler, eliminar_equipo_handler,
    noticias, ayuda, menu_principal,
    cmd_equipos, cmd_buscar, cmd_noticias, cmd_stats,
)
from src.analytics import init_analytics, registrar_evento

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

AFILIADOS = {
    "bet365": {"nombre": "Bet365", "texto": "🎲 Pronosticá con los mejores → Bet365"},
    "betano": {"nombre": "Betano", "texto": "🔥 Seguí las cuotas en vivo → Betano"},
}


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
                    if not fixture_id or not fecha_str:
                        continue
                    if verificar_notificado(fixture_id, "notificado_manana"):
                        continue
                    try:
                        fecha_dt = datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
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
                    registrar_evento("fixture_sync", {"equipo": equipo["nombre"], "fixture": fixture_id})

    except Exception as e:
        logger.error(f"Error en sync_fixtures: {e}")


async def enviar_con_afiliado(app, chat_id: int, texto: str, parse_mode="Markdown"):
    try:
        await app.send_message(chat_id=chat_id, text=texto, parse_mode=parse_mode)

        if chat_id % 3 == 0:
            afiliado = AFILIADOS["bet365"]
            await app.send_message(
                chat_id=chat_id,
                text=f"{afiliado['texto']}\n🔗 https://www.bet365.com/?aff={chat_id}",
                disable_web_page_preview=True,
            )
    except Exception as e:
        logger.error(f"Error enviar con afiliado: {e}")


async def resumen_diario(context: ContextTypes.DEFAULT_TYPE):
    try:
        app = context.bot
        usuarios = obtener_todos_los_usuarios()
        now = datetime.now(timezone.utc)

        for usuario in usuarios:
            if not usuario.equipos:
                continue
            partidos_hoy = []
            for equipo in usuario.equipos:
                try:
                    partidos = football_client.obtener_proximos_partidos(equipo["id"])
                except Exception:
                    continue
                for p in partidos:
                    fixture = p.get("fixture", {})
                    fecha_str = fixture.get("date", "")
                    if not fecha_str:
                        continue
                    try:
                        fecha_dt = datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
                    except Exception:
                        continue

                    if fecha_dt.date() == now.date():
                        local = p.get("teams", {}).get("home", {}).get("name", "")
                        visitante = p.get("teams", {}).get("away", {}).get("name", "")
                        hora = fecha_dt.astimezone(timezone(timedelta(hours=-3))).strftime("%H:%M")
                        liga = fixture.get("league", {}).get("name", "")
                        partidos_hoy.append(f"• {local} vs {visitante} — {hora} ({liga})")

            if partidos_hoy:
                usuario_data = obtener_usuario(usuario.chat_id)
                nombre = usuario_data.username or "amigo"
                msg = (
                    f"🌅 *¡Buenos días {nombre}!*\n\n"
                    f"📅 *Resumen del día:*\n"
                    + "\n".join(partidos_hoy) +
                    "\n\n⚽ Que tengas un gran día de fútbol!"
                )
                await enviar_con_afiliado(app, usuario.chat_id, msg)

    except Exception as e:
        logger.error(f"Error resumen diario: {e}")


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

            # Notificación de alineación (1 hora antes)
            if diff > 0 and diff <= 60 * 60 and diff > 15 * 60 and not verificar_notificado(fixture_id, "notificado_lineup"):
                try:
                    fixture_data = football_client.obtener_fixture_por_id(int(fixture_id))
                    if fixture_data:
                        events = fixture_data.get("events", [])
                        lineup_home = [e for e in events if e.get("type") == "Lineup" and e.get("team", {}).get("id") == equipo_id]
                        if lineup_home:
                            await enviar_con_afiliado(
                                app, chat_id,
                                f"📋 *Alineación confirmada!*\n\n"
                                f"⚽ {local} vs {visitante}\n"
                                f"🏆 {liga}\n\n"
                                f"Ya se conocen los titulares. ¿Vamos con pronóstico? 🤔"
                            )
                            marcar_notificado(fixture_id, "notificado_lineup")
                            registrar_evento("lineup_notified", {"fixture": fixture_id, "equipo": equipo_nombre})
                except Exception as e:
                    logger.error(f"Error lineup: {e}")

            # Recordatorio mañana (24h antes hasta 30min antes)
            if diff > 30 * 60 and not verificar_notificado(fixture_id, "notificado_manana"):
                try:
                    hora_local = fecha_dt.astimezone(timezone(timedelta(hours=-3))).strftime("%H:%M")
                    await enviar_con_afiliado(
                        app, chat_id,
                        f"🌅 *Recordatorio!*\n\n"
                        f"⚽ {local} vs {visitante}\n"
                        f"🏆 {liga}\n"
                        f"🕐 *{hora_local}* (hora ARG)\n\n"
                        f"💡 ¿Ya hiciste tu predicción? Tu equipo quiere verte ganar.",
                    )
                    marcar_notificado(fixture_id, "notificado_manana")
                    registrar_evento("match_reminder", {"fixture": fixture_id, "diff_hours": diff / 3600})
                except Exception as e:
                    logger.error(f"Error recordatorio: {e}")

            # 15 minutos antes
            if diff > 0 and diff <= 15 * 60 and not verificar_notificado(fixture_id, "notificado_15min"):
                try:
                    await enviar_con_afiliado(
                        app, chat_id,
                        f"⏰ *¡Faltan 15 minutos!*\n\n"
                        f"⚽ *{local}* vs *{visitante}*\n"
                        f"🏆 {liga}\n\n"
                        f"🔥 Última chance para pronosticar!",
                    )
                    marcar_notificado(fixture_id, "notificado_15min")
                    registrar_evento("15min_alert", {"fixture": fixture_id})
                except Exception as e:
                    logger.error(f"Error 15min: {e}")

            # Inicio del partido
            if diff <= 0 and not verificar_notificado(fixture_id, "notificado_inicio"):
                try:
                    await enviar_con_afiliado(
                        app, chat_id,
                        f"🟢 *¡Comenzó el partido!*\n\n"
                        f"⚽ {local} vs {visitante}\n"
                        f"🏆 {liga}\n\n"
                        f"📊 Seguilo en vivo y no te pierdas ningún gol.",
                    )
                    marcar_notificado(fixture_id, "notificado_inicio")
                    marcar_partido_en_vivo(fixture_id)
                    registrar_evento("match_started", {"fixture": fixture_id})
                except Exception as e:
                    logger.error(f"Error inicio: {e}")

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
                partidos_data = football_client.obtener_partidos_en_vivo_por_equipo(equipo_id)
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
            goles_local_actual = partido_actual.get("goals", {}).get("home", 0) or 0
            goles_visitante_actual = partido_actual.get("goals", {}).get("away", 0) or 0
            minuto = fixture.get("status", {}).get("elapsed", 0)

            goles_anteriores = gl + gv
            goles_actuales = goles_local_actual + goles_visitante_actual

            if estado_actual in ("FT", "AET", "PEN"):
                try:
                    resultado = f"*{local}* {goles_local_actual} - {goles_visitante_actual} *{visitante}*"
                    await enviar_con_afiliado(
                        app, chat_id,
                        f"🏁 *¡Final del partido!*\n\n{resultado}\n\n🏆 {liga}\n\n"
                        f"📊 ¿Acertaste el resultado? Seguí sumando puntos en el próximo!",
                    )
                    eliminar_partido(fixture_id)
                    registrar_evento("match_ended", {"fixture": fixture_id, "resultado": resultado})
                except Exception as e:
                    logger.error(f"Error final: {e}")
                continue

            if estado_actual == "HT" and not verificar_notificado(fixture_id, "notificado_ht"):
                try:
                    await enviar_con_afiliado(
                        app, chat_id,
                        f"⏸️ *Medio tiempo*\n\n"
                        f"*{local}* {goles_local_actual} - {goles_visitante_actual} *{visitante}*\n"
                        f"⏱️ Minuto {minuto}'\n\n"
                        f"¿Qué esperás para el segundo tiempo? 🤔",
                    )
                    marcar_notificado(fixture_id, "notificado_ht")
                    registrar_evento("halftime", {"fixture": fixture_id})
                except Exception as e:
                    logger.error(f"Error HT: {e}")

            if estado_actual == "2H" and verificar_notificado(fixture_id, "notificado_ht") \
                    and not verificar_notificado(fixture_id, "notificado_2h"):
                try:
                    await enviar_con_afiliado(
                        app, chat_id,
                        f"▶️ *¡Comenzó el segundo tiempo!*\n\n"
                        f"⚽ {local} {goles_local_actual} - {goles_visitante_actual} {visitante}\n"
                        f"⏱️ {minuto}'",
                    )
                    marcar_notificado(fixture_id, "notificado_2h")
                except Exception as e:
                    logger.error(f"Error 2H: {e}")

            if goles_actuales > goles_anteriores:
                try:
                    goles_nuevos = goles_actuales - goles_anteriores
                    for _ in range(goles_nuevos):
                        await enviar_con_afiliado(
                            app, chat_id,
                            f"⚽ *¡GOOOOOOL!*\n\n"
                            f"*{local}* {goles_local_actual} - {goles_visitante_actual} *{visitante}*\n"
                            f"⏱️ Minuto {minuto}'\n\n"
                            f"🔥 Vamos que esto no termina acá!",
                        )
                        registrar_evento("goal_scored", {"fixture": fixture_id})
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
                        await enviar_con_afiliado(
                            app, chat_id,
                            f"🟥 *¡TARJETA ROJA!*\n\n"
                            f"👤 {ev_player}\n"
                            f"📍 {ev_team}\n"
                            f"⏱️ Minuto {ev_time}'\n\n"
                            f"Partido que se pone picante 🔥",
                        )
                        marcar_notificado(ev_key, "notificado_")
                        registrar_evento("red_card", {"fixture": fixture_id, "player": ev_player})

                    elif ev_detail in ("Yellow Card",):
                        msg = (
                            f"🟨 *Tarjeta amarilla*\n\n"
                            f"👤 {ev_player}\n"
                            f"📍 {ev_team}\n"
                            f"⏱️ Minuto {ev_time}'"
                        )
                        await app.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
                        marcar_notificado(ev_key, "notificado_")

                    elif ev_detail == "Penalty" and ev_tipo == "Goal":
                        await enviar_con_afiliado(
                            app, chat_id,
                            f"🥅 *¡PENAL Y GOL!*\n\n"
                            f"⚽ {ev_player}\n"
                            f"📍 {ev_team}\n"
                            f"⏱️ Minuto {ev_time}'\n\n"
                            f"Nervios de acero 🧊",
                        )
                        marcar_notificado(ev_key, "notificado_")
                        registrar_evento("penalty_goal", {"fixture": fixture_id})

                    elif ev_detail == "Missed Penalty":
                        await app.send_message(
                            chat_id=chat_id,
                            text=f"😱 *¡PENAL ERRADO!*\n\n👤 {ev_player}\n📍 {ev_team}\n⏱️ Minuto {ev_time}'",
                            parse_mode="Markdown",
                        )
                        marcar_notificado(ev_key, "notificado_")

            except Exception as e:
                logger.error(f"Error eventos: {e}")

            actualizar_estado_partido(
                fixture_id, estado_actual,
                goles_local_actual, goles_visitante_actual,
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
                        f"📰 *Noticia - {equipo['nombre']}*\n\n"
                        f"*{titulo}*\n\n"
                        f"📡 {fuente}\n🔗 {url}"
                    )
                    try:
                        await app.send_message(
                            chat_id=usuario.chat_id, text=msg, parse_mode="Markdown",
                        )
                        registrar_noticia_enviada(usuario.chat_id, url)
                        registrar_evento("news_sent", {"equipo": equipo["nombre"], "url": url})
                    except Exception as e:
                        logger.error(f"Error noticia: {e}")
    except Exception as e:
        logger.error(f"Error en check_news: {e}")


async def resumen_semanal(context: ContextTypes.DEFAULT_TYPE):
    try:
        app = context.bot
        usuarios = obtener_todos_los_usuarios()
        for usuario in usuarios:
            if not usuario.equipos:
                continue
            equipos_str = ", ".join(e["nombre"] for e in usuario.equipos)
            total_partidos = len(obtener_partidos_para_chequear())

            msg = (
                f"📊 *Resumen semanal - BotifutBot*\n\n"
                f"⚽ Equipos seguidos: {len(usuario.equipos)}\n"
                f"📅 Próximos partidos: {total_partidos}\n"
                f"🏆 Ligas disponibles: 7 países\n\n"
                f"Seguí toda la acción y no te pierdas ningún gol ⚽\n\n"
                f"📱 También podés seguir tus equipos en la web: botifutbol.app"
            )
            try:
                await app.send_message(chat_id=usuario.chat_id, text=msg, parse_mode="Markdown")
            except Exception:
                continue
    except Exception as e:
        logger.error(f"Error resumen semanal: {e}")


async def cmd_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        "👑 *BotifutBot Premium*\n\n"
        "🔹 *Gratuito:* 3 equipos, notificaciones cada 60s, anuncios\n"
        "🔹 *Premium ($499/mes):* 20 equipos, tiempo real, sin anuncios, predicciones\n"
        "🔹 *Pro ($999/mes):* Ilimitado, API access, webhooks\n\n"
        "💎 *Beneficios exclusivos:*\n"
        "• Notificaciones instantáneas de goles\n"
        "• Estadísticas avanzadas de jugadores\n"
        "• Competí con amigos y ganá puntos\n"
        "• Sin publicidad\n\n"
        "📲 Suscribite desde la app: https://botifutbol.app/premium",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def cmd_afiliados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        "💰 *Programa de Afiliados*\n\n"
        "Compartí tus enlaces y ganá comisiones:\n\n"
        "🎲 *Bet365* — 20% comisión\n"
        "🔥 *Betano* — 25% comisión\n"
        "⚽ *Sportingbet* — 15% comisión\n\n"
        f"Tu ID de afiliado: `{chat_id}`\n\n"
        "Compartí este link con tus amigos:\n"
        f"🔗 https://t.me/BotiFutBot?start=ref_{chat_id}",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def cmd_live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    partidos = football_client.obtener_partidos_en_vivo()
    if not partidos:
        await update.message.reply_text("🔴 No hay partidos en vivo en este momento.")
        return

    msg = "🔴 *Partidos en vivo:*\n\n"
    for p in partidos[:10]:
        fixture = p.get("fixture", {})
        teams = p.get("teams", {})
        goals = p.get("goals", {})
        elapsed = fixture.get("status", {}).get("elapsed", 0)
        local = teams.get("home", {}).get("name", "")
        visit = teams.get("away", {}).get("name", "")
        goles = f"{goals.get('home', 0)} - {goals.get('away', 0)}"
        msg += f"⚽ {local} {goles} {visit} ({elapsed}')\n"

    await update.message.reply_text(msg, parse_mode="Markdown")


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
    app.add_handler(CommandHandler("premium", cmd_premium))
    app.add_handler(CommandHandler("afiliados", cmd_afiliados))
    app.add_handler(CommandHandler("live", cmd_live))

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
    job_queue.run_daily(resumen_diario, time=timezone.utc, days=(0, 1, 2, 3, 4, 5, 6))
    job_queue.run_weekly(resumen_semanal, day_of_week=0, time=timezone.utc)

    logger.info("BotifutBot está corriendo! 🚀")
    app.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
