from telegram import Update, ReplyKeyboardMarkup  # type: ignore

from telegram.ext import (  # type: ignore
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


questions = [
    {
        "question": "1. Что делает input()?",
        "answers": ["Получает данные", "Выводит данные", "Создаёт функцию"],
        "correct": "Получает данные",
    },
    {
        "question": "2. Что делает print()?",
        "answers": ["Сохраняет значение", "Выводит данные", "Сравнивает значения"],
        "correct": "Выводит данные",
    },
    {
        "question": "3. Что такое переменная?",
        "answers": [
            "Имя для хранения значения",
            "Ошибка программы",
            "Команда выхода",
        ],
        "correct": "Имя для хранения значения",
    },
    {
        "question": "4. Какой тип у значения 'Аиша'?",
        "answers": ["int", "str", "bool"],
        "correct": "str",
    },
    {
        "question": "5. Какой тип у числа 14?",
        "answers": ["str", "float", "int"],
        "correct": "int",
    },
    {
        "question": "6. Что означает == ?",
        "answers": ["Присвоить", "Сравнить", "Вывести"],
        "correct": "Сравнить",
    },
    {
        "question": "7. Для чего нужен if?",
        "answers": [
            "Для условия",
            "Для создания файла",
            "Для установки библиотеки",
        ],
        "correct": "Для условия",
    },
    {
        "question": "8. Что делает lower()?",
        "answers": [
            "Делает буквы маленькими",
            "Удаляет текст",
            "Завершает программу",
        ],
        "correct": "Делает буквы маленькими",
    },
    {
        "question": "9. Что означает def?",
        "answers": [
            "Создать функцию",
            "Создать переменную",
            "Запустить цикл",
        ],
        "correct": "Создать функцию",
    },
    {
        "question": "10. Что делает return?",
        "answers": [
            "Возвращает результат функции",
            "Печатает текст",
            "Создаёт условие",
        ],
        "correct": "Возвращает результат функции",
    },
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["question"] = 0
    context.user_data["score"] = 0

    await send_question(update, context)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_number = context.user_data["question"]

    if question_number >= len(questions):
        score = context.user_data["score"]

        await update.message.reply_text(
            f"Викторина закончена!\n"
            f"Твой результат: {score} из {len(questions)}"
        )
        return

    current_question = questions[question_number]

    keyboard = [
        [current_question["answers"][0]],
        [current_question["answers"][1]],
        [current_question["answers"][2]],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await update.message.reply_text(
        current_question["question"],
        reply_markup=reply_markup,
    )


async def answer_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    question_number = context.user_data.get("question")

    if question_number is None:
        await update.message.reply_text(
            "Напиши /start, чтобы начать викторину."
        )
        return

    if question_number >= len(questions):
        await update.message.reply_text(
            "Викторина уже закончена. Напиши /start, чтобы пройти ещё раз."
        )
        return

    user_answer = update.message.text
    current_question = questions[question_number]

    if user_answer == current_question["correct"]:
        context.user_data["score"] += 1

        await update.message.reply_text(
            "Правильно! ✅"
        )

    else:
        await update.message.reply_text(
            f"Неправильно ❌\n"
            f"Правильный ответ: {current_question['correct']}"
        )

    context.user_data["question"] += 1

    await send_question(update, context)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        answer_message,
    )
)

app.run_polling()