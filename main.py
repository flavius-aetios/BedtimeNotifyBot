import telebot
import config
import schedule
from threading import Thread

from time import sleep

from telebot import types
from datetime import datetime, time, timedelta

bot = telebot.TeleBot(config.TOKEN)

beforeTime = time(1, 0)
idealSleepTime = time(8, 30)
alarmTime = time(0, 28)
periodNotifyTime = time(4, 0)
runFlag = False



def notifyMain(chatId):
	print("IN notifyMain LOL!")

	beforeTimeDelta 		= timedelta(hours = beforeTime.hour, 			minutes = beforeTime.minute)
	idealSleepTimeDelta 	= timedelta(hours = idealSleepTime.hour, 		minutes = idealSleepTime.minute)

	nowTime = datetime.now()
	alarmTimeScheduled = datetime.now()

	if nowTime.time() > alarmTime:
		alarmTimeScheduled 			= alarmTimeScheduled.replace(day = alarmTimeScheduled.day + 1, hour = alarmTime.hour, minute = alarmTime.minute, second = 0, microsecond = 0)
		print("alarmTimeScheduled ", alarmTimeScheduled)
	else:
		alarmTimeScheduled 			= alarmTimeScheduled.replace(day = alarmTimeScheduled.day, hour = alarmTime.hour, minute = alarmTime.minute, second = 0, microsecond = 0)
		print("alarmTimeScheduled ", alarmTimeScheduled)


	delta = timedelta(hours = beforeTime.hour)
	print(delta)

	now = datetime.now()

	now = now - delta
	print(now)

	less = alarmTimeScheduled - idealSleepTimeDelta - beforeTimeDelta
	print("\nLess = ", less)

	more = alarmTimeScheduled - idealSleepTimeDelta + timedelta(hours=2)
	print("More = ", more)

	# Время оставшееся до сна
	leftTime = alarmTimeScheduled - idealSleepTimeDelta - datetime.now()
	if leftTime.days < 0:
		timeToSleep = True
		# Время оставшееся для сна
		leftTime = alarmTimeScheduled - datetime.now()
		print("Уже нужно спать!")
	else:
		timeToSleep = False
	
	print("leftTime = ", leftTime)

	# Если текущее время в промежутке между времененм до сна и временем отхода ко сну + ещё некоторое время
	if datetime.now() > alarmTimeScheduled - idealSleepTimeDelta - beforeTimeDelta and datetime.now() < alarmTimeScheduled - idealSleepTimeDelta + timedelta(hours=2):
		global msg
		try: msg
		except NameError: msg = None

		if msg is None:
			print("MSG IS NOT DEFINE!")
		else:
			bot.delete_message(chatId, msg.message_id)
			print("DEL MSG")

		if timeToSleep is True:
			msg = bot.send_message(chatId, 'Пора спать! До пробуждения осталось: ' + ':'.join(str(leftTime).split(':')[:2]) + "! Вставать в " + alarmTime.strftime("%H:%M"))
		else:
			msg = bot.send_message(chatId, 'Пора спать через ' + ':'.join(str(leftTime).split(':')[:2]) + "! Вставать в " + alarmTime.strftime("%H:%M"))

@bot.message_handler(commands=['start'])
def welcome(message):
	
	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("1. Сигнал отхода ко сну")
	item2 = types.KeyboardButton("2. Идеальное время сна")
	item3 = types.KeyboardButton("3. Время будильника")
	item4 = types.KeyboardButton("4. Периодичность уведомлений")
	item5 = types.KeyboardButton("Запуск!")
	item6 = types.KeyboardButton("Стоп!")

	markup.add(item1, item2, item3, item4, item5, item6)

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def keyBut(message):
	if message.chat.type == 'private':
		match message.text:
			case "1. Сигнал отхода ко сну":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("за 15 минут", 		callback_data='before_15min')
				item2 = types.InlineKeyboardButton("за 30 минут", 		callback_data='before_30min')
				item3 = types.InlineKeyboardButton("за 45 минут", 		callback_data='before_45min')
				item4 = types.InlineKeyboardButton("за 1 час", 			callback_data='before_1hour')
				item5 = types.InlineKeyboardButton("за 1 час 30 мин", 	callback_data='before_1hour45min')
				item6 = types.InlineKeyboardButton("за 2 часа", 		callback_data='before_2hour')
 
				markup.add(item1, item2, item3, item4, item5, item6)

				bot.send_message(message.chat.id, 'Начинать присылать уведомления', reply_markup=markup)

			case "2. Идеальное время сна":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("7 часов", 			callback_data='ideal_7Hour')
				item2 = types.InlineKeyboardButton("7 часов 30 минут", 	callback_data='ideal_7hour30min')
				item3 = types.InlineKeyboardButton("8 часов", 			callback_data='ideal_8hour')
				item4 = types.InlineKeyboardButton("8 часов 30 минут", 	callback_data='ideal_8hour30min')
				item5 = types.InlineKeyboardButton("9 часов", 			callback_data='ideal_9hour')
				item6 = types.InlineKeyboardButton("9 часов 30 минут",  callback_data='ideal_9hour30min')
 
				markup.add(item1, item2, item3, item4, item5, item6)

				bot.send_message(message.chat.id, 'Идеальное время сна', reply_markup=markup)
				
			case "3. Время будильника":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("6 часов", 			callback_data='alarm_6Hour')
				item2 = types.InlineKeyboardButton("6 часов 30 минут", 	callback_data='alarm_6Hour30min')
				item3 = types.InlineKeyboardButton("7 часов", 			callback_data='alarm_7Hour')
				item4 = types.InlineKeyboardButton("7 часов 30 минут", 	callback_data='alarm_7hour30min')
				item5 = types.InlineKeyboardButton("8 часов", 			callback_data='alarm_8hour')
				item6 = types.InlineKeyboardButton("8 часов 30 минут", 	callback_data='alarm_8hour30min')
				item7 = types.InlineKeyboardButton("9 часов", 			callback_data='alarm_9hour')
				item8 = types.InlineKeyboardButton("9 часов 30 минут",	callback_data='alarm_9hour30min')
 
				markup.add(item1, item2, item3, item4, item5, item6, item7, item8)

				bot.send_message(message.chat.id, 'Время будильника', reply_markup=markup)
			
			case "4. Периодичность уведомлений":
				markup = types.InlineKeyboardMarkup(row_width=1)
				item1 = types.InlineKeyboardButton("1 минута", 	callback_data='periodNotify_1min')
				item2 = types.InlineKeyboardButton("2 минуты", 	callback_data='periodNotify_2min')
				item3 = types.InlineKeyboardButton("3 минуты", 	callback_data='periodNotify_3min')
				item4 = types.InlineKeyboardButton("4 минуты", 	callback_data='periodNotify_4min')
				item5 = types.InlineKeyboardButton("5 минут", 	callback_data='periodNotify_5min')
				item6 = types.InlineKeyboardButton("10 минут", 	callback_data='periodNotify_10min')
 
				markup.add(item1, item2, item3, item4, item5, item6)

				bot.send_message(message.chat.id, 'Периодичность уведомлений', reply_markup=markup)

			case "Запуск!":
				# schedule.every(periodNotifyTime.minute).minute.do(notifyMain, message.chat.id)
				schedule.every(15).seconds.do(notifyMain, message.chat.id)

				bot.send_message(message.chat.id, 'Уведомления запущены!')

			case "Стоп!":
				schedule.clear()

				bot.send_message(message.chat.id, 'Уведомления остановлены!')

			case _:
				bot.send_message(message.chat.id, 'Я не знаю что ответить😢')



# ---------------BEFORE TIME-----------------
@bot.callback_query_handler(func=lambda call: call.data == "before_15min")
def before_15min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Уведомления до сна: <b>за 15 мин</b>", parse_mode='html',)
	global beforeTime
	beforeTime = time(0, 15)

@bot.callback_query_handler(func=lambda call: call.data == "before_30min")
def before_30min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Уведомления до сна: <b>за 30 минут</b>", parse_mode='html',)
	global beforeTime
	beforeTime = time(0, 30)

@bot.callback_query_handler(func=lambda call: call.data == "before_45min")
def before_45min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Уведомления до сна: <b>за 45 минут</b>", parse_mode='html',)
	global beforeTime
	beforeTime = time(0, 45)

@bot.callback_query_handler(func=lambda call: call.data == "before_1hour")
def before_1hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Уведомления до сна: <b>за 1 час</b>", parse_mode='html',)
	global beforeTime
	beforeTime = time(1, 0)

@bot.callback_query_handler(func=lambda call: call.data == "before_1hour45min")
def before_1hour45min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Уведомления до сна: <b>за 1 час 30 мин</b>", parse_mode='html',)
	global beforeTime
	beforeTime = time(1, 30)

@bot.callback_query_handler(func=lambda call: call.data == "before_2hour")
def before_2hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Уведомления до сна: <b>за 2 часа</b>", parse_mode='html',)
	global beforeTime
	beforeTime = time(2, 0)


# ------------------IDEAL TIME------------------
@bot.callback_query_handler(func=lambda call: call.data == "ideal_7Hour")
def ideal_7Hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Идеальное время сна: <b>7 часов</b>", parse_mode='html',)
	global idealSleepTime
	idealSleepTime = time(7, 0)

@bot.callback_query_handler(func=lambda call: call.data == "ideal_7hour30min")
def ideal_7hour30min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Идеальное время сна: <b>7 часов 30 минут</b>", parse_mode='html',)
	global idealSleepTime
	idealSleepTime = time(7, 30)

@bot.callback_query_handler(func=lambda call: call.data == "ideal_8hour")
def ideal_8hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Идеальное время сна: <b>8 часов</b>", parse_mode='html',)
	global idealSleepTime
	idealSleepTime = time(8, 0)

@bot.callback_query_handler(func=lambda call: call.data == "ideal_8hour30min")
def ideal_8hour30min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Идеальное время сна: <b>8 часов 30 минут</b>", parse_mode='html',)
	global idealSleepTime
	idealSleepTime = time(8, 30)

@bot.callback_query_handler(func=lambda call: call.data == "ideal_9hour")
def ideal_9hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Идеальное время сна: <b>9 часов</b>", parse_mode='html',)
	global idealSleepTime
	idealSleepTime = time(9, 0)

@bot.callback_query_handler(func=lambda call: call.data == "ideal_9hour30min")
def ideal_9hour30min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Идеальное время сна: <b>9 часов 30 минут</b>", parse_mode='html',)
	global idealSleepTime
	idealSleepTime = time(9, 30)


# ------------------ALARM TIME------------------
@bot.callback_query_handler(func=lambda call: call.data == "alarm_6Hour")
def alarm_7Hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>6 часов</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(6, 0)

@bot.callback_query_handler(func=lambda call: call.data == "alarm_6Hour30min")
def alarm_7Hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>6 часов 30 минут</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(6, 30)

@bot.callback_query_handler(func=lambda call: call.data == "alarm_7Hour")
def alarm_7Hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>7 часов</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(7, 0)

@bot.callback_query_handler(func=lambda call: call.data == "alarm_7hour30min")
def alarm_7hour30min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>7 часов 30 минут</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(7, 30)

@bot.callback_query_handler(func=lambda call: call.data == "alarm_8hour")
def alarm_8hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>8 часов</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(8, 0)

@bot.callback_query_handler(func=lambda call: call.data == "alarm_8hour30min")
def alarm_8hour30min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>8 часов 30 минут</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(8, 30)

@bot.callback_query_handler(func=lambda call: call.data == "alarm_9hour")
def alarm_9hour_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>9 часов</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(9, 0)

@bot.callback_query_handler(func=lambda call: call.data == "alarm_9hour30min")
def alarm_9hour30min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Будильник прозвенит в: <b>9 часов 30 минут</b>", parse_mode='html',)
	global alarmTime
	alarmTime = time(9, 30)


# ------------------PERIOD TIME------------------
@bot.callback_query_handler(func=lambda call: call.data == "periodNotify_1min")
def periodNotify_1min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Период повторения: <b>1 минута</b>", parse_mode='html',)
	global periodNotifyTime
	periodNotifyTime = time(0, 1)

@bot.callback_query_handler(func=lambda call: call.data == "periodNotify_2min")
def periodNotify_2min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Период повторения: <b>2 минуты</b>", parse_mode='html',)
	global periodNotifyTime
	periodNotifyTime = time(0, 2)

@bot.callback_query_handler(func=lambda call: call.data == "periodNotify_3min")
def periodNotify_3min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Период повторения: <b>3 минуты</b>", parse_mode='html',)
	global periodNotifyTime
	periodNotifyTime = time(0, 3)

@bot.callback_query_handler(func=lambda call: call.data == "periodNotify_4min")
def periodNotify_4min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Период повторения: <b>4 минуты</b>", parse_mode='html',)
	global periodNotifyTime
	periodNotifyTime = time(0, 4)

@bot.callback_query_handler(func=lambda call: call.data == "periodNotify_5min")
def periodNotify_5min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Период повторения: <b>5 минут</b>", parse_mode='html',)
	global periodNotifyTime
	periodNotifyTime = time(0, 5)

@bot.callback_query_handler(func=lambda call: call.data == "periodNotify_10min")
def periodNotify_10min_pressed(call: types.CallbackQuery):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None, text="Период повторения: <b>10 минут</b>", parse_mode='html',)
	global periodNotifyTime
	periodNotifyTime = time(0, 10)

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

scheduleThread = Thread(target=schedule_checker)
scheduleThread.daemon = True
scheduleThread.start()

bot.polling(none_stop=True)

