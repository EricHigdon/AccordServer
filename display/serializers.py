from .models import Slide
from bulletin.models import Church
from rest_framework import serializers
from django.conf import settings
from datetime import date, datetime, timedelta

class SlideSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Slide
        fields = ('name', 'image')
    
    def get_image(self, slide):
        image_url = slide.image.url
        return settings.STATIC_URL + settings.UPLOAD_PATH + image_url

class CountdownSerializer(serializers.ModelSerializer):
    countdown = serializers.SerializerMethodField()

    class Meta:
        model = Church
        fields = ('name', 'countdown', 'countdown_image', 'countdown_position')

    def get_countdown(self, church):
        today = date.today()
        day = church.countdown_day
        time = church.countdown_time
        next_date = today + timedelta(
            days=((day-today.weekday()) % 7),
        )
        countdown_to = datetime(
            year=next_date.year,
            month=next_date.month,
            day=next_date.day,
            hour=time.hour,
            minute=time.minute,
            second=time.second
        )
        if countdown_to < datetime.now():
            next_date = today + timedelta(
                days=((day-1-today.weekday()) % 7+1),
            )
            countdown_to = datetime(
                year=next_date.year,
                month=next_date.month,
                day=next_date.day,
                hour=time.hour,
                minute=time.minute,
                second=time.second
            )

        return countdown_to