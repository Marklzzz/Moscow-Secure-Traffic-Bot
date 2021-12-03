# Импортируем необходимые классы.
from secrets import API_KEY
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import ConversationHandler, CommandHandler
from telegram import ReplyKeyboardMarkup

WAITING_FOR_AUTH = range(1)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.
def hello(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.

    message1 = 'Привет. Меня зовут Кибер-бот! \nЯ хочу помочь тебе разобраться с такой непростой вещью, как кибербезопасность.'
    message2 = 'Обещаю, что обучение будет нескучным и продуктивным!'

    update.message.reply_text(message1)
    update.message.reply_text(message2)
    start(update, context)


def start(update, context):
    user_id = update.message.from_user.id
    message = 'Давай начнем с авторизации. Я храню результаты своих пользователей, чтобы они могли сохранить их даже при создании нового аккаунта в Telegram.'
    markup = ReplyKeyboardMarkup([['Войти'], ['Зарегестрироваться']], one_time_keyboard=False)
    update.message.reply_text(message, reply_markup=markup)
    return WAITING_FOR_AUTH


def register(update, context):
    update.message.reply_text('ЗАРЕГИСТРИРОВАН')


def log_in(update, context):
    update.message.reply_text('ВХОД ВЫПОЛНЕН')


def zero(update, context):
    pass


def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', hello)],
        states={
            WAITING_FOR_AUTH: [MessageHandler(Filters.regex('^(Зарегестрироваться)$'), register),
                               MessageHandler(Filters.regex('^(Войти)$'), log_in)]
        },
        fallbacks=[CommandHandler('cancel', zero)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
