import logging

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

from storage import add_subscription, remove_subscription, get_subscriptions
from storage import get_subscriptions_by_chat
from utils import build_google_sheet_url
from utils import parse_google_sheet_url

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s started bot", update.message.chat_id)
    await update.message.reply_text(
        "Отправь ссылку Google Sheets с range.\n"
        "Повторная отправка — отписка.\n"
        "/subscriptions — посмотреть активные подписки"
    )


async def subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    logger.info("User %s requested subscriptions list", chat_id)
    subs = get_subscriptions_by_chat(chat_id)

    if not subs:
        await update.message.reply_text("У тебя нет активных подписок.")
        return

    lines = ["Твои подписки:\n"]

    for spreadsheet_id, gid, range_ in subs:
        url = build_google_sheet_url(spreadsheet_id, gid, range_)
        lines.append(url)

    await update.message.reply_text("\n".join(lines))


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    url = update.message.text.strip()

    try:
        spreadsheet_id, gid, range_ = parse_google_sheet_url(url)
    except Exception:
        logger.warning(
            "User %s sent invalid url: %s",
            chat_id,
            url,
        )
        await update.message.reply_text("Неверный формат ссылки.")
        return

    subs = get_subscriptions()
    exists = any(
        s for s in subs
        if s == (chat_id, spreadsheet_id, gid, range_)
    )

    if exists:
        remove_subscription(chat_id, spreadsheet_id, gid, range_)
        logger.info(
            "User %s unsubscribed from %s %s %s",
            chat_id,
            spreadsheet_id,
            gid,
            range_,
        )
        await update.message.reply_text(f"Вы успешно отписались от: {url}")
    else:
        add_subscription(chat_id, spreadsheet_id, gid, range_)
        logger.info(
            "User %s subscribed to %s %s %s",
            chat_id,
            spreadsheet_id,
            gid,
            range_,
        )
        await update.message.reply_text(f"Успешная подписка на {url}.")


def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscriptions", subscriptions))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
