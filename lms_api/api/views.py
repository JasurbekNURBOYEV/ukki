from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from LMS import LMS
import time
import database
from random import choice
from tools import is_expired, calculate_current_semester, clear_text, schedule_reformatter, shifr
import telebot
from strings import get_string
import requests as r
import base64
import test_schedule
import bs4

method = 'POST'
db = database.DataBase()
token = "BOT_TOKEN"
bot = telebot.TeleBot(token)


class HandleCredentials:
	def get_ip(self, request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip


	def __init__(self, request):
		if request.method == 'GET':
			self.username = request.GET.get('username', None)
			self.pswd = request.GET.get('pswd', None)
			self.token = request.GET.get('token', None)
			self.subject_id = request.GET.get('subject_id', None)
		elif request.method == 'POST':
			if request.body:
				keys = request.POST
			else: 
				keys = dict()
			self.name = None
			self.user_id = None
			self.tg_accs = []
			self.app = request.META.get('HTTP_USER_AGENT', None)
			self.device_name = request.POST.get('device_name', None)
			self.device_id = request.POST.get('device_id', None)
			self.username = keys.get('username', None)
			self.pswd = keys.get('pswd', None)
			self.token = request.META.get('HTTP_TOKEN', None)
			if self.token:
				credentials = db.get_user_credentials(token=self.token)
				if credentials:
					self.name = credentials['name']
					self.username = credentials['login']
					self.pswd = credentials['password']
					self.tg_accs = credentials['telegram_accounts']
				data = db.get_user_data(token=self.token)
				if data != None:
					self.user_id = data.user_id
			if not self.username and not self.pswd:
				try:
					keys = json.loads(request.body)
					self.username = keys.get('username', None)
					self.pswd = keys.get('pswd', None)
				except:
					pass
			self.subject_id = keys.get('subject_id', None)
			db.store_request(agent=self.app, path=request.path, user_id=self.user_id, 
				ip=self.get_ip(request), device_name=self.device_name, device_id=self.device_id,
				token=self.token)


def get_credentials(request):
	if request.method == 'GET':
		return request.GET.get('token', None)
	elif request.method == 'POST':
		return request.META.get('Token', None)


@csrf_exempt
def login(request):
	if request.method == method:
		credentials = HandleCredentials(request)
		if credentials.token:
			try:
				user_data = db.get_user_credentials(credentials.token)
				if user_data:
					student = user_data['name']
					user_id = user_data['user_id']
					db.register_device(device_id=credentials.device_id, device_name=credentials.device_name, user_id=user_id)
					tg_accs = credentials.tg_accs
					for acc in tg_accs:
						try:
							bot.send_message(acc.tg_id, get_string('new_login').format(device=credentials.device_name, app=credentials.app), parse_mode='html')
						except:
							pass
			except Exception as e:
				print(f"Error in login: {e}")
			return JsonResponse({'ok': True})
		else:
			return JsonResponse({'ok': False})


@csrf_exempt
def get_subjects(request):
	if request.method == method:
		credentials = HandleCredentials(request)
		lms = LMS(credentials.username, credentials.pswd)
		if lms.check_credentials():
			subjects = lms.get_subjects()
			return JsonResponse(subjects)
		else:
			return JsonResponse({'ok': False, 'desc': 'Authentication error'})


@csrf_exempt
def get_activities(request):
	if request.method == method:
		credentials = HandleCredentials(request)
		subject_id = credentials.subject_id
		lms = LMS(credentials.username, credentials.pswd)
		if lms.check_credentials() and subject_id:
			return JsonResponse(lms.get_activities(subject_id))
		else:
			return JsonResponse({'ok': False, 'desc': 'Authentication error'})


@csrf_exempt
def get_semester(request):
	if request.method == method:
		credentials = HandleCredentials(request)
		lms = LMS(credentials.username, credentials.pswd)
		if lms.check_credentials():
			return JsonResponse(lms.get_semester())
		else:
			return JsonResponse({'ok': False, 'desc': 'Authentication error'})


@csrf_exempt
def get_schedule(request):
	if request.method == method:
		credentials = HandleCredentials(request)
		lms = LMS(credentials.username, credentials.pswd)
		if lms.check_credentials():
			response = lms.get_schedule()
			return JsonResponse(response)
		else:
			return JsonResponse({'ok': False, 'desc': 'Authentication error'})


@csrf_exempt
def get_finals(request):
	if request.method == method:
		credentials = HandleCredentials(request)
		lms = LMS(credentials.username, credentials.pswd)
		if lms.check_credentials():
			return JsonResponse(lms.get_finals())
		else:
			return JsonResponse({'ok': False, 'desc': 'Authentication error'})


@csrf_exempt
def get_news(request):
	if request.method == method:
		credentials = HandleCredentials(request)
		lms = LMS(credentials.username, credentials.pswd)
		if credentials.username and credentials.pswd:
			news = db.get_news()
			return JsonResponse({'ok': True, 'data': news})
		else:
			return JsonResponse({'ok': False})


def get_session(token):
	return None
	data = db.get_session(token)
	if data != None:
		if data['session'] != None:
			if not is_expired(data['session'].loaded_at):
				return {'xsrf_token': data['session'].xsrf_token, 'tuit_lms_session': data['session'].tuit_lms_session}
		lms = LMS(data['account'].login, data['account'].password)
		if lms.check_credentials():
			new_session = lms.browser.session.cookies
			print(new_session)
			db.store_session(data['account'].token,
				xsrf_token=new_session['XSRF-TOKEN'],
				tuit_lms_session=new_session['tuit_lms_session'])
			return {'xsrf_token': new_session['XSRF-TOKEN'], 'tuit_lms_session': new_session['tuit_lms_session']}
	return None


@csrf_exempt
def access_for_subjects(request):
	return JsonResponse({'ok': False})
	credentials = HandleCredentials(request)
	if credentials.token != None:
		session = get_session(credentials.token)
		account_info = db.get_user_data(token=credentials.token)
		if account_info.freshman_year == None or session == None:
			return JsonResponse({'ok': False})
		semester = calculate_current_semester(account_info.freshman_year)
		agent = choice(json.loads(open('all_agents.txt', 'r').read())['agents'])
		urls = '{};my-courses/show/'.format(semester)
		return JsonResponse({'ok': True, 'agent': agent, 'urls': urls, 'access': '{};{}'.format(session['xsrf_token'], session['tuit_lms_session'])})
	else:
		return JsonResponse({'ok': False})


def parse_activities(html):
	parser = bs4.BeautifulSoup(html, features="html.parser")
	table = parser.find('div', 'table-responsive')
	if not table:
		return None
	tbody = table.find('tbody')
	data = []
	for row in tbody.findAll('tr'):
		cols = row.findAll('td')
		teacher = cols[0].text
		task = cols[1].find(text=True)
		task_file_name = cols[1].find('a').text
		task_file_url = cols[1].find('a')
		if task_file_url:
			task_file_url = task_file_url['href']
		else:
			task_file_url = None
		task_deadline = cols[2].text
		task_grade = [x.text for x in cols[3].findAll('button')]
		max_grade = task_grade[1]
		acheived_grade = task_grade[0]
		submitted_work = cols[4]
		submitted = False
		uploaded_file = None
		uploaded_file_name = None
		if submitted_work.find('i', 'fa fa-download'):
			submitted = True
			uploaded_file = submitted_work.find('a')['href']
			if len(str(uploaded_file)) < 20:
				uploaded_file = None
			uploaded_file_name = clear_text(submitted_work.find('a').text)
		data.append({
			'teacher': clear_text(teacher),
			'task': clear_text(task),
			'task_file_name': clear_text(task_file_name),
			'task_file_url': task_file_url,
			'deadline': clear_text(task_deadline),
			'max_grade': clear_text(max_grade),
			'grade': clear_text(acheived_grade),
			'is_submitted': submitted,
			'submitted_file_url': uploaded_file,
			'submitted_file_name': uploaded_file_name
		})
	return data


def parse_schedule(html):
	parser = bs4.BeautifulSoup(html, features="html.parser")
	tbody = parser.find('tbody')
	if tbody == None:
		return {'ok': False, 'data': None}
	rows = tbody.findAll('tr')
	data = []
	days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
	for i in rows:
		cols = i.findAll('td')
		duration = cols[0].text
		week = []
		current_day = 0
		for day in cols[1:]:
			if len(day.text) > 1:
				subject = day.find(text=True)
				code = day.find('span')
				building = day.find('small').text.split('-')[0]
				room = day.find('small').text.split('-')[1]
				week.append({'data': {'subject': subject.replace('  ', '').replace('\n', ''), 'identificator': code.text, 'room': room, 'building': building}, 'day': days[current_day]})
			else:
				week.append({'day': days[current_day], 'data': None})
			current_day += 1
		if week:
			data.append({'time': duration, 'week': week})
	return {'ok': True, 'data': schedule_reformatter(data)}


@csrf_exempt
def process_raw_data(request):
	data = request.POST.get('data', None)
	data = json.loads(data)
	if data != None:
		schedule = parse_schedule(data['schedule'])
		final_result = []
		for activity in data['data']:
			parsed = parse_activities(activity['data'])
			
			final_result.append({'key': activity['key'], 'data': parsed})
	return JsonResponse({'ok': True, 'data': final_result, 'schedule': schedule})


@csrf_exempt
def check(request):
	credentials = HandleCredentials(request)
	if credentials.token != None:
		user_data = db.get_user_credentials(credentials.token)
		if user_data != None:
			return JsonResponse({"ok": True})
	return JsonResponse({"ok": False})


@csrf_exempt
def test(request):
	credentials = HandleCredentials(request)
	if credentials.token != None:
		keys = request.POST.get('data').split('<>')
		k = int(keys[0])
		n = int(keys[1])
		print(f"KEYS: k={k} n={n}")
		data = db.get_user_credentials(credentials.token)
		if data != None:
			account_info = db.get_user_data(token=credentials.token)
			if account_info.freshman_year == None:
				return JsonResponse({'ok': False})
			semester = calculate_current_semester(account_info.freshman_year)
			agent = choice(json.loads(open('all_agents.txt', 'r').read())['agents'])
			print(f'LGN: {data["login"]} PSWD: {data["password"]} AGENT: {agent}')
			return JsonResponse({'ok': True, 'sid': semester, 'encrypted': shifr('{}<>{}'.format(data['login'], data['password']), k, n)+'<>{}'.format(agent) })
	return JsonResponse({'ok': False})


@csrf_exempt
def test_2(request):
	data = request.POST.get('data')
	print(f"ENCRYPTED: {data}")
	keys = request.POST.get("keys").split("<>")
	k, n = int(keys[0]), int(keys[1])
	decrypted = base64.b64decode(data).decode("utf-8")
	print(f"DECRYPTED: {decrypted}")
	temp_acc = db.get_temp_acc(tg_id=int(decrypted))
	if temp_acc != None:
		agent = choice(json.loads(open('all_agents.txt', 'r').read())['agents'])
		return JsonResponse({'ok': True, 'encrypted': shifr('{}<>{}'.format(temp_acc['login'], temp_acc['password']), k, n)+'<>{}'.format(agent)})
	else:
		return JsonResponse({'ok': False})


@csrf_exempt
def test_3(request):
	credentials = HandleCredentials(request)
	data = request.POST.get('data')
	decrypted = base64.b64decode(data).decode("utf-8")
	tg_id = int(decrypted.split('<>')[0])
	name = decrypted.split('<>')[1]
	temp_acc = db.get_temp_acc(tg_id=tg_id, delete=True)
	if temp_acc != None:
		token = db.register(tg_id=tg_id, login=temp_acc['login'], password=temp_acc['password'], name=name)[1]
		user_data = db.get_user_credentials(token)
		if user_data:
			student = user_data['name']
			user_id = user_data['user_id']
			db.register_device(device_id=credentials.device_id, device_name=credentials.device_name, user_id=user_id)
			tg_accs = credentials.tg_accs
			for acc in tg_accs:
				try:
					bot.send_message(acc.tg_id, get_string('new_login').format(device=credentials.device_name, app=credentials.app), parse_mode='html')
				except:
					pass
		return JsonResponse({'ok': True, 'encrypted': token})
	else:
		return JsonResponse({'ok': False})
