from django.db import models

# Create your models here.
class Church(models.Model):
    name = models.CharField(max_length=200)
    is_premium = models.BooleanField(default=False)