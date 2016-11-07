"""docomo_mock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from common import views

urlpatterns = [
    url(r'^signin/$', views.signin, name="common.signin"),
    url(r'^signin-continue/$', views.signin_continue, name="common.signin_continue"),
    url(r'^signin-process/$', views.signin_process, name="common.signin_process"),
    url(r'^signup/$', views.signup, name="common.signup"),
    url(r'^signup-continue/$', views.signup_continue, name="common.signup_continue"),
    url(r'^signup-process/$', views.signup_process, name="common.signup_process"),
]
