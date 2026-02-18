import logging

from telegram.ext import ApplicationBuilder

from bot import setup_handlers
from checker import checker
from config import TELEGRAM_TOKEN, CHECK_INTERVAL_SECONDS
from logging_config import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()

    logger.info("Starting application")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    setup_handlers(app)

    app.job_queue.run_repeating(
        checker,
        interval=CHECK_INTERVAL_SECONDS,
        first=0,
    )

    logger.info("Bot started, polling enabled")
    app.run_polling()


if __name__ == "__main__":
    main()
