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

@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		match message.text:
			case "1. За сколько до сна":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("за 15 минут", callback_data='before_15min')
				item2 = types.InlineKeyboardButton("за 30 минут", callback_data='before_30min')
				item3 = types.InlineKeyboardButton("за 45 минут", callback_data='before_45min')
				item4 = types.InlineKeyboardButton("за 1 час", callback_data='before_1hour')
				item5 = types.InlineKeyboardButton("за 1 час 30 мин", callback_data='before_1hour45min')
				item6 = types.InlineKeyboardButton("за 2 часа", callback_data='before_2hour')
 
				markup.add(item1, item2, item3, item4, item5, item6)

				bot.send_message(message.chat.id, 'Cколько до сна?', reply_markup=markup)

			case "2. Идеальное время сна":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("7 часов", callback_data='ideal_7Hour')
				item2 = types.InlineKeyboardButton("7 часов 30 минут", callback_data='ideal_7hour30min')
				item3 = types.InlineKeyboardButton("8 часов", callback_data='ideal_8hour')
				item4 = types.InlineKeyboardButton("8 часов 30 минут", callback_data='ideal_8hour30min')
				item5 = types.InlineKeyboardButton("9 часов", callback_data='ideal_9hour')
				item6 = types.InlineKeyboardButton("9 часов", callback_data='ideal_9hour30min')
 
				markup.add(item1, item2, item3, item4, item5, item6)

				bot.send_message(message.chat.id, 'Идеальное время сна', reply_markup=markup)
				
			case "3. Время будильника":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("7 часов", callback_data='alarm_7Hour')
				item2 = types.InlineKeyboardButton("7 часов 30 минут", callback_data='ideal_7hour30min')
				item3 = types.InlineKeyboardButton("8 часов", callback_data='ideal_8hour')
				item4 = types.InlineKeyboardButton("8 часов 30 минут", callback_data='ideal_8hour30min')
				item5 = types.InlineKeyboardButton("9 часов", callback_data='ideal_9hour')
				item6 = types.InlineKeyboardButton("9 часов", callback_data='ideal_9hour30min')
 
				markup.add(item1, item2, item3, item4, item5, item6)

				bot.send_message(message.chat.id, 'Время будильника', reply_markup=markup)
			case "4. Периодичность уведомлений":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("1 минута", callback_data='period_1min')
				item2 = types.InlineKeyboardButton("2 минуты", callback_data='period_2min')
				item3 = types.InlineKeyboardButton("3 минуты", callback_data='period_3min')
				item4 = types.InlineKeyboardButton("4 минуты", callback_data='period_4min')
				item5 = types.InlineKeyboardButton("5 минут", callback_data='period_5min')
				item6 = types.InlineKeyboardButton("10 минут", callback_data='period_10min')
 
				markup.add(item1, item2, item3, item4, item5, item6)

				bot.send_message(message.chat.id, 'Периодичность уведомлений', reply_markup=markup)
			case _:
				bot.send_message(message.chat.id, 'Я не знаю что ответить😢')



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == '15min':
				bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
			elif call.data == '30min':
				bot.send_message(call.message.chat.id, 'Бывает 😢')
 
			# remove inline buttons
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="1. За сколько до сна",
				reply_markup=None)
 
			# show alert
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
 
	except Exception as e:
		print(repr(e))

# RUN
bot.polling(none_stop=True)
