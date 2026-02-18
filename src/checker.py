import logging

from parser import fetch_range
from storage import get_subscriptions, get_last_value, set_last_value
from utils import hash_value

logger = logging.getLogger(__name__)


async def checker(context):
    app = context.application
    subs = get_subscriptions()

    logger.info("Checker tick, subscriptions: %d", len(subs))

    for chat_id, spreadsheet_id, gid, range_ in subs:
        try:
            data = fetch_range(spreadsheet_id, gid, range_)
            raw = str(data)
            h = hash_value(raw)

            last = get_last_value(spreadsheet_id, gid, range_)
            if last and last[0] == h:
                continue

            set_last_value(spreadsheet_id, gid, range_, h, raw)

            if last:
                logger.info(
                    "Change detected: %s %s %s",
                    spreadsheet_id,
                    gid,
                    range_,
                )
                await app.bot.send_message(
                    chat_id,
                    f"Изменение:\n{data}"
                )

        except Exception:
            logger.exception(
                "Error while checking %s %s %s",
                spreadsheet_id,
                gid,
                range_,
            )
