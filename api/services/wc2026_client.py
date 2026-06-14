import os
import requests
from typing import Optional
from datetime import datetime

WC2026_API_BASE = "https://api.wc2026api.com"
WHENISKICKOFF_BASE = "https://wheniskickoff.com/data/v1"


def _get_api_key() -> Optional[str]:
    return os.environ.get("WC2026_API_KEY")


def _is_live() -> bool:
    return bool(_get_api_key())


# --- WC2026 API (live) ---


def _fetch_live(path: str) -> Optional[dict]:
    key = _get_api_key()
    if not key:
        return None
    try:
        r = requests.get(
            f"{WC2026_API_BASE}{path}",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"WC2026 live API error: {e}")
        return None


# --- wheniskickoff.com (static fallback) ---


def _fetch_static(endpoint: str) -> Optional[dict]:
    try:
        r = requests.get(f"{WHENISKICKOFF_BASE}/{endpoint}", timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"WC2026 static API error: {e}")
        return None


# --- Standings ---


def _build_standings_live() -> list:
    teams_data = _fetch_live("/teams")
    team_lookup = {t["code"]: t for t in (teams_data.get("data", []) if teams_data else [])}
    data = _fetch_live("/groups")
    groups = data.get("data", []) if data else []
    result = []

    for g in groups:
        label = f"Grupo {g.get('name', '?')}"
        standings = sorted(g.get("standings", []), key=lambda t: t.get("position", 99))
        group_teams = []

        for i, entry in enumerate(standings):
            team_code = entry.get("team", "")
            team_info = team_lookup.get(team_code, {})
            group_teams.append({
                "position": entry.get("position", i + 1),
                "team_id": team_code,
                "team_name": team_info.get("name", team_code),
                "team_logo": team_info.get("flag_url", ""),
                "points": entry.get("points", 0),
                "played": entry.get("played", 0),
                "win": entry.get("w", 0),
                "draw": entry.get("d", 0),
                "lose": entry.get("l", 0),
                "goals_for": entry.get("gf", 0),
                "goals_against": entry.get("ga", 0),
                "goal_difference": entry.get("gd", 0),
            })

        result.append({"name": label, "teams": group_teams})

    return result


def _build_standings_static() -> list:
    data = _fetch_static("matches.json")
    matches = data.get("data", []) if data else []
    data = _fetch_static("teams.json")
    teams = data.get("data", []) if data else []
    team_lookup = {t["code"]: t for t in teams}
    group_matches: dict[str, list] = {}

    for m in matches:
        g = m.get("group")
        if g and m.get("phase") == "group":
            group_matches.setdefault(g, []).append(m)

    result = []

    for gn in sorted(group_matches.keys()):
        group_teams_map: dict[str, dict] = {}
        for code, t in team_lookup.items():
            if t.get("group") == gn:
                group_teams_map[code] = {
                    "team_code": code,
                    "team_name": t.get("name", code),
                    "team_flag": t.get("flag", ""),
                    "played": 0, "win": 0, "draw": 0, "lose": 0,
                    "goals_for": 0, "goals_against": 0, "points": 0,
                }

        for m in group_matches[gn]:
            home, away = m.get("home"), m.get("away")
            sh, sa = m.get("score_home"), m.get("score_away")
            if m.get("status") != "FINISHED" or sh is None or sa is None:
                continue

            for code, side_score, opp_score in [(home, sh, sa), (away, sa, sh)]:
                if code in group_teams_map:
                    t = group_teams_map[code]
                    t["played"] += 1
                    t["goals_for"] += side_score
                    t["goals_against"] += opp_score
                    if side_score > opp_score:
                        t["win"] += 1
                        t["points"] += 3
                    elif side_score == opp_score:
                        t["draw"] += 1
                        t["points"] += 1
                    else:
                        t["lose"] += 1

        sorted_teams = sorted(
            group_teams_map.values(),
            key=lambda t: (-t["points"], -(t["goals_for"] - t["goals_against"]), -t["goals_for"]),
        )

        result.append({
            "name": f"Grupo {gn}",
            "teams": [
                {
                    "position": i + 1,
                    "team_id": t["team_code"],
                    "team_name": t["team_name"],
                    "team_logo": t["team_flag"],
                    "points": t["points"],
                    "played": t["played"],
                    "win": t["win"],
                    "draw": t["draw"],
                    "lose": t["lose"],
                    "goals_for": t["goals_for"],
                    "goals_against": t["goals_against"],
                    "goal_difference": t["goals_for"] - t["goals_against"],
                }
                for i, t in enumerate(sorted_teams)
            ],
        })

    return result


# --- Fixtures ---


def _build_fixtures_live() -> list:
    matches = _fetch_live("/matches")
    matches = matches.get("data", []) if matches else []
    result = []

    for i, m in enumerate(matches):
        raw_status = m.get("status", "")
        phase = m.get("phase", "")

        if raw_status == "completed":
            status = "FT"
        elif raw_status == "in_progress":
            status = "LIVE"
        else:
            status = "SCHEDULED"

        elapsed_map = {"1H": "1H", "HT": "HT", "2H": "2H", "ET1": "ET1", "ET2": "ET2", "PEN": "PEN"}
        elapsed = elapsed_map.get(phase) if status == "LIVE" else None

        home = m.get("home_team") or {}
        away = m.get("away_team") or {}

        result.append({
            "id": m.get("id", i),
            "date": m.get("kickoff_utc", ""),
            "status": status,
            "elapsed": elapsed,
            "round": m.get("round", "group"),
            "group": m.get("group") or m.get("group_name", ""),
            "home": {"id": home.get("code", ""), "name": home.get("name", ""), "logo": ""},
            "away": {"id": away.get("code", ""), "name": away.get("name", ""), "logo": ""},
            "goals": {"home": m.get("home_score"), "away": m.get("away_score")},
        })

    return result


def _build_fixtures_static() -> list:
    data = _fetch_static("matches.json")
    matches = data.get("data", []) if data else []
    result = []

    for i, m in enumerate(matches):
        status = m.get("status", "")
        short_status = "FT" if status == "FINISHED" else "LIVE" if status == "LIVE" else "SCHEDULED"
        result.append({
            "id": m.get("num", i),
            "date": m.get("datetime_utc", ""),
            "status": short_status,
            "elapsed": None,
            "round": m.get("phase", "group"),
            "group": m.get("group", ""),
            "home": {"id": m.get("home"), "name": m.get("home_name", m.get("home")), "logo": ""},
            "away": {"id": m.get("away"), "name": m.get("away_name", m.get("away")), "logo": ""},
            "goals": {"home": m.get("score_home"), "away": m.get("score_away")},
        })

    return result


# --- Public API ---


def build_standings() -> list:
    if _is_live():
        try:
            return _build_standings_live()
        except Exception as e:
            print(f"Live standings failed, falling back to static: {e}")
    return _build_standings_static()


def build_fixtures() -> list:
    if _is_live():
        try:
            return _build_fixtures_live()
        except Exception as e:
            print(f"Live fixtures failed, falling back to static: {e}")
    return _build_fixtures_static()


def _build_topscorers_live() -> list:
    return []


def _build_topscorers_static() -> list:
    data = _fetch_static("matches.json")
    matches = data.get("data", []) if data else []
    team_goals: dict[str, dict] = {}

    for m in matches:
        if m.get("status") != "FINISHED":
            continue
        sh = m.get("score_home")
        sa = m.get("score_away")
        if sh is None or sa is None:
            continue

        for code, name, scored in [
            (m.get("home"), m.get("home_name", m.get("home")), sh),
            (m.get("away"), m.get("away_name", m.get("away")), sa),
        ]:
            if code not in team_goals:
                team_goals[code] = {"team_code": code, "team_name": name, "goals": 0, "matches": 0}
            team_goals[code]["goals"] += scored
            team_goals[code]["matches"] += 1

    sorted_teams = sorted(team_goals.values(), key=lambda t: (-t["goals"], t["team_name"]))
    return [
        {"position": i + 1, "team_code": t["team_code"], "team_name": t["team_name"], "goals": t["goals"], "matches": t["matches"], "avg": round(t["goals"] / t["matches"], 2) if t["matches"] else 0}
        for i, t in enumerate(sorted_teams)
    ]


def build_topscorers() -> list:
    if _is_live():
        try:
            return _build_topscorers_live()
        except Exception as e:
            print(f"Live topscorers failed, falling back to static: {e}")
    return _build_topscorers_static()
