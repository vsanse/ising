from django.conf.urls import url,include
from django.contrib import admin
from . import views
app_name='music'
urlpatterns = [
    url(r'^index$',views.index,name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^', views.login_user, name='login_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]

