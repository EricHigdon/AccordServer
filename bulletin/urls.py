from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^api/(?P<slug>[\w]+)/$', views.api, name='api'),
    url(r'^form/(?P<form_id>[0-9]+)/$', views.form, name='form'),
]
