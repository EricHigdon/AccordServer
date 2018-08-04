from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^webhook/(?P<list_pk>[0-9]+)', views.webhook, name='groupme_webhook')
]