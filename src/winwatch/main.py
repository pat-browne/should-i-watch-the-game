from winwatch.config import load_settings
from winwatch.service import run_forever


if __name__ == "__main__":
    run_forever(load_settings())
