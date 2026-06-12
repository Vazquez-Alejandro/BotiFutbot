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
    "🌎 Americas": "americas",
    "🌍 Europa": "europa",
    "🌍 Asia": "asia",
    "🌍 Africa": "africa",
    "🌍 Oceanía": "oceania",
}

PAISES_POR_CONTINENTE = {
    "americas": {
        "🇦🇷 Argentina": {"code": "AR", "ligas": [
            {"id": 1, "nombre": "Liga Profesional"},
            {"id": 2, "nombre": "Primera Nacional"},
        ]},
        "🇧🇷 Brasil": {"code": "BR", "ligas": [
            {"id": 3, "nombre": "Serie A"},
            {"id": 4, "nombre": "Serie B"},
            {"id": 5, "nombre": "Copa do Brasil"},
        ]},
        "🇲🇽 México": {"code": "MX", "ligas": [
            {"id": 262, "nombre": "Liga MX"},
            {"id": 263, "nombre": "Liga de Expansión MX"},
        ]},
        "🇨🇴 Colombia": {"code": "CO", "ligas": [
            {"id": 239, "nombre": "Liga BetPlay"},
        ]},
        "🇨🇱 Chile": {"code": "CL", "ligas": [
            {"id": 266, "nombre": "Primera División"},
        ]},
        "🇺🇾 Uruguay": {"code": "UY", "ligas": [
            {"id": 268, "nombre": "Primera División"},
        ]},
        "🇺🇸 USA": {"code": "US", "ligas": [
            {"id": 253, "nombre": "MLS"},
        ]},
    },
    "europa": {
        "🇪🇸 España": {"code": "ES", "ligas": [
            {"id": 140, "nombre": "La Liga"},
            {"id": 141, "nombre": "Segunda División"},
            {"id": 143, "nombre": "Copa del Rey"},
        ]},
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra": {"code": "GB", "ligas": [
            {"id": 39, "nombre": "Premier League"},
            {"id": 40, "nombre": "Championship"},
            {"id": 41, "nombre": "League One"},
            {"id": 42, "nombre": "League Two"},
            {"id": 45, "nombre": "FA Cup"},
            {"id": 48, "nombre": "League Cup"},
        ]},
        "🇮🇹 Italia": {"code": "IT", "ligas": [
            {"id": 135, "nombre": "Serie A"},
            {"id": 136, "nombre": "Serie B"},
            {"id": 137, "nombre": "Coppa Italia"},
        ]},
        "🇩🇪 Alemania": {"code": "DE", "ligas": [
            {"id": 78, "nombre": "Bundesliga"},
            {"id": 79, "nombre": "2. Bundesliga"},
            {"id": 80, "nombre": "3. Liga"},
        ]},
        "🇫🇷 Francia": {"code": "FR", "ligas": [
            {"id": 61, "nombre": "Ligue 1"},
            {"id": 62, "nombre": "Ligue 2"},
            {"id": 66, "nombre": "Copa de Francia"},
        ]},
        "🇵🇹 Portugal": {"code": "PT", "ligas": [
            {"id": 94, "nombre": "Primeira Liga"},
            {"id": 95, "nombre": "Liga Portugal 2"},
        ]},
        "🇳🇱 Holanda": {"code": "NL", "ligas": [
            {"id": 88, "nombre": "Eredivisie"},
        ]},
        "🇧🇪 Bélgica": {"code": "BE", "ligas": [
            {"id": 144, "nombre": "Jupiler Pro League"},
        ]},
        "🇹🇷 Turquía": {"code": "TR", "ligas": [
            {"id": 203, "nombre": "Süper Lig"},
        ]},
        "🇷🇺 Rusia": {"code": "RU", "ligas": [
            {"id": 179, "nombre": "Premier League"},
        ]},
        "🇬🇷 Grecia": {"code": "GR", "ligas": [
            {"id": 195, "nombre": "Super League"},
        ]},
    },
    "asia": {
        "🇸🇦 Arabia Saudita": {"code": "SA", "ligas": [
            {"id": 307, "nombre": "Saudi Pro League"},
        ]},
        "🇯🇵 Japón": {"code": "JP", "ligas": [
            {"id": 98, "nombre": "J1 League"},
            {"id": 99, "nombre": "J2 League"},
        ]},
        "🇨🇳 China": {"code": "CN", "ligas": [
            {"id": 169, "nombre": "Chinese Super League"},
        ]},
        "🇰🇷 Corea del Sur": {"code": "KR", "ligas": [
            {"id": 292, "nombre": "K League 1"},
        ]},
        "🇮🇳 India": {"code": "IN", "ligas": [
            {"id": 323, "nombre": "ISL"},
        ]},
    },
    "africa": {
        "🇪🇬 Egipto": {"code": "EG", "ligas": [
            {"id": 200, "nombre": "Premier League"},
        ]},
        "🇲🇦 Marruecos": {"code": "MA", "ligas": [
            {"id": 266, "nombre": "Botola Pro"},
        ]},
        "🇳🇬 Nigeria": {"code": "NG", "ligas": [
            {"id": 202, "nombre": "NPFL"},
        ]},
        "🇿🇦 Sudáfrica": {"code": "ZA", "ligas": [
            {"id": 293, "nombre": "PSL"},
        ]},
    },
    "oceania": {
        "🇦🇺 Australia": {"code": "AU", "ligas": [
            {"id": 188, "nombre": "A-League"},
        ]},
        "🇳🇿 Nueva Zelanda": {"code": "NZ", "ligas": [
            {"id": 190, "nombre": "ISPS Handa Premiership"},
        ]},
    },
}

EQUIPOS_POR_LIGA = {
    # Argentina - Liga Profesional (league_id: 1, season: 2024)
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
        {"id": 54, "nombre": "Unión"},
        {"id": 55, "nombre": "Belgrano"},
        {"id": 56, "nombre": "Argentinos Juniors"},
        {"id": 57, "nombre": "Banfield"},
        {"id": 58, "nombre": "Godoy Cruz"},
        {"id": 59, "nombre": "Platense"},
        {"id": 60, "nombre": "Sarmiento"},
        {"id": 61, "nombre": "Barracas Central"},
        {"id": 62, "nombre": "Independiente Rivadavia"},
        {"id": 63, "nombre": "Unión Santa Fe"},
    ],
    # España - La Liga (league_id: 140, season: 2024)
    (140, 2024): [
        {"id": 529, "nombre": "Barcelona"},
        {"id": 541, "nombre": "Real Madrid"},
        {"id": 530, "nombre": "Atlético Madrid"},
        {"id": 536, "nombre": "Sevilla"},
        {"id": 548, "nombre": "Real Sociedad"},
        {"id": 532, "nombre": "Valencia"},
        {"id": 533, "nombre": "Villarreal"},
        {"id": 534, "nombre": "Athletic Bilbao"},
        {"id": 535, "nombre": "Celta Vigo"},
        {"id": 537, "nombre": "Betis"},
        {"id": 538, "nombre": "Espanyol"},
        {"id": 539, "nombre": "Getafe"},
        {"id": 540, "nombre": "Mallorca"},
        {"id": 542, "nombre": "Rayo Vallecano"},
        {"id": 543, "nombre": "Osasuna"},
        {"id": 544, "nombre": "Girona"},
        {"id": 545, "nombre": "Las Palmas"},
        {"id": 546, "nombre": "Alavés"},
        {"id": 547, "nombre": "Cádiz"},
        {"id": 549, "nombre": "Granada"},
    ],
    # Inglaterra - Premier League (league_id: 39, season: 2024)
    (39, 2024): [
        {"id": 33, "nombre": "Manchester United"},
        {"id": 40, "nombre": "Liverpool"},
        {"id": 50, "nombre": "Manchester City"},
        {"id": 47, "nombre": "Tottenham"},
        {"id": 42, "nombre": "Arsenal"},
        {"id": 49, "nombre": "Chelsea"},
        {"id": 48, "nombre": "West Ham"},
        {"id": 46, "nombre": "Leicester"},
        {"id": 44, "nombre": "Leeds"},
        {"id": 41, "nombre": "Brighton"},
        {"id": 66, "nombre": "Aston Villa"},
        {"id": 63, "nombre": "Newcastle"},
        {"id": 39, "nombre": "Wolverhampton"},
        {"id": 38, "nombre": "Watford"},
        {"id": 37, "nombre": "Norwich"},
        {"id": 36, "nombre": "Brentford"},
        {"id": 35, "nombre": "Crystal Palace"},
        {"id": 34, "nombre": "Everton"},
        {"id": 32, "nombre": "Southampton"},
        {"id": 45, "nombre": "Fulham"},
    ],
    # Italia - Serie A (league_id: 135, season: 2024)
    (135, 2024): [
        {"id": 489, "nombre": "Juventus"},
        {"id": 505, "nombre": "Inter Milan"},
        {"id": 497, "nombre": "AC Milan"},
        {"id": 496, "nombre": "AS Roma"},
        {"id": 487, "nombre": "SS Lazio"},
        {"id": 492, "nombre": "Napoli"},
        {"id": 490, "nombre": "Fiorentina"},
        {"id": 498, "nombre": "Atalanta"},
        {"id": 499, "nombre": "Bologna"},
        {"id": 500, "nombre": "Torino"},
        {"id": 501, "nombre": "Sampdoria"},
        {"id": 502, "nombre": "Genoa"},
        {"id": 503, "nombre": "Cagliari"},
        {"id": 504, "nombre": "Udinese"},
        {"id": 506, "nombre": "Sassuolo"},
        {"id": 507, "nombre": "Verona"},
        {"id": 508, "nombre": "Lecce"},
        {"id": 509, "nombre": "Empoli"},
        {"id": 510, "nombre": "Frosinone"},
        {"id": 511, "nombre": "Salernitana"},
    ],
    # Alemania - Bundesliga (league_id: 78, season: 2024)
    (78, 2024): [
        {"id": 157, "nombre": "Bayern Munich"},
        {"id": 165, "nombre": "Borussia Dortmund"},
        {"id": 168, "nombre": "Bayer Leverkusen"},
        {"id": 169, "nombre": "RB Leipzig"},
        {"id": 162, "nombre": "Eintracht Frankfurt"},
        {"id": 163, "nombre": "Borussia Mönchengladbach"},
        {"id": 164, "nombre": "Schalke 04"},
        {"id": 166, "nombre": "VfB Stuttgart"},
        {"id": 167, "nombre": "Wolfsburg"},
        {"id": 170, "nombre": "Werder Bremen"},
        {"id": 171, "nombre": "Hertha Berlin"},
        {"id": 172, "nombre": "FC Augsburg"},
        {"id": 173, "nombre": "Hoffenheim"},
        {"id": 174, "nombre": "Mainz 05"},
        {"id": 175, "nombre": "Freiburg"},
        {"id": 176, "nombre": "Hamburger SV"},
        {"id": 177, "nombre": "Hannover 96"},
        {"id": 178, "nombre": "1. FC Nürnberg"},
    ],
    # Francia - Ligue 1 (league_id: 61, season: 2024)
    (61, 2024): [
        {"id": 85, "nombre": "Paris Saint-Germain"},
        {"id": 80, "nombre": "Lyon"},
        {"id": 81, "nombre": "Marseille"},
        {"id": 82, "nombre": "Monaco"},
        {"id": 83, "nombre": "Lille"},
        {"id": 84, "nombre": "Nice"},
        {"id": 86, "nombre": "Rennes"},
        {"id": 87, "nombre": "Strasbourg"},
        {"id": 88, "nombre": "Lens"},
        {"id": 89, "nombre": "Montpellier"},
        {"id": 90, "nombre": "Nantes"},
        {"id": 91, "nombre": "Bordeaux"},
        {"id": 92, "nombre": "Saint-Étienne"},
        {"id": 93, "nombre": "Toulouse"},
        {"id": 147, "nombre": "Brest"},
        {"id": 148, "nombre": "Reims"},
        {"id": 149, "nombre": "Metz"},
        {"id": 150, "nombre": "Lorient"},
        {"id": 151, "nombre": "Le Havre"},
    ],
    # Brasil - Serie A (league_id: 3, season: 2024)
    (3, 2024): [
        {"id": 119, "nombre": "Flamengo"},
        {"id": 120, "nombre": "Corinthians"},
        {"id": 121, "nombre": "São Paulo"},
        {"id": 122, "nombre": "Palmeiras"},
        {"id": 126, "nombre": "Grêmio"},
        {"id": 123, "nombre": "Santos"},
        {"id": 124, "nombre": "Cruzeiro"},
        {"id": 125, "nombre": "Atlético Mineiro"},
        {"id": 127, "nombre": "Internacional"},
        {"id": 128, "nombre": "Fluminense"},
        {"id": 129, "nombre": "Vasco da Gama"},
        {"id": 130, "nombre": "Botafogo"},
        {"id": 131, "nombre": "Bahia"},
        {"id": 132, "nombre": "Sport Recife"},
        {"id": 133, "nombre": "Vitória"},
        {"id": 134, "nombre": "Goiás"},
        {"id": 135, "nombre": "Athletico Paranaense"},
        {"id": 136, "nombre": "Coritiba"},
        {"id": 137, "nombre": "Fortaleza"},
        {"id": 138, "nombre": "Ceará"},
    ],
}
