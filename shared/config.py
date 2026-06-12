import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/botifutbol.db")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", 5))

API_FOOTBALL_BASE_URL = "https://v3.football.api-sports.io"
NEWS_API_BASE_URL = "https://newsapi.org/v2"

CONTINENTES = {
    "Americas": "americas",
    "Europa": "europa",
    "Asia": "asia",
    "Africa": "africa",
    "Oceania": "oceania",
}

PAISES_POR_CONTINENTE = {
    "americas": {
        "Argentina": {"code": "AR", "flag": "🇦🇷", "ligas": [
            {"id": 1, "nombre": "Liga Profesional"},
            {"id": 2, "nombre": "Primera Nacional"},
        ]},
        "Brasil": {"code": "BR", "flag": "🇧🇷", "ligas": [
            {"id": 3, "nombre": "Serie A"},
            {"id": 4, "nombre": "Serie B"},
            {"id": 5, "nombre": "Copa do Brasil"},
        ]},
        "México": {"code": "MX", "flag": "🇲🇽", "ligas": [
            {"id": 262, "nombre": "Liga MX"},
            {"id": 263, "nombre": "Liga de Expansión MX"},
        ]},
        "Colombia": {"code": "CO", "flag": "🇨🇴", "ligas": [
            {"id": 239, "nombre": "Liga BetPlay"},
        ]},
        "Chile": {"code": "CL", "flag": "🇨🇱", "ligas": [
            {"id": 266, "nombre": "Primera División"},
        ]},
        "Uruguay": {"code": "UY", "flag": "🇺🇾", "ligas": [
            {"id": 268, "nombre": "Primera División"},
        ]},
        "USA": {"code": "US", "flag": "🇺🇸", "ligas": [
            {"id": 253, "nombre": "MLS"},
        ]},
    },
    "europa": {
        "España": {"code": "ES", "flag": "🇪🇸", "ligas": [
            {"id": 140, "nombre": "La Liga"},
            {"id": 141, "nombre": "Segunda División"},
        ]},
        "Inglaterra": {"code": "GB", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "ligas": [
            {"id": 39, "nombre": "Premier League"},
            {"id": 40, "nombre": "Championship"},
            {"id": 45, "nombre": "FA Cup"},
        ]},
        "Italia": {"code": "IT", "flag": "🇮🇹", "ligas": [
            {"id": 135, "nombre": "Serie A"},
            {"id": 136, "nombre": "Serie B"},
        ]},
        "Alemania": {"code": "DE", "flag": "🇩🇪", "ligas": [
            {"id": 78, "nombre": "Bundesliga"},
            {"id": 79, "nombre": "2. Bundesliga"},
        ]},
        "Francia": {"code": "FR", "flag": "🇫🇷", "ligas": [
            {"id": 61, "nombre": "Ligue 1"},
            {"id": 62, "nombre": "Ligue 2"},
        ]},
        "Portugal": {"code": "PT", "flag": "🇵🇹", "ligas": [
            {"id": 94, "nombre": "Primeira Liga"},
        ]},
        "Holanda": {"code": "NL", "flag": "🇳🇱", "ligas": [
            {"id": 88, "nombre": "Eredivisie"},
        ]},
        "Turquía": {"code": "TR", "flag": "🇹🇷", "ligas": [
            {"id": 203, "nombre": "Süper Lig"},
        ]},
    },
    "asia": {
        "Arabia Saudita": {"code": "SA", "flag": "🇸🇦", "ligas": [
            {"id": 307, "nombre": "Saudi Pro League"},
        ]},
        "Japón": {"code": "JP", "flag": "🇯🇵", "ligas": [
            {"id": 98, "nombre": "J1 League"},
        ]},
        "Corea del Sur": {"code": "KR", "flag": "🇰🇷", "ligas": [
            {"id": 292, "nombre": "K League 1"},
        ]},
    },
    "africa": {
        "Egipto": {"code": "EG", "flag": "🇪🇬", "ligas": [
            {"id": 200, "nombre": "Premier League"},
        ]},
        "Marruecos": {"code": "MA", "flag": "🇲🇦", "ligas": [
            {"id": 266, "nombre": "Botola Pro"},
        ]},
        "Sudáfrica": {"code": "ZA", "flag": "🇿🇦", "ligas": [
            {"id": 293, "nombre": "PSL"},
        ]},
    },
    "oceania": {
        "Australia": {"code": "AU", "flag": "🇦🇺", "ligas": [
            {"id": 188, "nombre": "A-League"},
        ]},
    },
}

EQUIPOS_POR_LIGA = {
    (1, 2024): [
        {"id": 19, "nombre": "River Plate"},
        {"id": 12, "nombre": "Boca Juniors"},
        {"id": 46, "nombre": "Racing Club"},
        {"id": 53, "nombre": "San Lorenzo"},
        {"id": 44, "nombre": "Vélez Sarsfield"},
        {"id": 45, "nombre": "Estudiantes"},
        {"id": 47, "nombre": "Gimnasia y Esgrima"},
        {"id": 48, "nombre": "Newell's Old Boys"},
        {"id": 49, "nombre": "Rosario Central"},
        {"id": 50, "nombre": "Talleres"},
        {"id": 51, "nombre": "Defensa y Justicia"},
        {"id": 52, "nombre": "Lanús"},
    ],
    (3, 2024): [
        {"id": 119, "nombre": "Flamengo"},
        {"id": 120, "nombre": "Corinthians"},
        {"id": 121, "nombre": "São Paulo"},
        {"id": 122, "nombre": "Palmeiras"},
        {"id": 126, "nombre": "Grêmio"},
        {"id": 127, "nombre": "Internacional"},
    ],
    (140, 2024): [
        {"id": 529, "nombre": "Barcelona"},
        {"id": 541, "nombre": "Real Madrid"},
        {"id": 530, "nombre": "Atlético Madrid"},
        {"id": 536, "nombre": "Sevilla"},
        {"id": 548, "nombre": "Real Sociedad"},
        {"id": 532, "nombre": "Valencia"},
    ],
    (39, 2024): [
        {"id": 33, "nombre": "Manchester United"},
        {"id": 40, "nombre": "Liverpool"},
        {"id": 50, "nombre": "Manchester City"},
        {"id": 47, "nombre": "Tottenham"},
        {"id": 42, "nombre": "Arsenal"},
        {"id": 49, "nombre": "Chelsea"},
    ],
    (135, 2024): [
        {"id": 489, "nombre": "Juventus"},
        {"id": 505, "nombre": "Inter Milan"},
        {"id": 497, "nombre": "AC Milan"},
        {"id": 496, "nombre": "AS Roma"},
        {"id": 492, "nombre": "Napoli"},
    ],
    (78, 2024): [
        {"id": 157, "nombre": "Bayern Munich"},
        {"id": 165, "nombre": "Borussia Dortmund"},
        {"id": 168, "nombre": "Bayer Leverkusen"},
        {"id": 169, "nombre": "RB Leipzig"},
    ],
    (61, 2024): [
        {"id": 85, "nombre": "Paris Saint-Germain"},
        {"id": 80, "nombre": "Lyon"},
        {"id": 81, "nombre": "Marseille"},
        {"id": 82, "nombre": "Monaco"},
    ],
}
