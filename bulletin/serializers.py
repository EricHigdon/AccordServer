from bulletin.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('name', 'recipient', 'fields')
        
class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'auth_token', 'first_name', 'last_name', 'pk')
        extra_kwargs = {
            'auth_token': {'required': False},
            'pk': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
            'password': {'write_only': True, 'required': False}
        }