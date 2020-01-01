# tools
from uuid import uuid4
import random
import time
from datetime import datetime, timedelta


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
		return "{prefix}:{uuid}".format(prefix=random.randint(10000000, 99999999), uuid=uuid4().hex)

	def generate_uid(self):
		return int(time.time()/random.randint(3, 13))*7

	def generate_comfirmation_code(self):
		return random.randint(100000, 999999)

def unix_to_date(timestamp):
	return datetime.fromtimestamp(timestamp//1000 + 3*60*60).strftime('%Y-%m-%d %H:%M:%S')

def is_expired(stored_date, delta=60): # delta is in minutes
	return (stored_date  + timedelta(minutes=delta)) > datetime.now()

def shifr(  s,  k, n):
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