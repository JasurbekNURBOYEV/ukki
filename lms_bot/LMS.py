# LMS bilan ulanish uchun class
import requests
from robobrowser import RoboBrowser
from requests import Session
from random import choice
import json
import xml
import re
import bs4
import random
import test_schedule

class Logging(object):
	"""docstring for Logging"""
	def __init__(self):
		self.arg = 1

	def error(self, err):
		print(err)

logging = Logging()



# here is the method to reformat the reponse
# this makes the result as same as LMS API
# when API is available, we won't have to rewrite client side
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

		
class LMS:

	def __init__(self, username, pswd, proxy=False):
		"""
		login/parol yordamida LMS classidan instance yaratiladi
		:param: username => string: login
		:param: pswd => string: parol
		:param: proxy => bool: proxy ishlatish yoki ishlatmaslikni belgilash [default: False]
		"""
		self.username = username
		self.pswd = pswd
		self.session = Session()
		self.proxy = proxy
		agent = choice(json.loads(open('all_agents.txt', 'r').read())['agents'])
		if self.proxy:
			random_proxy = random.choice(self.get_proxies(False))
			self.session.proxies = {'https': 'https://{ip}:{port}'.format(ip=random_proxy['ip'], port=random_proxy['port'])}
			self.browser = RoboBrowser(user_agent=agent, session=self.session)
		else:
			self.browser = RoboBrowser(user_agent=agent)


	def load_session(self, session):
		self.session = session
	
	def clear_text(self, text):
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
	
	def is_valid(self, page):
		"""
		login jarayoni muvaffaqiyatli kechganini aniqlash metodi
		:param: page => string: sahifaning html kodi
		:return: bool
		"""
		if 'exampleInputEmail1' in str(page):
			return False
		else:
			return True

	def get_proxies(self, fresh=False):
		if fresh:
			#try:
				url = 'https://www.sslproxies.org/'
				response = requests.get(url)
				parser = bs4.BeautifulSoup(response.text)
				tbody = parser.find('tbody')
				data = []
				for row in tbody.findAll('tr'):
					cols = row.findAll('td')
					data.append({'ip': cols[0].text, 'port': cols[1].text})
				with open('proxies.json', 'w') as f:
					f.write(json.dumps(data))
				return data
			#except Exception as e:
			#	print(str(e))
			#	return False
		else:
			try:
				return json.loads(open('proxies.json', 'r').read())
			except Exception as e:
				logging.error(str(e))
				return False

	def check_credentials(self):
		"""
		login/parol to'g'riligini tekshirish metodi
		:return:
			- student_name => string: login/parol to'g'iri bo'lganda
			- bool: login/parol noto'g'iri bo'lganda [False]
		"""
		login_url = 'https://lms.tuit.uz/auth/login'
		self.browser.open(login_url)
		form = self.browser.get_form(action=login_url)
		form['login'].value = self.username
		form['password'].value = self.pswd
		self.browser.submit_form(form)
		page = self.browser.parsed
		if self.is_valid(page):
			parser = bs4.BeautifulSoup(str(page))
			name = parser.find('ul', 'dropdown-menu dropdown-content').findAll('li')[0].text
			return name.replace('\n', '').strip()
		else:
			return False

	def get_current_semester_id(self):
		"""
		ayni paytdagi faol semester id raqamini aniqlaydi
		agar ayni paytda N-semester bo'la turib, shu semesterda birorta fan mavjud bo'lmasa,
		N-1 natija sifatida qaytariladi
		"""
		url = "https://lms.tuit.uz/student/my-courses"
		self.browser.open(url)
		page = self.browser.parsed
		parser = bs4.BeautifulSoup(str(page))
		block = parser.find("select", {'name': 'semester_id'})
		semester_ids = block.findAll('option')
		semester_id = len(semester_ids)
		basic_url = 'https://lms.tuit.uz/student/my-courses/data?semester_id={}'
		try:
			data = self.browser.open(basic_url.format(semester_id))
			count = json.loads(self.clear_text(str(self.browser.parsed)))['recordsTotal']
		except Exception as e:
			logging.error(str(e))
			count = 0
		if count == 0:
			semester_id -= 1
		return semester_id
	
	def enable_proxy(self, proxies=None):
		self.proxy = proxies if proxies != None else self.get_proxies()
		self.proxy = proxy
		agent = choice(json.loads(open('all_agents.txt', 'r').read())['agents'])
		if self.proxy:
			random_proxy = random.choice(self.get_proxies())
			self.session.proxies = {'https': 'https://{ip}:{port}'.format(ip=random_proxy['ip'], port=random_proxy['port'])}
			self.browser = RoboBrowser(user_agent=agent, session=self.session)
		else:
			self.browser = RoboBrowser(user_agent=agent)
			
	def chameleon(self):
		agent = choice(json.loads(open('all_agents.txt', 'r').read())['agents'])
		if self.proxy:
			random_proxy = random.choice(self.get_proxies())
			self.session.proxies = {'https': 'https://{ip}:{port}'.format(ip=random_proxy['ip'], port=random_proxy['port'])}
			self.browser = RoboBrowser(user_agent=agent, session=self.session)
		else:
			self.browser = RoboBrowser(user_agent=agent)

	
	def get_finals(self):
		basic_url = 'https://lms.tuit.uz/student/finals/data?semester_id=3'
		try:
			data = []
			c = 3
			valid = True
			while valid:
				self.browser.open(basic_url)
				page = self.browser.parsed
				single = json.loads(self.clear_text(str(page)))
				return {'ok': True, 'data': single}
				if single['recordsTotal'] != 0:
					data.append({c: single})
				else:
					valid = False
				c += 1
			data = {'ok': True, 'data': data}
		except Exception as e:
			data = {'ok': False, 'data': None}
		return data

	def get_semester(self):
		try:
			self.browser.open('https://lms.tuit.uz/student/study-plan')
			parser = bs4.BeautifulSoup(str(self.browser.parsed))
			rows = parser.findAll('tr')
			if len(rows) == 0:
				return {'ok': False, 'data': None}
			data = []
			semester = []
			semester_count = 1
			for i in rows[1:]:
				cols = [x.text.replace('\n', '') for x in i.findAll('td')]
				if len(cols) > 1:
					semester.append({'subject': cols[0], 'credit': cols[1], 'grade': cols[2].replace(' ', '')})
				elif i.find('td', 'bg-info'):
					data.append({'semester': semester_count, 'data': semester})
					semester_count += 1
					semester = []
			if len(semester) > 0:
				data.append({'semester': semester_count, 'data': semester})
			data = {'ok': True, 'data': data}
		except Exception as e:
			logging.error(str(e))
			data = {'ok': False, 'data': None}
		return data
		
	def get_schedule(self):
		try:
			self.browser.open('https://lms.tuit.uz/student/schedule')
			parser = bs4.BeautifulSoup(str(self.browser.parsed))
			tbody = parser.find('tbody')
			if tbody == None:
				print("Tbody is None")
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
					print("for loop DAY: " + str(day))
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
			data = {'ok': True, 'data': schedule_reformatter(data)}
		except Exception as e:
			logging.error(str(e))
			data = {'ok': False, 'data': e}
		return data

	def get_subjects(self, semester_id=1):
		semester_id = self.get_current_semester_id()
		basic_url = 'https://lms.tuit.uz/student/my-courses/data?semester_id={}'
		try:
			data = self.browser.open(basic_url.format(semester_id))
			data = {'ok': True, 'data': json.loads(self.clear_text(str(self.browser.parsed)))}
		except Exception as e:
			logging.error(str(e))
			data = {'ok': False, 'data': str(e)}
		return data
		
	def get_activities(self, subject_id):
		try:
			self.browser.open('https://lms.tuit.uz/student/my-courses/show/{}'.format(subject_id))
			parser = bs4.BeautifulSoup(str(self.browser.parsed))
			table = parser.find('div', 'table-responsive')
			if not table:
				logging.error('GET_ACTIVITIES: Table not found')
				return {'ok': False, 'data': None}
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
					uploaded_file_name = self.clear_text(submitted_work.find('a').text)
				data.append({
					'teacher': self.clear_text(teacher),
					'task': self.clear_text(task),
					'task_file_name': self.clear_text(task_file_name),
					'task_file_url': task_file_url,
					'deadline': self.clear_text(task_deadline),
					'max_grade': self.clear_text(max_grade),
					'grade': self.clear_text(acheived_grade),
					'is_submitted': submitted,
					'submitted_file_url': uploaded_file,
					'submitted_file_name': uploaded_file_name
				})
			data = {'ok': True, 'data': data}
		except Exception as e:
			logging.error(str(e))
			data = {'ok': False, 'data': None}
		return data

	def test(self, url):
		try:
			self.browser.open(url)
		except:
			pass