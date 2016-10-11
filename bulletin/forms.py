from django import forms
from .models import *

class PhoneInput(forms.widgets.TextInput):
    input_type = 'tel'

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {'page': forms.HiddenInput()}

class ContactForm(forms.Form):

    def __init__(self, instance=None, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['form'] = forms.CharField(initial=instance.name, widget=forms.HiddenInput())
        self.fields['recipient'] = forms.CharField(initial=instance.recipient, widget=forms.HiddenInput())
        for field in instance.fields.all().order_by('sort_order'):
            if field.field_type == 'char':
                self.fields[field.name] = forms.CharField(
                    required = field.required,
                    widget = forms.TextInput(attrs={'placeholder': field.name})
                )
            if field.field_type == 'email':
                self.fields[field.name] = forms.EmailField(
                    required = field.required,
                    widget = forms.EmailInput(attrs={'placeholder': field.name})
                )
            if field.field_type == 'phone':
                self.fields[field.name] = forms.CharField(
                    required = field.required,
                    widget = PhoneInput(attrs={'placeholder': field.name})
                )
            elif field.field_type == 'text':
                self.fields[field.name] = forms.CharField(
                    required = field.required,
                    widget=forms.Textarea(attrs={'placeholder': field.name})
                )
            elif field.field_type == 'int':
                self.fields[field.name] = forms.IntegerField(
                    required = field.required,
                    widget=forms.NumberInput(attrs={'placeholder': field.name})
                )
            elif field.field_type == 'bool':
                self.fields[field.name] = forms.BooleanField(
                    required = field.required,
                )
            elif field.field_type == 'choice':
                self.fields[field.name] = forms.ModelChoiceField(
                    required = field.required,
                    queryset=field.choices.all(), 
                    empty_label=field.name
                )
            elif field.field_type == 'file':
                self.fields[field.name] = forms.FileField(
                    required = field.required,
                )