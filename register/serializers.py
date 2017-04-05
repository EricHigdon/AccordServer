from .models import Registrant
from rest_framework import serializers
from django.conf import settings

class RegistrantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Registrant
        fields = '__all__'
