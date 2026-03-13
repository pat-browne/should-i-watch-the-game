from winwatch.config import load_settings
from winwatch.service import run_once


if __name__ == "__main__":
    sent = run_once(load_settings())
    print(f"notification_sent={str(sent).lower()}")
