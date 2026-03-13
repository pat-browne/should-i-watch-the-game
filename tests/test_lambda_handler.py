import unittest
from unittest.mock import patch

from winwatch.lambda_handler import handler


class LambdaHandlerTests(unittest.TestCase):
    def test_handler_returns_notification_status(self):
        with patch("winwatch.lambda_handler.load_settings") as load_mock, patch(
            "winwatch.lambda_handler.run_once", return_value=True
        ) as run_mock:
            result = handler({}, {})

        load_mock.assert_called_once()
        run_mock.assert_called_once()
        self.assertEqual(result, {"notification_sent": True})


if __name__ == "__main__":
    unittest.main()
