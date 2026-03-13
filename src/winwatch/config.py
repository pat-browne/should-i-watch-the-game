from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    league: str
    team: str
    email_to: str
    email_from: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    poll_interval_seconds: int = 4 * 60 * 60



def load_settings() -> Settings:
    required = {
        "LEAGUE": "league code: nhl or bundesliga",
        "TEAM": "team name",
        "EMAIL_TO": "destination email",
        "EMAIL_FROM": "sender email",
        "SMTP_HOST": "smtp host",
        "SMTP_PORT": "smtp port",
        "SMTP_USER": "smtp username",
        "SMTP_PASSWORD": "smtp password",
    }
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        details = ", ".join(f"{m} ({required[m]})" for m in missing)
        raise ValueError(f"Missing env vars: {details}")

    return Settings(
        league=os.environ["LEAGUE"].strip().lower(),
        team=os.environ["TEAM"].strip(),
        email_to=os.environ["EMAIL_TO"].strip(),
        email_from=os.environ["EMAIL_FROM"].strip(),
        smtp_host=os.environ["SMTP_HOST"].strip(),
        smtp_port=int(os.environ["SMTP_PORT"]),
        smtp_user=os.environ["SMTP_USER"].strip(),
        smtp_password=os.environ["SMTP_PASSWORD"],
        poll_interval_seconds=int(os.getenv("POLL_INTERVAL_SECONDS", 4 * 60 * 60)),
    )
