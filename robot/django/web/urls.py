from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import Comandos

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<key>.+)/(?P<value>.+)$', Comandos.as_view()),
)
