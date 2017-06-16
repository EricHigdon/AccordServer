from django.db import models
from django.dispatch import receiver
from django.core.mail import send_mail

# Create your models here.

class ContactSubmission(models.Model):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + ' - ' + self.subject

@receiver(models.signals.post_save, sender=ContactSubmission)
def send_email(sender, instance, created, *args, **kwargs):
    if created:
        body = 'Name: {}\n{}'.format(instance.name, instance.body)
        send_mail(instance.subject, body, instance.email, ['eric.s.higdon@gmail.com'], fail_silently=True)
