from django import forms
from django.conf import settings
from django.forms.models import inlineformset_factory

from bulletin.models import *
from display.models import *
from register.models import *
from interface.models import *
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
        return super().save()


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
        return super().save()

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
    
    def save(self, church, *args, **kwargs):
        apn_devices = APNSDevice.objects.filter(active=True, user__churches=church)
        gcm_devices = GCMDevice.objects.filter(active=True, user__churches=church)
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
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea())

    def save(self):
        ContactSubmission(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            subject='support_request',
            body=self.cleaned_data['message']
        ).save()

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        exclude = ['datetime',]
        widgets = {
            'name': forms.widgets.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.widgets.EmailInput(attrs={'placeholder': 'Email'}),
            'subject': forms.widgets.TextInput(attrs={'placeholder': 'Subject'}),
            'body': forms.widgets.Textarea(attrs={'placeholder': 'Message'}),
        }

class GetStartedForm(forms.Form):
    name = forms.CharField()
    church_name = forms.CharField()
    church_website = forms.URLField(required=False)
    phone_number = forms.CharField(required=False)
    email = forms.EmailField()
    average_church_attendance = forms.IntegerField()
    notes = forms.CharField(
        label='Any other details you wish to share',
        widget=forms.Textarea(),
        required=False
    )

    def save(self):
        body = 'Church Name: {}\nChurch Website: {}\nPhone Number: {}\nChurch Size: {}'.format(
            self.cleaned_data['church_name'],
            self.cleaned_data['church_website'],
            self.cleaned_data['phone_number'],
            self.cleaned_data['average_church_attendance'],
            self.cleaned_data['notes'],
        )
        ContactSubmission(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            subject="I'm Ready to Get Started",
            body=body
        ).save()
