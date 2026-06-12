import requests
from typing import Optional
from src.config import API_FOOTBALL_KEY, API_FOOTBALL_BASE_URL


class FootballAPIClient:
    def __init__(self):
        self.headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": API_FOOTBALL_KEY,
        }
        self.base_url = API_FOOTBALL_BASE_URL

    def _request(self, endpoint: str, params: Optional[dict] = None) -> Optional[dict]:
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params or {},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("errors"):
                print(f"API Error: {data['errors']}")
                return None
            return data.get("response", [])
        except requests.RequestException as e:
            print(f"Error en la petición: {e}")
            return None

    def obtener_partidos_por_equipo(self, equipo_id: int, temporadas: int = 2024) -> list:
        params = {"team": equipo_id, "season": temporadas, "last": 5}
        return self._request("fixtures", params) or []

    def obtener_partidos_en_vivo(self, liga_id: Optional[int] = None) -> list:
        params = {}
        if liga_id:
            params["league"] = liga_id
        return self._request("fixtures", {"live": "all", **params}) or []

    def obtener_goles_recientes(self, equipo_id: int, temporadas: int = 2024) -> list:
        partidos = self.obtener_partidos_por_equipo(equipo_id, temporadas)
        goles = []
        for partido in partidos:
            fixture = partido.get("fixture", {})
            goles_equipo = []
            for evento in partido.get("goals", []):
                if evento.get("team", {}).get("id") == equipo_id:
                    goles_equipo.append(
                        {
                            "minuto": evento.get("time", {}).get("elapsed", 0),
                            "jugador": evento.get("player", {}).get("name", "Desconocido"),
                            "equipo": evento.get("team", {}).get("name", ""),
                        }
                    )
            if goles_equipo:
                goles.append(
                    {
                        "partido_id": fixture.get("id"),
                        "fecha": fixture.get("date"),
                        "local": partido.get("teams", {})
                        .get("home", {})
                        .get("name", ""),
                        "visitante": partido.get("teams", {})
                        .get("away", {})
                        .get("name", ""),
                        "goles": goles_equipo,
                    }
                )
        return goles

    def obtener_estadisticas_partido(self, fixture_id: int) -> Optional[dict]:
        result = self._request("fixtures/statistics", {"fixture": fixture_id})
        if result and len(result) > 0:
            return result[0]
        return None

    def buscar_equipo(self, nombre: str) -> list:
        params = {"search": nombre}
        result = self._request("teams", params)
        return result or []

    def obtener_ligas_disponibles(self, pais: Optional[str] = None) -> list:
        params = {}
        if pais:
            params["country"] = pais
        return self._request("leagues", params) or []

    def obtener_proximos_partidos(self, equipo_id: int, temporadas: int = 2024) -> list:
        from datetime import datetime, timedelta
        hoy = datetime.utcnow().strftime("%Y-%m-%d")
        futuro = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
        params = {"team": equipo_id, "season": temporadas, "from": hoy, "to": futuro}
        return self._request("fixtures", params) or []

    def obtener_partidos_en_vivo_por_equipo(self, equipo_id: int) -> list:
        params = {"team": equipo_id, "live": "all"}
        return self._request("fixtures", params) or []

    def obtener_eventos_partido(self, fixture_id: int) -> list:
        return self._request("fixtures/events", {"fixture": fixture_id}) or []


football_client = FootballAPIClient()
