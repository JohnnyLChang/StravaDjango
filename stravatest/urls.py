"""stravatest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from stravatest.views import hello_world
from django.core.urlresolvers import reverse_lazy
from stravauth.views import StravaAuth
from views import HomeView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^stravatest/$', hello_world),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^stravalogin/', StravaAuth.as_view(url=reverse_lazy("home")), kwargs={"approval_prompt": "force"}, name="stravalogin"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page': '/'}, name="logout"),
]
