from django.conf.urls import url
from .views import Register

urlpatterns = [
    url(r'^$', Register.as_view(), name='register'),        
]
