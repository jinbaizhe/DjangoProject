"""Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
app_name = 'Admin'
urlpatterns = [
    path('index/', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('changepassowrd/', changepassowrd, name='changepassowrd'),
    re_path('^notice/(?:page-(?P<current_page>\d+)/)?', notice, name='notice'),
    path('deletenotice/<int:noticeid>/', delete_notice, name='delete_notice'),
    re_path('^visit/(?:page-(?P<current_page>\d+)/)?', visit, name='visit'),
    re_path('^message/(?:page-(?P<current_page>\d+)/)?', message, name='message'),
    path('deletemessage/<int:messageid>/', delete_message, name='delete_message'),
    path('deletevisit/<int:visitorid>/', delete_visitor, name='delete_visitor'),
    re_path('^userSetting/(?:page-(?P<current_page>\d+)/)?', userSetting, name='userSetting'),
    path('setadmin/<int:userid>/', setAdmin, name='setAdmin'),
    path('resetadmin/<int:userid>/', resetAdmin, name='resetAdmin'),
]
