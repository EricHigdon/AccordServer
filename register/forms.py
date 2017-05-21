from django import forms
from django.forms.models import inlineformset_factory
from .models import Registrant, Child
from bulletin.models import Church

class RegistrantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['street1'].is_address = True
        self.fields['street2'].is_address = True
        self.fields['city'].is_address = True
        self.fields['state'].is_address = True
        self.fields['zip_code'].is_address = True

    class Meta:
        model = Registrant
        fields = '__all__'
        widgets = {
            'church': forms.HiddenInput(),
            'event': forms.HiddenInput(),
            'phone': forms.TextInput(attrs={'type': 'tel'}),
        }

ChildrenFormSet = inlineformset_factory(
    Registrant, Child, fields='__all__', can_delete=False
)
