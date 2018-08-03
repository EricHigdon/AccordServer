from django.db import models
from bulletin.models import Church
from localflavor.us.us_states import US_STATES
from localflavor.us import models as localmodels

# Create your models here.

class Registrant(models.Model):
    church = models.ForeignKey(Church, related_name='registrants')
    event = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(
    	max_length=200,
        blank=True,
        null=True,
        help_text="""
            Your phone number will not be shared in any way.
            If you choose to enter your phone number,
            you may recieve text messages about upcoming events.
        """
    )
    street1 = models.CharField(max_length=200, blank=True)
    street2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = localmodels.USStateField(choices=US_STATES, blank=True)
    zip_code = localmodels.USZipCodeField(blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Child(models.Model):
    name = models.CharField(max_length=400)
    age = models.CharField(max_length=200)
    parent = models.ForeignKey(Registrant, related_name='children')

    def __str__(self):
        return '{} ({})'.format(self.name, self.age)
