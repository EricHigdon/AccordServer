from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

upload_storage = FileSystemStorage(location=settings.UPLOAD_URL)
# Create your models here.

class Slide(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.FileField(storage=upload_storage, blank=True)
    
    def __str__(self):
        return self.name
    