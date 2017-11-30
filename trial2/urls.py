from django.conf.urls import url,include
from django.contrib import admin
from trial2 import views

urlpatterns=[
	url(r'^$',views.homeview.as_view()),
	url(r'index2/$',views.homeview.as_view()),
]
