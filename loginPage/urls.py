from django.conf.urls import url
from django.contrib import admin
from . import views
app_name = "login_App"


urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='index'),
    url(r'^logout/$',  views.logoutview, name='logout'),
]
