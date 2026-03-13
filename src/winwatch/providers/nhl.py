from datetime import date, datetime, timedelta, timezone

from winwatch.http import get_json
from winwatch.models import GameResult
from winwatch.providers.base import LeagueProvider


class NHLProvider(LeagueProvider):
    """NHL score feed: https://api-web.nhle.com/v1/score/YYYY-MM-DD."""

    def latest_result(self, team_name: str) -> GameResult | None:
        for days_back in range(0, 4):
            day = date.today() - timedelta(days=days_back)
            data = get_json(f"https://api-web.nhle.com/v1/score/{day.isoformat()}", timeout=15)

            for game in data.get("games", []):
                if game.get("gameState") != "OFF":
                    continue
                home = game["homeTeam"]["name"]["default"]
                away = game["awayTeam"]["name"]["default"]
                if team_name.lower() not in {home.lower(), away.lower()}:
                    continue

                home_score = game["homeTeam"]["score"]
                away_score = game["awayTeam"]["score"]
                team_won = home_score > away_score if home.lower() == team_name.lower() else away_score > home_score
                opponent = away if home.lower() == team_name.lower() else home
                start = datetime.fromisoformat(game["startTimeUTC"].replace("Z", "+00:00")).astimezone(timezone.utc)
                return GameResult("nhl", team_name, opponent, start, team_won)
        return None
