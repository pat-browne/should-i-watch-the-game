from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GameResult:
    league: str
    team: str
    opponent: str
    game_time: datetime
    team_won: bool
