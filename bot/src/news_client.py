import requests
from typing import Optional
from src.config import NEWS_API_KEY, NEWS_API_BASE_URL


class NewsAPIClient:
    DOMINIOS_DEPORTIVOS = (
        "marca.com,as.com,ESPN.com,marca.com,goal.com,"
        "sport.es,mundodeportivo.com,football-espana.net,"
        "tycsports.com,olé,conmebol.com,fifa.com,uefa.com,"
        "transfermarkt.com,foxsports.com,espn.com"
    )

    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.base_url = NEWS_API_BASE_URL

    def _request(self, params: dict) -> Optional[dict]:
        try:
            params["apiKey"] = self.api_key
            params["language"] = "es"
            params["sortBy"] = "publishedAt"
            response = requests.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error en News API: {e}")
            return None

    def _es_noticia_deportiva(self, titulo: str, desc: str, url: str, fuente: str) -> bool:
        texto = f"{titulo} {desc}".lower()
        dominio_url = url.lower()

        palabras_no_deportivas = [
            "esposa", "novia", "mujer", "pareja", "boda", "casamiento",
            "novio", "boyfriend", "husband", "influencer", "famosa",
            "look", "vestido", "bikini", "playa", "fiesta", "escándalo",
            "romance", "separación", "divorcio", "engaño", "amante",
            "música", "concierto", "banda", "cantante", "artista",
            "álbum", "canción", "recital", "gira musical",
            "moda", "tendencia", "outfit", "celebridad",
            "cinema", "película", "serie", "actor", "actriz",
            "receta", "cocina", "comida", "restaurante",
            "horóscopo", "astrología", "signo",
        ]
        if any(p in texto for p in palabras_no_deportivas):
            return False

        palabras_futbol = [
            "futbol", "fútbol", "football", "gol", "goles", "partido",
            "liga", "champions", "copa", "mundial", "torneo",
            "transferencia", "fichaje", "entrenador", "dt", "técnico",
            "penal", "tarjeta", "roja", "amarilla", "tiro libre",
            "córner", "fuera de juego", "suplente", "titular",
            "arquero", "portero", "defensor", "mediocampista", "delantero",
            "fixture", "fecha", "jornada", "semifinal", "final",
            "eliminatoria", " clasific", "liga", "serie a", "premier",
            "bundesliga", "ligue 1", "eredivisie",
        ]
        tiene_palabras_futbol = any(p in texto for p in palabras_futbol)
        dominio_es_deportivo = any(d in dominio_url for d in [
            "futbol", "football", "deportes", "sports", "marca", "as.com",
            "espn", "goal.com", "mundodeportivo", "sport.es", "tycsports",
            "olé", "foxsport", "transfermarkt", "conmebol", "fifa", "uefa",
        ])

        return tiene_palabras_futbol or dominio_es_deportivo

    def obtener_noticias_equipo(self, nombre_equipo: str, page_size: int = 5) -> list:
        query = f'"{nombre_equipo}" fútbol'
        result = self._request({
            "q": query,
            "domains": self.DOMINIOS_DEPORTIVOS,
            "pageSize": page_size * 3,
        })
        if not result:
            return []

        articulos = result.get("articles", [])
        filtrados = []
        for a in articulos:
            titulo = a.get("title", "")
            desc = a.get("description", "")
            url = a.get("url", "")
            fuente = a.get("source", {}).get("name", "")
            if titulo and self._es_noticia_deportiva(titulo, desc, url, fuente):
                filtrados.append({
                    "titulo": titulo,
                    "descripcion": desc,
                    "url": url,
                    "imagen": a.get("urlToImage", ""),
                    "fuente": fuente,
                    "fecha": a.get("publishedAt", ""),
                })
            if len(filtrados) >= page_size:
                break
        return filtrados

    def obtener_noticias_liga(self, nombre_liga: str, page_size: int = 5) -> list:
        query = f'"{nombre_liga}" fútbol'
        result = self._request({
            "q": query,
            "domains": self.DOMINIOS_DEPORTIVOS,
            "pageSize": page_size * 3,
        })
        if not result:
            return []

        articulos = result.get("articles", [])
        filtrados = []
        for a in articulos:
            titulo = a.get("title", "")
            desc = a.get("description", "")
            url = a.get("url", "")
            fuente = a.get("source", {}).get("name", "")
            if titulo and self._es_noticia_deportiva(titulo, desc, url, fuente):
                filtrados.append({
                    "titulo": titulo,
                    "descripcion": desc,
                    "url": url,
                    "fuente": fuente,
                })
            if len(filtrados) >= page_size:
                break
        return filtrados


news_client = NewsAPIClient()
