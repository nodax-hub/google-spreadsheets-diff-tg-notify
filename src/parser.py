import csv
import logging
from io import StringIO

import requests

logger = logging.getLogger(__name__)


def fetch_range(spreadsheet_id, gid, range_):
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{spreadsheet_id}/export"
        f"?format=csv&gid={gid}&range={range_}"
    )

    logger.debug("Fetching URL: %s", url)

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    text = resp.content.decode("utf-8")
    reader = csv.reader(StringIO(text))
    return list(reader)
