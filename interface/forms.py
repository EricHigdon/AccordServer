from django import forms
from bulletin.models import *

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