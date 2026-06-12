# BotifutBot - Fútbol en tiempo real

Bot de Telegram + App web para seguir tus equipos de fútbol favoritos.

## Estructura del proyecto

```
botifutbol/
├── bot/                    # Bot de Telegram (Python)
│   ├── bot.py
│   └── src/
├── api/                    # Backend API (FastAPI)
│   ├── main.py
│   ├── config.py
│   └── routes/
├── web/                    # Frontend (Next.js)
│   ├── src/
│   └── public/
├── shared/                 # Código compartido
│   ├── config.py
│   ├── api_client.py
│   ├── database.py
│   └── models.py
├── assets/                 # Logos e imágenes
└── data/                   # Base de datos local (bot)
```

## Stack

- **Bot**: Python + python-telegram-bot
- **API**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Next.js + Tailwind CSS
- **Compartido**: API-Football client, configuración

## Desarrollo

### Bot
```bash
cd bot
source ../venv/bin/activate
python bot.py
```

### API
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd web
npm install
npm run dev
```

## Variables de entorno

Copiar `.env.example` a `.env` y completar:

```
TELEGRAM_TOKEN=tu_token
API_FOOTBALL_KEY=tu_api_key
NEWS_API_KEY=tu_newsapi_key
DATABASE_URL=postgresql://localhost:5432/botifutbol
```

## Features

- ⚽ Seguimiento de múltiples equipos
- 📰 Noticias deportivas filtradas
- 🔔 Notificaciones en tiempo real (goles, tarjetos, lineup)
- 📊 Tabla de posiciones actualizada
- 📅 Fixture completo con jornadas
- 🏆 Goleadores y estadísticas
- 👥 Sistema de amigos y predicciones
- 🎨 UI dark mode con logo WhatsApp + pelota
