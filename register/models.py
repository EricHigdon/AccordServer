from django.db import models
from bulletin.models import Church
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.us.us_states import US_STATES
from localflavor.us import models as localmodels

# Create your models here.

class Children(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.CharField(max_length=200)

class Registrant(models.Model):
    church = models.ForeignKey(Church, related_name='registrants')
    event = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True)
    phone = PhoneNumberField(blank=True)
    street1 = models.CharField(max_length=200, blank=True)
    street2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = localmodels.USStateField(choices=US_STATES, blank=True)
    zip_code = localmodels.USZipCodeField(blank=True)
    children = models.ManyToManyField(Children, blank=True)
