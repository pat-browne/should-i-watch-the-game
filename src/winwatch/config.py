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


def _read_value(key: str, prefixes: tuple[str, ...]) -> str | None:
    for prefix in prefixes:
        value = os.getenv(f"{prefix}{key}")
        if value:
            return value
    return None


def load_settings(prefixes: tuple[str, ...] | None = None) -> Settings:
    """Load config from env vars.

    Default behavior:
    - Lambda: checks LAMBDA_* first, then base names.
    - Non-Lambda: checks base names.
    """
    running_in_lambda = bool(os.getenv("AWS_LAMBDA_FUNCTION_NAME"))
    resolved_prefixes = prefixes or (("LAMBDA_", "") if running_in_lambda else ("",))

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

    values: dict[str, str] = {}
    missing = []
    for key in required:
        value = _read_value(key, resolved_prefixes)
        if value is None:
            missing.append(key)
        else:
            values[key] = value

    if missing:
        details = ", ".join(f"{m} ({required[m]})" for m in missing)
        raise ValueError(f"Missing env vars: {details}")

    poll_interval = _read_value("POLL_INTERVAL_SECONDS", resolved_prefixes)

    return Settings(
        league=values["LEAGUE"].strip().lower(),
        team=values["TEAM"].strip(),
        email_to=values["EMAIL_TO"].strip(),
        email_from=values["EMAIL_FROM"].strip(),
        smtp_host=values["SMTP_HOST"].strip(),
        smtp_port=int(values["SMTP_PORT"]),
        smtp_user=values["SMTP_USER"].strip(),
        smtp_password=values["SMTP_PASSWORD"],
        poll_interval_seconds=int(poll_interval or 4 * 60 * 60),
    )
