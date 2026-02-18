import hashlib
from urllib.parse import urlparse, parse_qs


def parse_google_sheet_url(url: str):
    parsed = urlparse(url)

    spreadsheet_id = parsed.path.split("/")[3]

    qs = parse_qs(parsed.fragment)
    gid = qs["gid"][0]
    range_ = qs["range"][0]

    return spreadsheet_id, gid, range_


def hash_value(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_google_sheet_url(spreadsheet_id: str, gid: str, range_: str) -> str:
    return (
        "https://docs.google.com/spreadsheets/d/"
        f"{spreadsheet_id}/edit"
        f"?gid={gid}#gid={gid}&range={range_}"
    )
