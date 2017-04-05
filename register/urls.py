from django.conf.urls import url, include
from .views import Register, RegistrantViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api', RegistrantViewSet)


urlpatterns = [
    url(r'^$', Register.as_view(), name='register'),        
    url(r'^', include(router.urls)),
]
