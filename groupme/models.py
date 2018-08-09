from django.core.exceptions import ValidationError
from django.db import models


class SignupList(models.Model):
    name = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    group = models.SlugField(max_length=200)
    bot_id = models.SlugField(max_length=200, blank=True)
    message = models.TextField()

    def clean(self):
        if self.end <= self.start:
            raise ValidationError({'end': 'End date must be after start date.'})
        return super().clean()

    def __str__(self):
        return self.name


class SignupItem(models.Model):
    list = models.ForeignKey(SignupList, related_name='items')
    title = models.CharField(max_length=200)
    signed_up = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ('sort_order',)

    def __str__(self):
        return self.title
