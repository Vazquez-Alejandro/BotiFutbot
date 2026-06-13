from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/mundial", tags=["mundial"])

LEAGUE_ID = 1
SEASON = 2026


@router.get("/standings")
def get_mundial_standings():
    from shared.api_client import football_client
    result = football_client.obtener_clasificacion(LEAGUE_ID, SEASON)
    if not result:
        return {"groups": []}

    raw_groups = result[0].get("league", {}).get("standings", [])
    groups = []
    for group_idx, group_data in enumerate(raw_groups):
        group_name = f"Grupo {chr(65 + group_idx)}"
        teams = []
        for team in group_data:
            teams.append({
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
            })
        groups.append({"name": group_name, "teams": teams})

    return {"groups": groups}


@router.get("/fixtures")
def get_mundial_fixtures(round: Optional[str] = None):
    from shared.api_client import football_client
    result = football_client.obtener_fixtures_por_liga(LEAGUE_ID, SEASON, round)
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


@router.get("/topscorers")
def get_mundial_topscorers():
    from shared.api_client import football_client
    result = football_client.obtener_goleadores(LEAGUE_ID, SEASON)
    scorers = []
    for p in (result or [])[:20]:
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
        })
    return {"scorers": scorers}
