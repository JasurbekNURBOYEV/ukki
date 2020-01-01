# Huge models are born right here
# Don't play with them, call, process and save.


class Subject:
	"""docstring for Subject"""
	def __init__(self, id=None, part_ids=None, streams=None, subject=None, subject_id=None, semester_id=None, attendance=None, teachers=None):
		self.id = id
		self.part_ids = part_ids
		self.streams = streams
		self.subject = subject
		self.subject_id = subject_id
		self.semester_id = semester_id
		self.attendance = attendance
		self.teachers = teachers


class Subjects:
	def __init__(self, json_data):
		subjects = []
		for i in json_data:
			subjects.append(Subject(
				i.get("id", None),
				i.get("part_ids", None),
				i.get("streams", None),
				i.get("subject", None),
				i.get("subject_id", None),
				i.get("semester_id", None),
				i.get("attendance", 0),
				i.get("teachers", None)))
		self.subjects = subjects


class AccountInfo:
	def __init__(self, token=None, name=None, telegram_accounts=None, devices=None):
		self.token = token
		self.name = name
		self.telegram_accounts = telegram_accounts if telegram_accounts else []
		self.devices = devices if devices else []


class Device:
	def __init__(self, device_name=None, device_id=None, login_time=None):
		self.device_name = device_name
		self.device_id = device_id
		self.login_time = login_time


class TelegramAccount:
	def __init__(self, tg_id=None, name=None, login_time=None):
		self.tg_id = tg_id
		self.name = name
		self.login_time = login_time

		