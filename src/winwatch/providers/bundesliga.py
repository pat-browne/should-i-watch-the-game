from datetime import datetime

from winwatch.http import get_json
from winwatch.models import GameResult
from winwatch.providers.base import LeagueProvider


class BundesligaProvider(LeagueProvider):
    """OpenLigaDB feed for Bundesliga 1 (no key)."""

    def latest_result(self, team_name: str) -> GameResult | None:
        season = datetime.utcnow().year
        candidates = []
        for year in (season, season - 1):
            for matchday in range(34, 0, -1):
                data = get_json(f"https://api.openligadb.de/getmatchdata/bl1/{year}/{matchday}", timeout=15)
                for game in data:
                    if not game.get("MatchIsFinished"):
                        continue
                    home = game["Team1"]["TeamName"]
                    away = game["Team2"]["TeamName"]
                    if team_name.lower() not in {home.lower(), away.lower()}:
                        continue
                    result = next(
                        (r for r in game.get("MatchResults", []) if r.get("ResultName") == "Endergebnis"),
                        None,
                    )
                    if not result:
                        continue
                    home_score = result["PointsTeam1"]
                    away_score = result["PointsTeam2"]
                    team_won = home_score > away_score if home.lower() == team_name.lower() else away_score > home_score
                    opponent = away if home.lower() == team_name.lower() else home
                    match_time = datetime.fromisoformat(game["MatchDateTimeUTC"].replace("Z", "+00:00"))
                    candidates.append(GameResult("bundesliga", team_name, opponent, match_time, team_won))
                if candidates:
                    return sorted(candidates, key=lambda x: x.game_time, reverse=True)[0]
        return None
