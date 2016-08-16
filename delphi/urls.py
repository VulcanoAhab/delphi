"""delphi URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls import handler404, handler403, handler500
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

#serving static - as a devel server 
static_url=url(r'^static\/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
urlpatterns.append(static_url)

#error handling
handler404='workers.views.sayError'
handler403='workers.views.sayError'
handler500='workers.views.sayError'

