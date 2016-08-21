from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^churches/', views.all_churches, name='all_churches')
]
