from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from shared.database import get_db
from shared.api_client import football_client

router = APIRouter(prefix="/api/leagues", tags=["leagues"])


@router.get("/standings")
def get_standings(league_id: int, season: int = 2024):
    result = football_client.obtener_clasificacion(league_id, season)
    if not result:
        return {"standings": []}

    standings_data = result[0].get("league", {}).get("standings", [[]])[0]
    table = []
    for team in standings_data:
        table.append({
            "position": team.get("rank"),
            "team_id": team.get("team", {}).get("id"),
            "team_name": team.get("team", {}).get("name"),
            "team_logo": team.get("team", {}).get("logo"),
            "points": team.get("points"),
            "played": team.get("all", {}).get("played"),
            "win": team.get("all", {}).get("win"),
            "draw": team.get("all", {}).get("draw"),
            "lose": team.get("all", {}).get("lose"),
            "goals_for": team.get("all", {}).get("goals", {}).get("for"),
            "goals_against": team.get("all", {}).get("goals", {}).get("against"),
            "goal_difference": team.get("goalsDiff"),
            "form": team.get("form"),
        })

    return {"standings": table}


@router.get("/fixtures")
def get_fixtures(league_id: int, season: int = 2024, round: Optional[str] = None):
    result = football_client.obtener_fixtures_por_liga(league_id, season, round)
    fixtures = []
    for f in result:
        fixture = f.get("fixture", {})
        teams = f.get("teams", {})
        goals = f.get("goals", {})
        fixtures.append({
            "id": fixture.get("id"),
            "date": fixture.get("date"),
            "timestamp": fixture.get("timestamp"),
            "status": fixture.get("status", {}).get("short"),
            "status_long": fixture.get("status", {}).get("long"),
            "elapsed": fixture.get("status", {}).get("elapsed"),
            "round": fixture.get("round"),
            "home": {
                "id": teams.get("home", {}).get("id"),
                "name": teams.get("home", {}).get("name"),
                "logo": teams.get("home", {}).get("logo"),
                "winner": teams.get("home", {}).get("winner"),
            },
            "away": {
                "id": teams.get("away", {}).get("id"),
                "name": teams.get("away", {}).get("name"),
                "logo": teams.get("away", {}).get("logo"),
                "winner": teams.get("away", {}).get("winner"),
            },
            "goals": {
                "home": goals.get("home"),
                "away": goals.get("away"),
            },
        })
    return {"fixtures": fixtures}


@router.get("/live")
def get_live_matches(league_id: Optional[int] = None):
    result = football_client.obtener_partidos_en_vivo(league_id)
    matches = []
    for f in result:
        fixture = f.get("fixture", {})
        teams = f.get("teams", {})
        goals = f.get("goals", {})
        matches.append({
            "id": fixture.get("id"),
            "date": fixture.get("date"),
            "status": fixture.get("status", {}).get("short"),
            "elapsed": fixture.get("status", {}).get("elapsed"),
            "home": {
                "id": teams.get("home", {}).get("id"),
                "name": teams.get("home", {}).get("name"),
                "logo": teams.get("home", {}).get("logo"),
            },
            "away": {
                "id": teams.get("away", {}).get("id"),
                "name": teams.get("away", {}).get("name"),
                "logo": teams.get("away", {}).get("logo"),
            },
            "goals": {
                "home": goals.get("home"),
                "away": goals.get("away"),
            },
        })
    return {"matches": matches}


@router.get("/topscorers")
def get_topscorers(league_id: int, season: int = 2024):
    result = football_client.obtener_goleadores(league_id, season)
    scorers = []
    for p in result[:20]:
        player = p.get("player", {})
        statistics = p.get("statistics", [{}])[0] if p.get("statistics") else {}
        scorers.append({
            "player_id": player.get("id"),
            "name": player.get("name"),
            "photo": player.get("photo"),
            "team": statistics.get("team", {}).get("name"),
            "team_logo": statistics.get("team", {}).get("logo"),
            "goals": statistics.get("goals", {}).get("total"),
            "assists": statistics.get("goals", {}).get("assists"),
            "appearances": statistics.get("games", {}).get("appearences"),
            "rating": statistics.get("games", {}).get("rating"),
        })
    return {"scorers": scorers}


@router.get("/match/{fixture_id}")
def get_match_detail(fixture_id: int):
    fixture = football_client.obtener_fixture_por_id(fixture_id)
    if not fixture:
        return {"match": None}

    events = football_client.obtener_eventos_partido(fixture_id)
    stats = football_client.obtener_estadisticas_partido(fixture_id)

    f = fixture.get("fixture", {})
    teams = fixture.get("teams", {})
    goals = fixture.get("goals", {})

    return {
        "match": {
            "id": f.get("id"),
            "date": f.get("date"),
            "status": f.get("status", {}).get("short"),
            "status_long": f.get("status", {}).get("long"),
            "elapsed": f.get("status", {}).get("elapsed"),
            "venue": f.get("venue", {}).get("name"),
            "referee": f.get("referee"),
            "home": {
                "id": teams.get("home", {}).get("id"),
                "name": teams.get("home", {}).get("name"),
                "logo": teams.get("home", {}).get("logo"),
                "winner": teams.get("home", {}).get("winner"),
            },
            "away": {
                "id": teams.get("away", {}).get("id"),
                "name": teams.get("away", {}).get("name"),
                "logo": teams.get("away", {}).get("logo"),
                "winner": teams.get("away", {}).get("winner"),
            },
            "goals": {
                "home": goals.get("home"),
                "away": goals.get("away"),
            },
            "events": [
                {
                    "time": e.get("time", {}).get("elapsed"),
                    "team": e.get("team", {}).get("name"),
                    "player": e.get("player", {}).get("name"),
                    "assist": e.get("assist", {}).get("name"),
                    "type": e.get("type"),
                    "detail": e.get("detail"),
                }
                for e in events
            ],
            "statistics": stats,
        }
    }
