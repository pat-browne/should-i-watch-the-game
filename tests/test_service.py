import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from winwatch.models import GameResult
from winwatch.service import run_once


class DummyProvider:
    def __init__(self, won: bool):
        self.won = won

    def latest_result(self, team_name: str):
        return GameResult("nhl", team_name, "Other", datetime.now(timezone.utc), self.won)


class FailingProvider:
    def latest_result(self, _team_name: str):
        raise RuntimeError("api unavailable")


class DummySettings:
    league = "nhl"
    team = "Team A"
    smtp_host = "smtp.test"
    smtp_port = 587
    smtp_user = "u"
    smtp_password = "p"
    email_from = "from@test"
    email_to = "to@test"


class ServiceTests(unittest.TestCase):
    def test_run_once_no_email_when_team_lost(self):
        with patch("winwatch.service.PROVIDERS", {"nhl": DummyProvider(False)}), patch(
            "winwatch.service.send_watch_email"
        ) as send_mock:
            self.assertFalse(run_once(DummySettings()))
            send_mock.assert_not_called()

    def test_run_once_sends_email_when_team_won(self):
        with patch("winwatch.service.PROVIDERS", {"nhl": DummyProvider(True)}), patch(
            "winwatch.service.send_watch_email"
        ) as send_mock:
            self.assertTrue(run_once(DummySettings()))
            send_mock.assert_called_once()

    def test_run_once_returns_false_on_provider_error(self):
        with patch("winwatch.service.PROVIDERS", {"nhl": FailingProvider()}):
            self.assertFalse(run_once(DummySettings()))

    def test_run_once_returns_false_on_notify_error(self):
        with patch("winwatch.service.PROVIDERS", {"nhl": DummyProvider(True)}), patch(
            "winwatch.service.send_watch_email", side_effect=RuntimeError("smtp down")
        ):
            self.assertFalse(run_once(DummySettings()))


if __name__ == "__main__":
    unittest.main()
