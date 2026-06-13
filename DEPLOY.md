# BotiFutbol - Deploy en Railway

## Requisitos
- Docker
- Cuenta en Railway
- API keys de Telegram, API-Football, NewsAPI

## Variables de entorno en Railway
```
TELEGRAM_TOKEN=
API_FOOTBALL_KEY=
NEWS_API_KEY=
DATABASE_URL=
```

## Deploy

### Opción 1: Railway CLI
```bash
railway login
railway init
railway up
```

### Opción 2: Docker Compose (local)
```bash
docker-compose up -d
```

## Estructura de servicios
1. **bot** - Bot de Telegram
2. **api** - API FastAPI (puerto 8000)
3. **web** - Frontend Next.js (puerto 3000)
4. **postgres** - Base de datos

## URLs
- App: https://botifutbol.railway.app
- API: https://botifutbol-api.railway.app
- Bot: https://t.me/BotiFutBot
