from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^api/(?P<church_pk>[0-9]+)/$', views.api, name='api'),
    url(r'^modified/(?P<church_pk>[0-9]+)/$', views.modified, name='modified'),
    url(r'^form/(?P<form_id>[0-9]+)/$', views.form, name='form'),
    url(r'^account/$', csrf_exempt(views.UserViewSet.as_view({'get': 'list', 'put': 'create', 'post': 'update'})), name='account'),
]
