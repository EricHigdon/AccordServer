from django.contrib import admin

from groupme.api import GroupMeAPI
from groupme.models import SignupItem, SignupList
from django import forms


class SignupItemInline(admin.TabularInline):
    model = SignupItem


class SignupAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        groups = GroupMeAPI().get_groups()
        group_ids = []
        for group in groups:
            group_ids.append((group['id'], group['name']))
        self.fields['group'] = forms.ChoiceField(choices=group_ids)
    class Meta:
        model = SignupList
        fields = '__all__'


class SignupAdmin(admin.ModelAdmin):
    form = SignupAdminForm
    inlines = [SignupItemInline]


admin.site.register(SignupList, SignupAdmin)
