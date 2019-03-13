from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'dashboard'

urlpatterns = [
    url(r'^homepage/$', login_required(views.HomePageView.as_view()), name='homepage'),
    url(r'^mytests/$', login_required(views.MyTestView.as_view()), name='mytests'),
    url(r'^testquestions/(?P<test_id>[0-9]+)/$', login_required(views.TestQuestionsView.as_view()), name='testquestions'),
    url(r'^bookmark/(?P<test_id>[0-9]+)/$', login_required(views.AddBookmarkView.as_view()), name='addbookmark'),
    url(r'^bookmark/remove/(?P<question_id>[0-9]+)/$', login_required(views.RemoveBookmarkView.as_view()), name='removebookmark'),
    url(r'^bookmark/list/$', login_required(views.BookMarkListView.as_view()), name='bookmarklist'),
    url(r'^profile/$', login_required(views.ProfileView.as_view()), name='profile'),
    url(r'^custom_admin/$', login_required(views.CustomAdmin.as_view()), name='CustomAdmin'),
    url(r'^$', views.AboutUs.as_view(), name='about_us'),
]
