from django import forms
from .models import Registrant
from bulletin.models import Church

class RegistrantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Registrant
        fields = ['event', 'church', 'first_name', 'last_name', 'email', 'phone',]
        widgets = {
            'church': forms.HiddenInput(),
            'event': forms.HiddenInput(),
            'phone': forms.TextInput(attrs={'type': 'tel'})
        }
