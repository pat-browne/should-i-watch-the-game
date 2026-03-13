import os
import unittest
from unittest.mock import patch

from winwatch.config import load_settings


class ConfigTests(unittest.TestCase):
    def test_load_settings_uses_lambda_prefixed_vars_in_lambda_runtime(self):
        env = {
            "AWS_LAMBDA_FUNCTION_NAME": "watcher",
            "LAMBDA_LEAGUE": "nhl",
            "LAMBDA_TEAM": "Team A",
            "LAMBDA_EMAIL_TO": "to@test",
            "LAMBDA_EMAIL_FROM": "from@test",
            "LAMBDA_SMTP_HOST": "smtp.test",
            "LAMBDA_SMTP_PORT": "587",
            "LAMBDA_SMTP_USER": "u",
            "LAMBDA_SMTP_PASSWORD": "p",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = load_settings()

        self.assertEqual(settings.team, "Team A")
        self.assertEqual(settings.league, "nhl")

    def test_load_settings_falls_back_to_unprefixed_vars(self):
        env = {
            "AWS_LAMBDA_FUNCTION_NAME": "watcher",
            "LEAGUE": "bundesliga",
            "TEAM": "Bayern Munich",
            "EMAIL_TO": "to@test",
            "EMAIL_FROM": "from@test",
            "SMTP_HOST": "smtp.test",
            "SMTP_PORT": "587",
            "SMTP_USER": "u",
            "SMTP_PASSWORD": "p",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = load_settings()

        self.assertEqual(settings.team, "Bayern Munich")
        self.assertEqual(settings.league, "bundesliga")


if __name__ == "__main__":
    unittest.main()
