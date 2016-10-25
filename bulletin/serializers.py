from bulletin.models import *
from rest_framework import serializers


class FormSerializer(serializers.ModelSerializer):
    class Meta:
    model = Form
    fields = ('name', 'recipient', 'fields')
