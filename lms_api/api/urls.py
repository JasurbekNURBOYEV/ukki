from django.urls import path, re_path

from . import views

urlpatterns = [
	re_path('(?i)login', views.login),
	re_path('(?i)getSubjects', views.get_subjects),
	re_path('(?i)getActivities', views.get_activities),
	re_path('(?i)getSemester', views.get_semester),
	re_path('(?i)getSchedule', views.get_schedule),
	re_path('(?i)getFinals', views.get_finals),
	re_path('(?i)getNews', views.get_news),
	re_path('(?i)getAccessForSubjects', views.access_for_subjects),
	re_path('(?i)processRawData', views.process_raw_data),
	re_path('(?i)check', views.check),
	re_path('(?i)test_2', views.test_2),
	re_path('(?i)test_3', views.test_3),
	re_path('(?i)test', views.test)
]