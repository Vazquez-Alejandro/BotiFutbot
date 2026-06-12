from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.config import CONTINENTES, PAISES_POR_CONTINENTE, EQUIPOS_POR_LIGA
from src.database import (
    guardar_usuario,
    obtener_usuario,
    agregar_equipo,
    eliminar_equipo,
)
from src.api_client import football_client
from src.news_client import news_client
from src.analytics import (
    registrar_accion,
    obtener_usuarios_activos,
    obtener_total_usuarios,
    obtener_clicks_links,
    obtener_conversiones,
    obtener_top_equipos,
)


def keyboard_menu_principal():
    return [
        [InlineKeyboardButton("⚽ Mis Equipos", callback_data="mis_equipos")],
        [InlineKeyboardButton("🔍 Buscar Equipo", callback_data="buscar_equipo")],
        [InlineKeyboardButton("📰 Noticias", callback_data="noticias")],
        [InlineKeyboardButton("ℹ️ Ayuda", callback_data="ayuda")],
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    usuario_existente = obtener_usuario(user.id)
    guardar_usuario(user.id, user.username)
    if not usuario_existente:
        registrar_accion(user.id, "usuario_nuevo", user.username or "")
    registrar_accion(user.id, "start")

    reply_markup = InlineKeyboardMarkup(keyboard_menu_principal())
    mensaje = (
        f"¡Hola {user.first_name}! 👋\n\n"
        "Soy *BotifutBot* ⚽, tu asistente personal de fútbol.\n\n"
        "Te enviaré noticias y actualizaciones de los equipos que elijas.\n\n"
        "Elegí una opción del menú para comenzar:"
    )
    await update.message.reply_text(
        mensaje, reply_markup=reply_markup, parse_mode="Markdown"
    )


async def menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(keyboard_menu_principal())
    await query.edit_message_text("Menú principal:", reply_markup=reply_markup)


# ─── FLUJO DE BÚSQUEDA: Continente → País → Liga → Equipo ───


async def buscar_equipo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    registrar_accion(query.from_user.id, "buscar")

    botones = []
    for nombre, key in CONTINENTES.items():
        botones.append(
            [InlineKeyboardButton(nombre, callback_data=f"cont_{key}")]
        )
    botones.append([InlineKeyboardButton("🔙 Volver", callback_data="menu_principal")])

    reply_markup = InlineKeyboardMarkup(botones)
    await query.edit_message_text(
        "🌍 *Elegí el continente:*", reply_markup=reply_markup, parse_mode="Markdown"
    )


async def seleccionar_continente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    continente_key = query.data.replace("cont_", "")
    paises = PAISES_POR_CONTINENTE.get(continente_key, {})

    if not paises:
        await query.edit_message_text("No hay países disponibles para este continente.")
        return

    botones = []
    for nombre, data in paises.items():
        botones.append(
            [
                InlineKeyboardButton(
                    nombre, callback_data=f"pais_{continente_key}_{data['code']}"
                )
            ]
        )
    botones.append(
        [InlineKeyboardButton("🔙 Volver a continentes", callback_data="buscar_equipo")]
    )

    reply_markup = InlineKeyboardMarkup(botones)
    await query.edit_message_text(
        f"📍 *Elegí el país:*",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def seleccionar_pais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.replace("pais_", "").split("_", 1)
    continente_key = parts[0]
    pais_code = parts[1]

    paises = PAISES_POR_CONTINENTE.get(continente_key, {})
    pais_data = None
    for nombre, data in paises.items():
        if data["code"] == pais_code:
            pais_data = data
            break

    if not pais_data:
        await query.edit_message_text("País no encontrado.")
        return

    ligas = pais_data.get("ligas", [])
    if not ligas:
        await query.edit_message_text("No hay ligas disponibles para este país.")
        return

    botones = []
    for liga in ligas:
        botones.append(
            [
                InlineKeyboardButton(
                    liga["nombre"],
                    callback_data=f"liga_{continente_key}_{pais_code}_{liga['id']}",
                )
            ]
        )
    botones.append(
        [
            InlineKeyboardButton(
                "🔙 Volver a países", callback_data=f"cont_{continente_key}"
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(botones)
    await query.edit_message_text(
        f"🏆 *Elegí la liga:*",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def seleccionar_liga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.replace("liga_", "").split("_", 2)
    continente_key = parts[0]
    pais_code = parts[1]
    liga_id = int(parts[2])

    paises = PAISES_POR_CONTINENTE.get(continente_key, {})
    pais_nombre = ""
    liga_nombre = ""
    for nombre, data in paises.items():
        if data["code"] == pais_code:
            pais_nombre = nombre
            for liga in data["ligas"]:
                if liga["id"] == liga_id:
                    liga_nombre = liga["nombre"]
                    break
            break

    equipos = EQUIPOS_POR_LIGA.get((liga_id, 2024), [])

    if not equipos:
        await query.edit_message_text(
            f"No hay equipos cargados para {liga_nombre}.\n"
            "Podés usar /buscar nombre_equipo para buscar uno específico."
        )
        return

    botones = []
    for equipo in equipos:
        botones.append(
            [
                InlineKeyboardButton(
                    equipo["nombre"],
                    callback_data=f"agregar_{equipo['id']}_{equipo['nombre']}",
                )
            ]
        )
    botones.append(
        [
            InlineKeyboardButton(
                "🔙 Volver a ligas", callback_data=f"pais_{continente_key}_{pais_code}"
            )
        ]
    )

    reply_markup = InlineKeyboardMarkup(botones)
    await query.edit_message_text(
        f"⚽ *{liga_nombre}* - *{pais_nombre}*\n\nElegí tu equipo:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


# ─── AGREGAR / ELIMINAR EQUIPOS ───


async def agregar_equipo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_", 2)
    equipo_id = int(parts[1])
    equipo_nombre = parts[2] if len(parts) > 2 else "Equipo"

    agregar_equipo(query.from_user.id, equipo_id, equipo_nombre)

    keyboard = [
        [InlineKeyboardButton("🔍 Buscar más", callback_data="buscar_equipo")],
        [InlineKeyboardButton("📰 Ver Noticias", callback_data="noticias")],
        [InlineKeyboardButton("🔙 Menú", callback_data="menu_principal")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"✅ ¡*{equipo_nombre}* agregado a tu lista!\n\n"
        "Te enviaré noticias y actualizaciones de este equipo.",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def mis_equipos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    registrar_accion(query.from_user.id, "equipos")

    usuario = obtener_usuario(query.from_user.id)
    if not usuario or not usuario.equipos:
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="menu_principal")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Aún no seguís ningún equipo. 🔍\n"
            "Usá el botón 'Buscar Equipo' para agregar uno.",
            reply_markup=reply_markup,
        )
        return

    botones = []
    for equipo in usuario.equipos:
        botones.append(
            [
                InlineKeyboardButton(
                    f"❌ {equipo['nombre']}",
                    callback_data=f"eliminar_{equipo['id']}",
                )
            ]
        )
    botones.append([InlineKeyboardButton("🔙 Volver", callback_data="menu_principal")])

    reply_markup = InlineKeyboardMarkup(botones)
    equipos_text = "\n".join([f"• {e['nombre']}" for e in usuario.equipos])
    await query.edit_message_text(
        f"*Tus equipos:*\n\n{equipos_text}\n\n"
        "Tocá ❌ para dejar de seguir un equipo.",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def eliminar_equipo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    equipo_id = int(query.data.replace("eliminar_", ""))
    eliminar_equipo(query.from_user.id, equipo_id)

    await query.edit_message_text("✅ Equipo eliminado de tu lista.")
    await mis_equipos(update, context)


# ─── NOTICIAS ───


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    registrar_accion(query.from_user.id, "noticias")

    usuario = obtener_usuario(query.from_user.id)
    if not usuario or not usuario.equipos:
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="menu_principal")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Seguí un equipo primero para ver sus noticias. 📰",
            reply_markup=reply_markup,
        )
        return

    await query.edit_message_text("🔄 Buscando las últimas noticias...")

    mensajes = []
    for equipo in usuario.equipos[:3]:
        articulos = news_client.obtener_noticias_equipo(equipo["nombre"], page_size=2)
        if articulos:
            for art in articulos[:1]:
                titulo = art["titulo"][:100]
                url = art["url"]
                fuente = art["fuente"]
                mensajes.append(
                    f"⚽ *{equipo['nombre']}*\n\n📰 {titulo}\n🔗 {url}\n📡 {fuente}\n"
                )

    if not mensajes:
        mensajes.append("No hay noticias recientes para tus equipos. 😕")

    texto = "\n---\n".join(mensajes[:5])
    keyboard = [
        [InlineKeyboardButton("🔄 Actualizar", callback_data="noticias")],
        [InlineKeyboardButton("🔙 Menú", callback_data="menu_principal")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        texto, reply_markup=reply_markup, parse_mode="Markdown"
    )


# ─── AYUDA ───


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texto = (
        "ℹ️ *Ayuda - BotifutBot*\n\n"
        "*Comandos disponibles:*\n"
        "/start - Iniciar el bot\n"
        "/equipos - Ver tus equipos\n"
        "/buscar - Buscar un equipo\n"
        "/noticias - Ver noticias\n"
        "/ayuda - Mostrar esta ayuda\n\n"
        "*¿Cómo funciona?*\n"
        "1. Elegí los equipos que querés seguir\n"
        "2. Recibirás noticias y actualizaciones automáticamente\n"
        "3. ¡No tenés que hacer nada más! ⚽\n\n"
        "Desarrollado con ❤️ para fanáticos del fútbol"
    )
    keyboard = [[InlineKeyboardButton("🔙 Menú", callback_data="menu_principal")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(texto, reply_markup=reply_markup, parse_mode="Markdown")


# ─── COMANDOS DIRECTOS ───


async def cmd_equipos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = obtener_usuario(update.effective_user.id)
    if not usuario or not usuario.equipos:
        await update.message.reply_text(
            "Aún no seguís ningún equipo. Usá /buscar para agregar uno."
        )
        return

    equipos_text = "\n".join([f"• {e['nombre']}" for e in usuario.equipos])
    await update.message.reply_text(
        f"*Tus equipos:*\n\n{equipos_text}", parse_mode="Markdown"
    )


async def cmd_buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        nombre = " ".join(context.args)
        await update.message.reply_text(
            f"🔍 Buscando equipos similares a '{nombre}'..."
        )
        resultados = football_client.buscar_equipo(nombre)

        if not resultados:
            await update.message.reply_text("No encontré equipos con ese nombre. 😕")
            return

        botones = []
        for equipo in resultados[:5]:
            team = equipo.get("team", {})
            botones.append(
                [
                    InlineKeyboardButton(
                        f"{team.get('name', '?')} ({team.get('country', {}).get('name', '')})",
                        callback_data=f"agregar_{team['id']}_{team['name']}",
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(botones)
        await update.message.reply_text(
            "🔍 *Resultados:*", reply_markup=reply_markup, parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "Usage: /buscar nombre_del_equipo\nEjemplo: /buscar Barcelona"
        )


async def cmd_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = obtener_usuario(update.effective_user.id)
    if not usuario or not usuario.equipos:
        await update.message.reply_text(
            "Seguí un equipo primero con /buscar para ver noticias."
        )
        return

    await update.message.reply_text("🔄 Buscando noticias...")

    mensajes = []
    for equipo in usuario.equipos[:3]:
        articulos = news_client.obtener_noticias_equipo(equipo["nombre"], page_size=2)
        for art in articulos[:1]:
            titulo = art["titulo"][:100]
            url = art["url"]
            mensajes.append(f"⚽ *{equipo['nombre']}*\n📰 {titulo}\n🔗 {url}\n")

    if not mensajes:
        await update.message.reply_text("No hay noticias recientes. 😕")
        return

    texto = "\n---\n".join(mensajes[:5])
    await update.message.reply_text(texto, parse_mode="Markdown")


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    registrar_accion(user_id, "stats")

    total = obtener_total_usuarios()
    activos_7d = obtener_usuarios_activos(7)
    activos_30d = obtener_usuarios_activos(30)
    clicks = obtener_clicks_links(30)
    conversiones = obtener_conversiones(30)
    top_equipos = obtener_top_equipos(5)

    equipos_text = (
        "\n".join([f"  • {e[0]}: {e[1]} seguidores" for e in top_equipos])
        if top_equipos
        else "  Sin datos aún"
    )

    texto = (
        "📊 *Estadísticas del Bot*\n\n"
        f"*Usuarios totales:* {total}\n"
        f"*Activos (7 días):* {activos_7d}\n"
        f"*Activos (30 días):* {activos_30d}\n\n"
        f"*Clicks en links (30d):* {clicks}\n"
        f"*Conversiones (30d):* {conversiones}\n\n"
        f"*Top equipos:*\n{equipos_text}\n\n"
        f"*Tasa de conversión:* {((conversiones/clicks)*100) if clicks > 0 else 0:.1f}%"
    )
    await update.message.reply_text(texto, parse_mode="Markdown")
