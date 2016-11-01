from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from bulletin.models import Church

upload_storage = FileSystemStorage(location=settings.UPLOAD_URL)
# Create your models here.

class Slide(models.Model):
    church = models.ForeignKey(Church, related_name='slides')
    name = models.CharField(max_length=200, unique=True)
    image = models.FileField(storage=upload_storage, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
