from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.forms.models import inlineformset_factory

from bulletin.models import *
from display.models import *
from register.models import *
from push_notifications.models import *

class ImageInput(forms.ClearableFileInput):
    template_with_initial = (
        '<label class="image-field">%(input)s<span class="header"><i class="fa fa-edit"></i> %(clear_template)s</span>'
        '<img src="'+settings.STATIC_URL+settings.UPLOAD_PATH+'%(initial_url)s"/>'
        '</label>'
    )
    template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s"><i class="fa fa-trash"></i></label>'

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('church', 'sort_order',)
        widgets = {
            'start_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'end_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'content': forms.TextInput(attrs={'class': 'html-editor'})
        }
    
    def save(self, church):
        self.instance.church = church
        super().save()

class ImNewForm(forms.ModelForm):
    class Meta:
        model = Church
        fields = ('im_new',)
        widgets = {'im_new': forms.TextInput(attrs={'class': 'html-editor'})}
        
class ConnectForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ('name', 'recipient', 'start_datetime', 'end_datetime')
        widgets = {
            'start_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'end_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
        }
    
    def save(self, church, *args, **kwargs):
        self.instance.church = church
        return super().save(*args, **kwargs)
    
class PassageItemForm(forms.ModelForm):
    class Meta:
        model = Passage
        exclude = ('church', 'sort_order',)
        widgets = {
            'start_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'end_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
        }
    
    def save(self, church):
        self.instance.church = church
        super().save()
        
class MyChurchForm(forms.ModelForm):
    class Meta:
        model = Church
        exclude = ('admins', 'modified', 'im_new', 'foreground_image', 'background_image')
        widgets = {
            'address': forms.TextInput(attrs={'class': 'html-editor'}),
            'logo': ImageInput()
        }

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ('church',)
        widgets = {
            'start_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'end_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'content': forms.TextInput(attrs={'class': 'html-editor'})
        }
    
    def save(self, church):
        self.instance.church = church
        super().save()


class CampaignEntryForm(forms.ModelForm):
    class Meta:
        model = CampaignEntry
        exclude = ('campaign', 'sort_order',)
        widgets = {
            'start_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'end_datetime': forms.TextInput(attrs={
                'class': 'date',
                'placeholder': 'leave blank for indefinite'
            }),
            'content': forms.TextInput(attrs={'class': 'html-editor'})
        }

    def save(self, campaign):
        self.instance.campaign = campaign
        super().save()

class HomeForm(forms.ModelForm):
    class Meta:
        model = Church
        fields = ('foreground_image', 'background_image')
        widgets = {
            'foreground_image': ImageInput(),
            'background_image': ImageInput()
        }
        
class MessageForm(forms.Form):
    message = forms.CharField(max_length=200)
    sound = forms.BooleanField(
        initial=True,
        help_text='Determines whether or not the user will be notified with sound/vibration.',
        required=False    
    )
    force_update = forms.BooleanField(
        help_text='This forces older versions of the app to clear the cache a pull all new content.',
        required=False
    )
    
    def save(self, *args, **kwargs):
        apn_devices = APNSDevice.objects.filter(active=True)
        gcm_devices = GCMDevice.objects.filter(active=True)
        if self.cleaned_data['sound']:
            apn_devices.send_message(
                self.cleaned_data['message'],
                sound='default',
                content_available=self.cleaned_data['force_update']
            )
            gcm_devices.send_message(
                self.cleaned_data['message'],
                sound='default',
                content_available=self.cleaned_data['force_update']
            )
        else:
            apn_devices.send_message(
                self.cleaned_data['message'],
                content_available=self.cleaned_data['force_update']
            )
            gcm_devices.send_message(
                self.cleaned_data['message'],
                content_available=self.cleaned_data['force_update']
            )
        
class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        exclude = ('church', 'status',)
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'date'}),
        }
    
    def save(self, church):
        self.instance.church = church
        super().save()

class RegistrantForm(forms.ModelForm):
    class Meta:
        model = Registrant
        exclude = ('church', 'children',)
        widgets = {
            'event': forms.HiddenInput(),
            'phone': forms.TextInput(attrs={'type': 'tel'}),
            'state': forms.Select(attrs={'class': 'form-control'})
        }
    
    def save(self, church):
        self.instance.church = church
        super().save()

ChildrenFormSet = inlineformset_factory(
    Registrant, Child, fields='__all__', extra=1
)

class SupportForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())

    def save(self):
        send_mail('support request', self.cleaned_data['message'], 'eric.s.higdon@gmail.com', [self.cleaned_data['email']], fail_silently=False)
