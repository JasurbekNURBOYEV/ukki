# do api stuff here

import requests as r
import json
from models import *
from tools import Logger
from strings import get_string
from LMS import LMS
from datetime import datetime

logger = Logger("api")
#logger.deactivate()

base_url = "http://116.203.202.211:6000/api/"

def get_subjects(login, password, modelify=False):
	method = "getSubjects"
	try:
		data = r.post(base_url+method, json={"username": login, "pswd": password})
	except Exception as e:
		logger.log(e)
		return Subjects([])
	try:
		data = json.loads(data.text)['data']['data']
	except Exception as e:
		logger.log(e)
		data = []
	if modelify:
		data = Subjects(data)
	return data

def login(login, password):
	method = "login"
	try:
		data = json.loads(r.post(base_url+method, json={"username": login, "pswd": password}, timeout=5).text)
		lms = LMS(login, password)
		if lms.check_credentials():
			current_semester = lms.get_current_semester_id()
			current_month = int(datetime.now().strftime("%m"))
			current_year = int(datetime.now().strftime("%Y"))
			if current_month < 9:
				freshman_year = current_year - (current_semester//4 + 1)
			else:
				freshman_year = current_year - (current_semester//4)
			data['freshman_year'] = freshman_year
	except Exception as e:
		raise Exception(e)
		logger.log(e)
		return{'ok': False, 'desc': get_string('reg_fatal_error')}
	# try:
	# 	data = json.loads(data.text)
	# except:
	# 	data = {'ok': False, 'desc': get_string('reg_fatal_error')}
	return data

def create_stream(stream_name):
	if type(stream_name) == list:
		for i in stream_name:
			requests.post('http://127.0.0.1:6000/stream/create_stream', data={'name': i})
	elif type(stream_name) == str:
		requests.post('http://127.0.0.1:6000/stream/create_stream', data={'name': stream_name})
