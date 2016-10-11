from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^(?P<slug>[\w]+)/$', views.main, name='index'),
    url(r'^api/(?P<slug>[\w]+)/$', views.api, name='api'),
    url(r'^form/(?P<form_id>[0-9]+)/$', views.form, name='form'),
    url(r'^(?P<slug>[\w]+)/(?P<action>[\w]+)/(?P<item_id>[0-9]+)', views.update, name='update'),
    url(r'^cache.manifest', views.manifest, name='manifest'),
]
