import time

from winwatch.config import Settings
from winwatch.notifier import send_watch_email
from winwatch.providers.base import LeagueProvider
from winwatch.providers.bundesliga import BundesligaProvider
from winwatch.providers.nhl import NHLProvider


PROVIDERS: dict[str, LeagueProvider] = {
    "nhl": NHLProvider(),
    "bundesliga": BundesligaProvider(),
}


def run_once(settings: Settings) -> bool:
    provider = PROVIDERS.get(settings.league)
    if not provider:
        raise ValueError(f"Unsupported league: {settings.league}")

    try:
        result = provider.latest_result(settings.team)
    except Exception as exc:
        print(f"provider_error league={settings.league}: {exc}")
        return False

    if not result or not result.team_won:
        return False

    try:
        send_watch_email(
            settings.smtp_host,
            settings.smtp_port,
            settings.smtp_user,
            settings.smtp_password,
            settings.email_from,
            settings.email_to,
            result,
        )
    except Exception as exc:
        print(f"notify_error team={settings.team}: {exc}")
        return False
    return True


def run_forever(settings: Settings) -> None:
    while True:
        run_once(settings)
        time.sleep(settings.poll_interval_seconds)
