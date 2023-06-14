import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	
	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("1. За сколько до сна")
	item2 = types.KeyboardButton("2. Идеальное время сна")
	item3 = types.KeyboardButton("3. Время будильника")
	item4 = types.KeyboardButton("4. Периодичность уведомлений")

	markup.add(item1, item2, item3, item4)

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)

# @bot.message_handler(content_types=['text'])
# def echo(message):
# 	bot.send_message(message.chat.id, message.text)

# RUN
bot.polling(none_stop=True)
