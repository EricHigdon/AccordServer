from .models import Registrant
from rest_framework import serializers
from django.conf import settings

class RegistrantSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Registrant
        fields = '__all__'

    def get_children(self, obj):
        return obj.children.count()
