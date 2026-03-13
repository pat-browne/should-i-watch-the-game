import json
from urllib.request import urlopen


def get_json(url: str, timeout: int = 15):
    with urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))
