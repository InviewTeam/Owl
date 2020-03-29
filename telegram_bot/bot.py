import telebot
import os
from dotenv import find_dotenv,load_dotenv
from service_functions import load_setting, get_one_metric
load_dotenv(find_dotenv())


token=os.environ['TOKEN']
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Уху Уху")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Привет, я сова")
    elif message.text == '/settings':
        settings(message)
    else:
        bot.send_message(message.from_user.id, "I don't know")

def settings(message):
    result = load_setting()
    settings = result['settings']
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(len(settings)):
        keyboard.row(
            telebot.types.InlineKeyboardButton(text=settings[i]['metric'], callback_data=settings[i]['metric'])
        )
    bot.send_message(
        message.chat.id,
        'Get info about Settings',
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call:True)
def iq_callback(query):
    data = query.data
    print(data)
    result=get_one_metric(data)
    answer = '<b>' + data + ':</b>\n\n' + \
             'From: ' + str(result['from']) + '\n' + \
             'To: ' + str(result['to'])
    bot.send_message(
        query.message.chat.id,
        answer,
        parse_mode='HTML'
    )


bot.polling(none_stop=True, interval=0)


