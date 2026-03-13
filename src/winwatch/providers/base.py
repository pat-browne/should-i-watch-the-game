from abc import ABC, abstractmethod

from winwatch.models import GameResult


class LeagueProvider(ABC):
    @abstractmethod
    def latest_result(self, team_name: str) -> GameResult | None:
        """Return latest completed game result for a team, else None."""
