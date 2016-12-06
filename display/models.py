from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from bulletin.models import Church
from django.utils import timezone

upload_storage = FileSystemStorage(location=settings.UPLOAD_URL)
SLIDE_STATUSES = (
    ('active', 'Active'),
    ('future', 'Future'),
    ('past', 'Past'),
)
# Create your models here.

class Slide(models.Model):
    church = models.ForeignKey(Church, related_name='slides')
    name = models.CharField(max_length=200, unique=True)
    image = models.FileField(storage=upload_storage, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=SLIDE_STATUSES)
    class Meta:
        ordering = ['status']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.start_date > now:
            self.status = 'future'
        elif self.end_date is not None and self.end_date < now:
            self.status = 'past'
        else:
            self.status = 'active'
        super(Slide, self).save(*args, **kwargs)
            
