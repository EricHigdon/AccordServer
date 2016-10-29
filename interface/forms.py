from django import forms
from django.conf import settings
from bulletin.models import *

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
        widgets = {'content': forms.TextInput(attrs={'class': 'html-editor'})}
    
    def save(self, church):
        self.instance.church = church
        super(NewsItemForm, self).save()

class ImNewForm(forms.ModelForm):
    class Meta:
        model = Church
        fields = ('im_new',)
        widgets = {'im_new': forms.TextInput(attrs={'class': 'html-editor'})}
        
class ConnectForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ('name', 'recipient',)
    
    def save(self, church, *args, **kwargs):
        self.instance.church = church
        return super(ConnectForm, self).save(*args, **kwargs)
    
class PassageItemForm(forms.ModelForm):
    class Meta:
        model = Passage
        exclude = ('church', 'sort_order',)
    
    def save(self, church):
        self.instance.church = church
        super(PassageItemForm, self).save()
        
class MyChurchForm(forms.ModelForm):
    class Meta:
        model = Church
        exclude = ('admins', 'modified', 'im_new')
        widgets = {
            'address': forms.TextInput(attrs={'class': 'html-editor'}),
            'logo': ImageInput()
        }