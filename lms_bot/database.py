# database
from db import models
from time import time
from tools import Logger, Generator
from strings import get_string

generator = Generator()

def get_time():
	return int(time()*1000)

class DataBase:
	
	def __init__(self):
		pass

	def executor(self, method, *args, **kwargs):
		try:
			data = method(*args, **kwargs)
		except Exception as e:
			print("ERROR in DB: {}".format(e))
			data = None
		return data

	def get_user_credentials(self, token):
		acc_info = self.executor(models.Account.objects.get, token=token)
		if acc_info != None:
			tg_accs = self.executor(models.TelegramAccount.objects.filter, user_id=acc_info.user_id)
			data = {
					'user_id': acc_info.user_id, 
					'login': acc_info.login, 
					'password': acc_info.password,
					'telegram_accounts': list(tg_accs) if len(tg_accs) != 0 else []
					}
		else:
			data = None
		return data

	def register_device(self, user_id, device_id, device_name):
		existing_device = self.executor(models.Device.objects.get, device_id=device_id)
		if existing_device != None:
			existing_device.user_id = user_id
			existing_device.save()
		else:
			self.executor(
							models.Device.objects.create, 
							device_id=device_id,
							device_name=device_name,
							user_id=user_id
						)

	def get_news(self):
		news = self.executor(models.Notification.objects.all)
		if news != None and len(news) != 0:
			return [{'title': i['title'], 'data': i['data'], 'notifier': i['notifier'], 'time': get_time(), 'id': str(i['id'])} for i in news]
		return []

	def set_status(self, tg_id, status):
		existing_status = self.executor(models.Status.objects.get, tg_id=tg_id)
		if existing_status != None:
			existing_status.status = status
			existing_status.save()
		else:
			models.Status.objects.create(tg_id=tg_id, status=status)

	def get_status(self, tg_id):
		existing_status = self.executor(models.Status.objects.get, tg_id=tg_id)
		if existing_status != None:
			return existing_status.status
		else:
			return None

	def check_if_token_exists(self, token):
		existing_token = self.executor(models.Account.objects.get, token=token)
		if existing_token != None:
			return True
		else:
			return False

	def check_if_uid_exists(self, user_id):
		existing_token = self.executor(models.Account.objects.get, user_id=user_id)
		if existing_token != None:
			return True
		else:
			return False

	def generate_unique_token(self):
		new_token = generator.generate_token()
		while self.check_if_token_exists(new_token):
			new_token = generator.generate_token()
		return new_token

	def generate_unique_user_id(self):
		new_user_id = generator.generate_uid()
		while self.check_if_uid_exists(new_user_id):
			new_user_id = generator.generate_uid()
		return new_user_id

	def terminate_old_sessions(self, user_id, tg_id):
		existing_devices = self.executor(models.Device.objects.filter, user_id=user_id)
		existing_tg_accs = self.executor(models.TelegramAccount.objects.filter, user_id=user_id)
		terminated_tg_accs = []
		if existing_devices != None:
			for device in existing_devices:
				device.delete()
		if existing_tg_accs != None:
			for tg_acc in existing_tg_accs:
				if tg_acc.tg_id != tg_id:
					terminated_tg_accs.append(tg_acc.tg_id)
					tg_acc.delete()
		return terminated_tg_accs

	def temp_reg(self, login, password, tg_id):
		existing_temp_acc = self.executor(models.TemporaryAccount.objects.get, tg_id=tg_id)
		if existing_temp_acc == None:
			models.TemporaryAccount.objects.create(login=login, password=password, tg_id=tg_id)
		else:
			existing_temp_acc.login = login
			existing_temp_acc.password = password
			existing_temp_acc.save()

	def register(self, tg_id, freshman_year=2018, name=None, login=None, password=None):
		terminated_tg_accs = []
		if login != None:
			login = login.lower()
		existing_tg_acc = self.executor(models.User.objects.get, tg_id=tg_id)
		if existing_tg_acc == None:
			models.User.objects.create(tg_id=tg_id)
		if login and password and name:
			gender = not name.split()[0].endswith('a')
			existing_account = self.executor(models.Account.objects.get, login=login)
			if existing_account != None:
				user_id = existing_account.user_id
				if existing_account.password != password:
					#print("Editing existing acc: old_pswd={} new_pswd={}".format(existing_account.password, password))
					existing_account.password = password
					new_token = self.generate_unique_token()
					existing_account.token = new_token
					existing_account.save()
					terminated_tg_accs = self.terminate_old_sessions(existing_account.user_id, tg_id)
			else:
				new_token = self.generate_unique_token()
				new_user_id = self.generate_unique_user_id()
				user_id = new_user_id
				models.Account.objects.create(
					user_id=new_user_id,
					name=name,
					token=new_token,
					login=login,
					password=password,
					gender=gender
					)
			existing_tg_acc = self.executor(models.TelegramAccount.objects.get, tg_id=tg_id)
			if existing_tg_acc != None:
				existing_tg_acc.name = name
				existing_tg_acc.user_id = self.executor(models.Account.objects.get, user_id=user_id)
				existing_tg_acc.save()
			else:
				print(f"TG_ID: {tg_id}\nUID: {user_id}\nNAME: {name}")
				models.TelegramAccount.objects.create(
					tg_id=tg_id,
					user_id=self.executor(models.Account.objects.get, user_id=user_id),
					name=name
					)
		return terminated_tg_accs

	def revoke_token(self, user_id, tg_id):
		response = {'ok': True}
		existing_account = self.executor(models.Account.objects.get, user_id=user_id)
		if existing_account != None:
			all_tg_accs = self.executor(models.TelegramAccount.objects.filter, user_id=existing_account).order_by('login_time')
			if all_tg_accs[0].tg_id != tg_id:
				response['ok'] = False
				response['desc'] = 'not_dominant'
				return response
			existing_account.token = self.generate_unique_token()
			existing_account.save()
			terminated_sessions = self.terminate_old_sessions(user_id, tg_id)
			response['data'] = terminated_sessions
			return response
		else:
			response['ok'] = False
			response['desc'] = 'acc_not_exist'
			return response

	def get_user_data(self, token=None, tg_id=None, user_id=None):
		name = None
		if token:
			data = self.executor(models.Account.objects.get, token=token)
			if data != None:
				user_id = data.user_id
				name = data.name
		elif tg_id:
			data = self.executor(models.TelegramAccount.objects.get, tg_id=tg_id)
			if data != None:
				user_id = data.user_id
				name = data.name

		if type(user_id) == int:
				user_id = user_id
		elif user_id != None:
			user_id = user_id.user_id

		if token == None and user_id != None:
			
			data = self.executor(models.Account.objects.get, user_id=user_id)
			if data != None:
				name = data.name
				token = data.token

		class AccountInfo:
				def __init__(self, token, name, telegram_accounts, devices):
					self.token = token
					self.name = name
					self.telegram_accounts = telegram_accounts
					self.user_id = user_id
					self.devices = devices
					if data != None: self.freshman_year = data.freshman_year

		if user_id != None:
			devices = self.executor(models.Device.objects.filter, user_id=user_id)
			tg_accs = self.executor(models.TelegramAccount.objects.filter, user_id=user_id)
			devices = list(devices) if devices != None and len(devices) != 0 else []
			tg_accs = list(tg_accs) if tg_accs != None and len(tg_accs) != 0 else []
		else:
			devices = []
			tg_accs = []
		return AccountInfo(token=token, name=name, telegram_accounts=tg_accs, devices=devices)

	def store_subjects(self, subjects, tg_id=None, user_id=None):
		if tg_id:
			existing_tg_acc = self.executor(models.TelegramAccount.objects.get, tg_id=tg_id)
			if existing_tg_acc != None:
				user_id = existing_tg_acc.user_id
			else:
				return False
		existing_subjects = self.executor(models.Subject.objects.filter, user_id=user_id)
		if existing_subjects != None and len(existing_subjects) > 0:
			for subject in existing_subjects:
				subject.delete()
		for subject in subjects.subjects:
			models.Subject.objects.create(
				user_id=user_id,
				unique_id=subject.id,
				part_ids=subject.part_ids,
				streams=subject.streams,
				subject=subject.subject,
				subject_id=subject.subject_id,
				semester_id=subject.semester_id,
				attendance=int(subject.attendance),
				teachers=subject.teachers
				)

	def get_user_name(self, tg_id):
		data = self.executor(models.TelegramAccount.objects.get, tg_id=tg_id)
		if data != None:
			return data.name
		return None

	def is_logged(self, tg_id):
		data = self.executor(models.TelegramAccount.objects.get, tg_id=tg_id)
		if data != None:
			return data.user_id
		return False

	def get_friends(self, user_id):
		subjects = self.executor(models.Subject.objects.filter, user_id=user_id)
		data = {'all_friends': {}}
		friends = {user_id.user_id, }
		if len(subjects) > 0:
			for subject in subjects:
				for stream in subject.streams.split('###'):
					friends_for_this_stream = self.executor(
						models.Subject.objects.filter, 
						streams__contains=stream)
					data[stream] = [x.user_id.user_id for x in friends_for_this_stream if x.user_id.user_id != user_id.user_id]
					
					for i in data[stream]:
						friends.add(i)
		for friend in friends:
			friend_name = self.executor(models.TelegramAccount.objects.get, user_id=friend)
			if friend_name != None:
				data['all_friends'][friend] = friend_name.name
			else:
				logged_out_name = self.executor(models.Account.objects.get, user_id=friend)
				if logged_out_name != None:
					data['all_friends'][friend] = f'{get_string("friends_unknown_key")}{logged_out_name.name}'
		return data

	def set_new_notification(self, title, data, notifier):
		self.executor(models.Notification.objects.create(
			title=title,
			data=data,
			notifier=notifier
			))

	def delete_notification(self, nid):
		existing_notification = self.executor(models.Notification.objects.get, id=nid)
		if existing_notification != None:
			existing_notification.delete()

	def get_all_notifications(self):
		data = self.executor(models.Notification.objects.all)
		if len(data) > 0:
			return list(data)
		return []

	def store_tg_file(self, url, file_id):
		self.executor(models.Download.objects.create, url=url, file_id=file_id)

	def get_tg_file(self, url):
		existing_file = self.executor(models.Download.objects.get, url=url)
		if existing_file:
			return existing_file.file_id
		return None

	def set_session(self, user_id, xsrf_token, tuit_lms_session):
		self.executor(models.Session.objects.create, user_id=user_id, xsrf_token=xsrf_token, tuit_lms_session=tuit_lms_session)

	def get_session(self, user_id):
		return self.executor(models.Session.objects.get, user_id=user_id)

	def is_new_stream(self, stream):
		existing_stream = self.executor(models.Stream.objects.get, name=stream)
		if existing_stream:
			return False
		return True


	def create_stream(self, stream, joinchat, chat_id):
		self.executor(models.Stream.objects.create, 
			name=stream, 
			group_link=joinchat,
			chat_id=chat_id)
	
	def get_stream_chat_id(self, name):
		existing_stream = self.executor(models.Stream.objects.get, name=name)
		if existing_stream != None:
			return existing_stream.chat_id
		return None

	def set_stream_member_count(self, chat_id, members_count):
		existing_stream = self.executor(models.Stream.objects.get, chat_id=chat_id)
		if existing_stream != None:
			existing_stream.members_count = members_count
			existing_stream.save()

	def increment_stream_members_count(self, name):
		existing_stream = self.executor(models.Stream.objects.get, name=name)
		if existing_stream != None:
			existing_stream.members_count += 1
			existing_stream.save()

	def decrement_stream_members_count(self, name):
		existing_stream = self.executor(models.Stream.objects.get, name=name)
		if existing_stream != None:
			existing_stream.members_count -= 1
			existing_stream.save()