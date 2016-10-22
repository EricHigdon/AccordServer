from .models import Slide
from rest_framework import serializers
from django.conf import settings

class SlideSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Slide
        fields = ('name', 'image')
    
    def get_image(self, slide):
        request = self.context.get('request')
        image_url = slide.image.url
        return settings.STATIC_URL + settings.UPLOAD_PATH + '/' + image_url