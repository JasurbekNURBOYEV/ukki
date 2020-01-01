from django.db import models

# Create your models here.

class Account(models.Model):
	user_id = models.BigIntegerField(primary_key=True)
	token = models.CharField(max_length=60)
	name = models.CharField(max_length=100)
	login = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	created_time = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=100, default='student')
	freshman_year = models.PositiveSmallIntegerField(default=2018)
	gender = models.NullBooleanField(null=True, default=None)
	token_generated_time = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'accounts'


class Session(models.Model):
	user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
	xsrf_token = models.TextField()
	tuit_lms_session = models.TextField()
	loaded_at = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'sessions'


class Subject(models.Model):
	user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
	unique_id = models.IntegerField()
	part_ids = models.CharField(max_length=50)
	streams = models.CharField(max_length=50)
	subject = models.CharField(max_length=200)
	subject_id = models.IntegerField()
	semester_id = models.PositiveSmallIntegerField(default=1)
	attendance = models.PositiveSmallIntegerField(default=0)
	teachers = models.CharField(max_length=200)
	loaded_at = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'subjects'


class Activity(models.Model):
	user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
	subject_id = models.IntegerField() # it is unique_id of Subject
	teacher = models.CharField(max_length=100)
	task = models.CharField(max_length=500)
	task_file_name = models.CharField(max_length=500)
	deadline = models.CharField(max_length=20)
	max_grade = models.CharField(max_length=5)
	grade = models.CharField(max_length=5)
	is_submitted = models.BooleanField(default=False)
	submitted_file_url = models.CharField(max_length=100)
	submitted_file_name = models.TextField()
	loaded_at = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'activities'


class Device(models.Model):
	user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	device_id = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)
	login_time = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'devices'


class Notification(models.Model):
	title = models.CharField(max_length=500)
	data = models.TextField()
	notifier = models.CharField(max_length=100)
	time = models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table = 'notifications'


class TelegramAccount(models.Model):
	user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
	tg_id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	login_time = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'telegram_accounts'


class Stream(models.Model):
	name = models.CharField(max_length=20, primary_key=True)
	group_link = models.CharField(max_length=30)
	chat_id = models.BigIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	members_count = models.IntegerField(default=1)
	loaded_at = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'streams'


class Status(models.Model):
	tg_id = models.IntegerField(primary_key=True)
	status = models.CharField(max_length=10)
	class Meta:
		db_table = 'statuses'


class Download(models.Model):
	url = models.CharField(max_length=100, primary_key=True)
	file_id = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table = 'downloads'


class User(models.Model):
	tg_id = models.BigIntegerField(primary_key=True)
	reg_time = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'users'


class TemporaryAccount(models.Model):
	tg_id = models.BigIntegerField(primary_key=True)
	login = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	created_time = models.DateTimeField(auto_now_add=True)
	reg_time = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'temporary_accounts'

class Request(models.Model):
	agent = models.TextField()
	path = models.CharField(max_length=255)
	user_id = models.BigIntegerField(null=True)
	ip = models.CharField(max_length=15)
	device_name = models.CharField(max_length=255, null=True)
	device_id = models.CharField(max_length=63, null=True)
	token = models.CharField(max_length=63, null=True)
	created_time = models.DateTimeField(auto_now=True)