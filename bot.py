def get_answer(message, name):

    if message == "привет":
        return "Привет, " + name + "!"

    elif message == "как дела":
        return "У меня всё хорошо!"

    elif message == "как меня зовут":
        return "Тебя зовут " + name

    else:
        return "Я пока не знаю, что ответить"


name = input("Как тебя зовут? ")

while True:

    message = input("Ты: ").lower()

    if message == "пока":
        print("Бот: Пока!")
        print("Tы - ", name, ", а я - первый Telegram-бот - ", message)
        break

    answer = get_answer(message, name)

    print("Бот:", answer)