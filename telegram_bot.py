from telegram import Update, ReplyKeyboardMarkup  # type: ignore

from telegram.ext import (  # type: ignore
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os
from dotenv import load_dotenv

load_dotenv()

# Получаем токен бота из переменной окружения.
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# chat_id владельца, которому бот будет отправлять новые записи.
OWNER_CHAT_ID = int(os.getenv("OWNER_CHAT_ID"))


# Эта функция вызывается, когда пользователь пишет /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Очищаем старые данные пользователя.
    # Например, если он уже раньше проходил запись.
    context.user_data.clear()

    # Сохраняем текущий шаг.
    # Сейчас бот ждёт имя пользователя.
    context.user_data["var"] = "name"

    await update.message.reply_text(
        "Привет! Как тебя зовут?"
    )


# Эта функция будет обрабатывать обычные сообщения пользователя.
async def answer_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # Получаем текст сообщения.
    # strip() убирает лишние пробелы в начале и конце.
    message = update.message.text.strip()

    # Получаем текущий шаг пользователя.
    step = context.user_data.get("var")


    # -------------------------
    # ШАГ 1. Получаем имя
    # -------------------------

    if step == "name":

        # Сохраняем имя пользователя.
        context.user_data["name"] = message

        # Теперь переходим к следующему шагу.
        context.user_data["var"] = "service"

        # Создаём кнопки с услугами.
        keyboard = [
            ["Маникюр", "Стрижка"],
            ["Консультация"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            f"Приятно познакомиться, {message}!\n"
            "Выбери услугу:",
            reply_markup=reply_markup
        )


    # -------------------------
    # ШАГ 2. Получаем услугу
    # -------------------------

    elif step == "service":

        # Сохраняем выбранную услугу.
        context.user_data["service"] = message

        # Теперь ждём время.
        context.user_data["var"] = "time"

        # Кнопки с доступным временем.
        keyboard = [
            ["15:00", "17:00"],
            ["19:00"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            f"Ты выбрала: {message}\n"
            "Теперь выбери время:",
            reply_markup=reply_markup
        )


    # -------------------------
    # ШАГ 3. Получаем время
    # -------------------------

    elif step == "time":

        # Сохраняем время.
        context.user_data["time"] = message

        # Следующий шаг — подтверждение.
        context.user_data["var"] = "confirm"

        # Достаём ранее сохранённые данные.
        name = context.user_data["name"]
        service = context.user_data["service"]
        time = context.user_data["time"]

        keyboard = [
            ["Да", "Нет"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        # Показываем пользователю все данные перед подтверждением.
        await update.message.reply_text(
            "Проверь запись:\n\n"
            f"Имя: {name}\n"
            f"Услуга: {service}\n"
            f"Время: {time}\n\n"
            "Подтвердить?",
            reply_markup=reply_markup
        )


    # -------------------------
    # ШАГ 4. Подтверждение
    # -------------------------

    elif step == "confirm":

        # Делаем ответ маленькими буквами,
        # чтобы "ДА", "Да" и "да" работали одинаково.
        answer = message.lower()

        if answer == "да":

            # Ещё раз достаём сохранённые данные.
            name = context.user_data["name"]
            service = context.user_data["service"]
            time = context.user_data["time"]

            # Сообщаем пользователю, что запись создана.
            await update.message.reply_text(
                "Запись подтверждена ✅"
            )

            # Отправляем сообщение владельцу.
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=(
                    "Новая запись!\n\n"
                    f"Имя: {name}\n"
                    f"Услуга: {service}\n"
                    f"Время: {time}"
                )
            )

            # Отмечаем, что сценарий завершён.
            context.user_data["var"] = "done"

        elif answer == "нет":

            # Если пользователь отказался,
            # очищаем старые данные.
            context.user_data.clear()

            # И начинаем сценарий сначала.
            context.user_data["var"] = "name"

            await update.message.reply_text(
                "Хорошо, начнём заново.\n"
                "Как тебя зовут?"
            )

        else:

            await update.message.reply_text(
                "Пожалуйста, выбери Да или Нет."
            )


    # -------------------------
    # Если пользователь пишет что-то вне сценария
    # -------------------------

    else:

        await update.message.reply_text(
            "Напиши /start, чтобы начать запись."
        )


# Создаём Telegram-приложение и передаём ему токен.
app = ApplicationBuilder().token(TOKEN).build()


# Если пользователь пишет /start,
# вызываем функцию start().
app.add_handler(
    CommandHandler("start", start)
)

# Все обычные текстовые сообщения
# отправляем в функцию answer_message().
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        answer_message
    )
)


# Запускаем бота.
# run_polling() постоянно проверяет новые сообщения в Telegram.
app.run_polling()