from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = "testApp"

urlpatterns = [
    url(r'^taketest/(?P<test_id>[0-9]+)$', views.StartTest.as_view(), name='index'),
    url(r'^QuestionSlide/(?P<test_id>[0-9]+)$', views.QuestionsSlide.as_view(), name='QuestionsSlide'),
    url(r'^complete_test/$', views.CompleteTest.as_view(), name='CompleteTest')
]
