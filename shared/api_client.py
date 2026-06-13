import requests
from typing import Optional
from shared.config import API_FOOTBALL_KEY, API_FOOTBALL_BASE_URL


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

    def obtener_clasificacion(self, league_id: int, season: int = 2024) -> list:
        return self._request("standings", {"league": league_id, "season": season}) or []

    def obtener_fixtures_por_liga(self, league_id: int, season: int = 2024, round_num: Optional[str] = None) -> list:
        params = {"league": league_id, "season": season}
        if round_num:
            params["round"] = round_num
        return self._request("fixtures", params) or []

    def obtener_fixture_por_id(self, fixture_id: int) -> Optional[dict]:
        result = self._request("fixtures", {"id": fixture_id})
        if result and len(result) > 0:
            return result[0]
        return None

    def obtener_eventos_partido(self, fixture_id: int) -> list:
        return self._request("fixtures/events", {"fixture": fixture_id}) or []

    def obtener_estadisticas_partido(self, fixture_id: int) -> Optional[dict]:
        result = self._request("fixtures/statistics", {"fixture": fixture_id})
        if result and len(result) > 0:
            return result[0]
        return None

    def obtener_partidos_en_vivo(self, league_id: Optional[int] = None) -> list:
        params = {}
        if league_id:
            params["league"] = league_id
        return self._request("fixtures", {"live": "all", **params}) or []

    def buscar_equipo(self, nombre: str) -> list:
        return self._request("teams", {"search": nombre}) or []

    def obtener_proximos_partidos(self, equipo_id: int, temporadas: int = 2024) -> list:
        from datetime import datetime, timedelta
        hoy = datetime.utcnow().strftime("%Y-%m-%d")
        futuro = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
        ids_vistos = set()
        resultados = []
        for season in [temporadas, 2025, 2026, 2022, 2023]:
            params = {"team": equipo_id, "season": season, "from": hoy, "to": futuro}
            data = self._request("fixtures", params) or []
            for item in data:
                fid = item.get("fixture", {}).get("id")
                if fid and fid not in ids_vistos:
                    ids_vistos.add(fid)
                    resultados.append(item)
            if data:
                break
        return resultados

    def obtener_partidos_por_equipo(self, equipo_id: int, temporadas: int = 2024) -> list:
        return self._request("fixtures", {"team": equipo_id, "season": temporadas, "last": 5}) or []

    def obtener_goleadores(self, league_id: int, season: int = 2024) -> list:
        return self._request("players/topscorers", {"league": league_id, "season": season}) or []


football_client = FootballAPIClient()
