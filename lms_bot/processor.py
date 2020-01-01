# coding: utf-8
# Seems we'll have all headaches here, I hope no ones ever reads this. Now let's move to stuff...
# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

### Have to do this for it to work in 1.9.x!
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests as r
from database import DataBase
import telebot
from strings import get_string
from telegraph import *
import json
from time import sleep
from tools import Logger, unix_to_date
import api
from models import *
import time
from telebot import types
import threading
from random import choice
from datetime import timedelta

logger = Logger("processor")
logger.deactivate()

beta_group = 0  # ID of "Hero" tg-group (need to replace 0 with real ID)
token = "BOT_TOKEN"
bot  = telebot.TeleBot(token)
db = DataBase()
owners = [] # Tg IDs of owners

def create_streams(streams):
	# TODO: body to create streams
	pass

@bot.message_handler()
def handle(m):
	text = m.text
	uid = m.from_user.id
	cid = m.chat.id
	try:
		user_real_name = db.get_user_name(uid)
	except:
		user_real_name = None

	status = db.get_status(uid)
	logger.log("status = {}".format(status))

	if status == 'reg' and m.chat.type == 'private':
		if not text.startswith('/'):
			data = text.split()
			valid = True
			if len(data) == 2:
				lgn = data[0]
				pswd = data[1]
			elif len(data) == 3:
				lgn = ' '.join(data[:2])
				pswd = data[2]
			else:
				valid = False
			if valid:
				keyboard = types.InlineKeyboardMarkup()
				yes = types.InlineKeyboardButton(text=get_string('reg_check_credentials_yes_button'), callback_data="lgn_{}|{}".format(lgn, pswd))
				no = types.InlineKeyboardButton(text=get_string('reg_check_credentials_no_button'), callback_data="lgn_no")
				keyboard.add(yes, no)
				bot.send_message(uid, get_string('reg_check_credentials').format(login=lgn, password=pswd), reply_markup=keyboard, parse_mode='html')
				bot.delete_message(uid, m.message_id)
				db.set_status(uid, 'halo')
			else:
				bot.reply_to(m, get_string('reg_invalid_input'), parse_mode='html')
			return

	if text.startswith("/start"):
		db.register(uid)
		db.set_status(uid, "start")
		db_response = db.register(tg_id=uid)
		if text == "/start":
			if db_response == 0:
				bot.reply_to(m, choice(get_string('start')), parse_mode='html')
			else:
				bot.reply_to(m, get_string('first_start'), parse_mode='html')
		else:
			data = text.split(" ")[1]
			if data == "login":
				user_data = db.get_user_data(tg_id=uid)
				if user_data.name:
					logger.log(user_data.token, type(user_data.token))
					keyboard = types.InlineKeyboardMarkup()
					url_button = types.InlineKeyboardButton(text=get_string('deep_linking_login_success_button'), url="http://ukkix.app/login?data={}".format(user_data.token))
					keyboard.add(url_button)
					bot.reply_to(m, get_string('deep_linking_login_success').format(token=user_data.token), parse_mode='html', reply_markup=keyboard)
				else:
					bot.reply_to(m, get_string('not_authorized'), parse_mode='html')
			else:
				decoded = base64.b64decode(data).decode("utf-8")
				logger.log(type(decoded))
				if decoded.startswith("sp"):
					decoded = decoded.replace("sp", "", 1).split("_")
					user_id = int(decoded[0])
					last_name = decoded[1]
					first_name = decoded[2]
					user_data = db.get_user_data(user_id=user_id)
					if user_data != None and user_real_name != None:
						if user_real_name.split(" ")[0].endswith("a"):
							if user_data.name.split(" ")[0].endswith("a"):
								bot.reply_to(m, get_string('tg_profile').format(name='{} {}'.format(last_name, first_name), tg_id=user_data.telegram_accounts[0].tg_id), parse_mode='html')
							else:
								bot.reply_to(m, get_string('tg_profile_only_girls'), parse_mode='html')
						else:
							if not user_data.name.split(" ")[0].endswith("a"):
								bot.reply_to(m, get_string('tg_profile').format(name='{} {}'.format(last_name, first_name), tg_id=user_data.telegram_accounts[0].tg_id), parse_mode='html')
							else:
								bot.reply_to(m, get_string('tg_profile_only_boys'), parse_mode='html')
					else:
						bot.reply_to(m, get_string('tg_profile_target_not_found'), parse_mode='html')
				elif decoded.startswith("dl"):
					bot.reply_to(m, get_string('files_not_functioning'))
					return
					short_link = decoded.replace('dl', '', 1)
					complete_url = 'https://lms.tuit.uz/uploads/{short_link}'.format(short_link=short_link)
					file_name = complete_url.split("/")[-1]
					msg = bot.reply_to(m, get_string('files_searching'))
					existing_file = db.get_tg_file(short_link)
					if existing_file:
						bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=get_string('files_sending'), parse_mode='html')
						bot.send_chat_action(uid, 'upload_document')
						bot.send_document(uid, existing_file, caption=get_string('files_caption').format(file_name.split(".")[-1]))
						bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=get_string('files_file_ready'), parse_mode='html')
					else:	
						try:
							file = r.get(complete_url, timeout=5)
						except:
							bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=get_string('files_file_dl_error'), parse_mode='html')
							return
						if file.status_code == 200:
							with open(file_name, "wb") as f:
								f.write(file.content)
							with open(file_name, "rb") as f:
								bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=get_string('files_sending'), parse_mode='html')
								bot.send_chat_action(uid, 'upload_document')
								new_file_id = bot.send_document(uid, f, caption=get_string('files_caption').format(file_name.split(".")[-1]))
								bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=get_string('files_file_ready'), parse_mode='html')
								db.store_tg_file(short_link, new_file_id.document.file_id)
								os.remove(file_name)
						else:
							bot.send_message(uid, get_string('files_not_found'))
	
	elif text.startswith("/terms"):
		bot.reply_to(m, get_string('terms'), parse_mode='html')
		if status == 'reg':
			db.set_status(uid, 'terms')

	elif text.startswith("/friends"):
		user_id = db.is_logged(uid)
		if user_id:
			logger.log(user_id)
			msg = bot.reply_to(m, get_string('friends_searching'), parse_mode='html')
			started = time.time()
			friends = db.get_friends(user_id)
			finished = time.time()
			logger.log(friends)
			bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=get_string('friends_search_completed'), parse_mode='html')
			new_page_url = generate_friends_page(user_id, friends)
			bot.edit_message_text(chat_id=cid, message_id=msg.message_id, text=get_string('friends_result').format(link=new_page_url, name=user_real_name, search_time=finished-started), parse_mode='html')
		else:
			bot.reply_to(m, get_string('not_authorized'), parse_mode='html')
		if status == 'reg':
			db.set_status(uid, 'friends')

	elif text.startswith("/reg"):
		if m.chat.type == 'private':
			db.set_status(uid, "reg")
			bot.reply_to(m, get_string('registration'), parse_mode='html')
		else:
			bot.reply_to(m, get_string('command_restricted_in_group'))

	elif text.startswith('/token'):
		user_data = db.get_user_data(tg_id=uid)
		if True: # there was a good condition, but I deleted it and put True
			if m.chat.type == 'private':
				if user_data.name:
					logger.log(user_data.token, type(user_data.token))
					bot.reply_to(m, get_string('token_info').format(token=user_data.token), parse_mode='html')
				else:
					bot.reply_to(m, get_string('not_authorized'), parse_mode='html')
			else:
				bot.reply_to(m, get_string('command_restricted_in_group'))
		else:
			bot.reply_to(m, get_string('user_not_permitted'))

	elif text.startswith('/me'):
		user_data = db.get_user_data(tg_id=uid)
		if user_data.name:
			tg_accs = []
			for i in user_data.telegram_accounts:

				try:
					tg_accs.append(get_string('user_info_list_item_telegram_account').format(tg_id=i.tg_id, tg_acc_name=bot.get_chat(i.tg_id).first_name, login_time=(i.login_time+timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')))
				except:
					pass
			all_devices = [get_string('user_info_list_item_device').format(device=x.name, login_time=(x.login_time+timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')) for x in user_data.devices]
			if len(all_devices) > 0:
				all_devices = '\n 🔹 '.join(all_devices)
			else:
				all_devices = get_string('user_info_list_item_device_not_found')
			info = get_string('user_information').format(name=user_data.name, telegram_accounts='\n 🔹 '.join(tg_accs), devices=all_devices)
			bot.reply_to(m, info, parse_mode='html')
		else:
			bot.reply_to(m, get_string('not_authorized'), parse_mode='html')

	elif text.startswith('/revoke'):
		if m.chat.type == 'private':
			user_data = db.get_user_data(tg_id=uid)
			response = db.revoke_token(user_data.user_id, uid)
			if response['ok']:
				bot.reply_to(m, get_string('privacy_token_revoked').format(name=user_data.name), parse_mode='html')
				for i in response['data']:
					try:
						bot.send_message(i, get_string('privacy_token_revoked').format(name=user_data.name), parse_mode='html')
					except:
						pass
			elif response['desc'] == 'not_dominant':
				bot.reply_to(m, get_string('privacy_not_dominant_account'), parse_mode='html')
			elif response['desc'] == 'acc_not_exist':
				bot.reply_to(m, get_string('privacy_token_not_exist'), parse_mode='html')
			else:
				bot.reply_to(m, get_string('fatal_eror'), parse_mode='html')
		else:
			bot.reply_to(m, get_string('command_restricted_in_group'))
	if uid in owners:
		if text.startswith('notify\n'):
			data = text.replace('notify\n', '', 1).split("\n<->\n")
			if len(data) == 3:
				db.set_new_notification(data[0], data[1], data[2])
				bot.reply_to(m, get_string('added_new_notification').format(title=data[0], data=data[1], notifier=data[2]), parse_mode='html')
			else:
				bot.reply_to(m, get_string('wrong_notification_format'))

		elif text == 'all_notifications':
			data = db.get_all_notifications()
			result = ""
			for i in data:
				result += get_string('notifications_list').format(nid=i.id, title=i.title)
			bot.reply_to(m, result if len(result) > 0 else "Bildirishnomalar yo'q", parse_mode='html')

		elif text.startswith('del_notif: '):
			nid = int(text.replace('del_notif: ', '', 1))
			db.delete_notification(nid)
			bot.reply_to(m, get_string('notification_deleted'))

		elif text == '!stats':
			

# work on callbacks
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	cid=call.message.chat.id
	data = call.data
	if call.message:
		if data.startswith("lgn_"):
			extracted = data.replace("lgn_", "", 1)
			if extracted == "no":
				bot.edit_message_text(chat_id=cid, message_id=call.message.message_id, text=get_string('reg_check_credentials_retry'), parse_mode='html')
			else:
				lgn = extracted.split("|")[0]
				pswd = extracted.split("|")[1]
				db.temp_reg(tg_id=cid, login=lgn, password=pswd)
				keyboard = types.InlineKeyboardMarkup()
				url_button = types.InlineKeyboardButton(text=get_string('deep_linking_login_success_button'), url="http://ukkix.app/login?init={}".format(base64.b64encode(str(cid).encode('utf-8')).decode('utf-8')))
				keyboard.add(url_button)
				bot.edit_message_text(chat_id=cid, message_id=call.message.message_id, text=get_string('reg_click_to_finish'), parse_mode='html', reply_markup=keyboard)
		elif data == 'del':
			bot.delete_message(call.message.message_id)

# Here we'll either use long polling or webhook.
# No matter what we use, let's just change only this part, DO NOT EVER touch other codes.

# I don't trust the long polling. 
# It crashes unexpectedly, you gotta keep awake the polling process in order to 
# maintain the stable connection between two servers (Bot API server and our server)
def do_polling(): #deprecated - DO NOT USE THIS
	try:
		bot.polling(none_stop=True, interval=0)
	except Exception as e:
		logger.log(e)
		sleep(3)
		do_polling()

bot.infinity_polling(timeout=1)