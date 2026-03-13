from winwatch.config import load_settings
from winwatch.service import run_once


def handler(_event, _context):
    sent = run_once(load_settings())
    return {"notification_sent": sent}
