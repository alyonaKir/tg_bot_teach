from telegram import Update  # type: ignore

from telegram.ext import (  # type: ignore
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def get_answer(message):

    if message == "привет":
        return "Привет!"

    elif message == "как дела":
        return "У меня всё хорошо!"

    elif message == "кто ты":
        return "Я первый Telegram-бот Аиши!"

    elif message == "ты ии":
        return "Пока нет, но скоро меня подключат к ИИ!"

    else:
        return "Я пока не знаю, что ответить"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Привет! Напиши мне что-нибудь."
    )


async def answer_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message.text.lower()

    answer = get_answer(message)

    await update.message.reply_text(answer)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        answer_message
    )
)

app.run_polling()