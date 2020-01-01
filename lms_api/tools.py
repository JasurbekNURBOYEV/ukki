# tools
from uuid import uuid4
import random
import time
from datetime import datetime, timedelta, timezone
import re


class Logger:
	def __init__(self, tag="mylog"):
		self.active = True
		self.tag = tag

	def log(self, *text):
		if self.active:
			print("{}: {}".format(self.tag, *text))

	def deactivate(self):
		self.active = False

class Generator:
	def __init__(self):
		pass

	def generate_token(self):
		return "{prefix}:{uuid}".format(prefix=random.randint(10**5, 10**8), uuid=uuid4().hex)

	def generate_uid(self):
		return int(time.time()/random.randint(3, 13))*7

	def generate_comfirmation_code(self):
		return random.randint(100000, 999999)

def unix_to_date(timestamp):
	return datetime.fromtimestamp(timestamp//1000 + 3*60*60).strftime('%Y-%m-%d %H:%M:%S')

def is_expired(stored_date, delta=60): # delta is in minutes
	print(stored_date.strftime("%H:%M"))
	print(datetime.now(timezone.utc).strftime("%H:%M"))
	return (stored_date  + timedelta(minutes=delta)) < datetime.now(timezone.utc)

def calculate_current_semester(freshman_year):
	current_date = datetime.now(timezone.utc)
	current_year = int(current_date.strftime('%Y'))
	current_month = int(current_date.strftime('%m'))
	if 12 >= current_month >= 9:
		semester = (current_year - freshman_year)*4 + 1
	else:
		semester = (current_year - freshman_year)*2 + 1
	return semester

def clear_text(text):
	"""
	matnni ortiqcha belgilardan tozalash uchun metod
	kiruvchi axborot string bo'lgandagina u qayta ishlanadi
	:param: text => string
	:return: string
	"""
	if type(text) == int or type(text) == float:
		return text
	else:
		text = str(text)
		tag_pattern = "</*[a-z]+>"
		for tag in re.findall(tag_pattern, text):
			text = text.replace(tag, '')
		return text.replace('\n', '').strip()

def schedule_reformatter(data):
	result = []
	times = {}
	times_counter = 1
	for i in range(len(data)):
		times[str(i+1)] = data[i]['time']

	result.append(times)
	for day in range(6):
		single = {}
		for pair in range(len(data)):
			if data[pair]['week'][day]['data'] != None:
				single[str(pair+1)] = [data[pair]['week'][day]['data']]
			else:
				single[str(pair+1)] = None
		result.append(single)
	return result

def shifr(s, k, n):
	st=""
	for i in range(len(str(s))):
		a=ord(s[i])
		x=k
		res=1
		while(x!=0):
			res=(res*a)%n
			x=x-1
		st+=str(res)+'.'
	st=st[:-1]
	return st  