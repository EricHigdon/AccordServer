from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bulletin.models import *
from .forms import *
from django.forms import inlineformset_factory
from bulletin.decorators import http_basic_auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.

def index(request):
    template = 'interface/index.html'
    context = {
        'title': 'Welcome',
        'active': 'home'
    }
    return render(request, template, context)

@login_required
def dashboard(request):
    template = 'interface/dashboard.html'
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    form_submissions = FormSubmission.objects.filter(form__church=church)
    context = {
        'form_submissions': form_submissions,
        'church': church,
        'active': 'overview'
    }
    return render(request, template, context)

@login_required
def news(request):
    template = 'interface/news.html'
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    edit_pk = request.GET.get('edit_pk', None)
    if edit_pk is not None:
        edit_item = Item.objects.get(pk=edit_pk)
    else:
        edit_item = None
    if request.method == 'POST':
        form = NewsItemForm(request.POST, instance=edit_item)
        if form.is_valid():
            form.save(church)
            form = NewsItemForm()
            if edit_pk is not None:
                return redirect('news')
    else:
        form = NewsItemForm(instance=edit_item)
    context = {
        'edit_pk': edit_pk,
        'form': form,
        'church': church,
        'active': 'news'
    }
    return render(request, template, context)

@login_required
def delete_item(request, item_pk):
    item = Item.objects.get(pk=item_pk)
    if request.user in item.church.admins.all():
        item.delete()
    return redirect('news')

@csrf_exempt
@http_basic_auth
def reorder_item(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        for item in data:
            try:
                news_item = Item.objects.get(pk=item)
                if request.user in news_item.church.admins.all():
                    news_item.sort_order = data[item]
                    news_item.save()
            except Item.DoesNotExist:
                pass
    return JsonResponse({'success': True})

@login_required
def im_new(request):
    template = 'interface/im-new.html'
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    if request.method == 'POST':
        form = ImNewForm(request.POST, instance=church)
        if form.is_valid():
            form.save()
    else:
        form = ImNewForm(instance=church)
    context = {
        'form': form,
        'church': church,
        'active': 'im-new'
    }
    return render(request, template, context)

@login_required
def connect(request):
    template = 'interface/connect.html'
    FieldFormSet = inlineformset_factory(
        Form,
        Field,
        fields=('name', 'field_type', 'required', 'sort_order'),
        extra=100,
        widgets={
            'name': forms.TextInput(attrs={'class': 'field-name'}),
            'sort_order': forms.HiddenInput(attrs={'class': 'sort-order'}),
        }
    )
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    edit_pk = request.GET.get('edit_pk', None)
    if edit_pk is not None:
        edit_form = Form.objects.get(pk=edit_pk)
    else:
        edit_form = None
    if request.method == 'POST':
        form = ConnectForm(request.POST, instance=edit_form)
        field_form = FieldFormSet(request.POST, instance=edit_form)
        if form.is_valid():
            new_form = form.save(church, commit=False)
            field_form = FieldFormSet(request.POST, instance=new_form)
            if field_form.is_valid():
                form.save(church)
                field_form.save()
                if edit_pk is not None:
                    return redirect('connect')
    else:
        form = ConnectForm(instance=edit_form)
        field_form = FieldFormSet(instance=edit_form)
    context = {
        'edit_pk': edit_pk,
        'form': form,
        'field_form': field_form,
        'church': church,
        'active': 'connect'
    }
    return render(request, template, context)

@login_required
def delete_form(request, form_pk):
    form = Form.objects.get(pk=form_pk)
    if request.user in form.church.admins.all():
        form.delete()
    return redirect('connect')

@csrf_exempt
@http_basic_auth
def reorder_form(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        for item in data:
            try:
                form = Form.objects.get(pk=item)
                if request.user in form.church.admins.all():
                    form.sort_order = data[item]
                    form.save()
            except Form.DoesNotExist:
                pass
    return JsonResponse({'success': True})

@login_required
def service(request):
    template = 'interface/service.html'
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    edit_pk = request.GET.get('edit_pk', None)
    if edit_pk is not None:
        edit_passage = Passage.objects.get(pk=edit_pk)
    else:
        edit_passage = None
    if request.method == 'POST':
        form = PassageItemForm(request.POST, instance=edit_passage)
        if form.is_valid():
            form.save(church)
            form = PassageItemForm()
            if edit_pk is not None:
                return redirect('service')
    else:
        form = PassageItemForm(instance=edit_passage)
    context = {
        'edit_pk': edit_pk,
        'form': form,
        'church': church,
        'active': 'service'
    }
    return render(request, template, context)

@login_required
def delete_passage(request, item_pk):
    passage = Passage.objects.get(pk=item_pk)
    if request.user in item.church.admins.all():
        passage.delete()
    return redirect('service')

@csrf_exempt
@http_basic_auth
def reorder_passage(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        for item in data:
            try:
                passage = Passage.objects.get(pk=item)
                if request.user in passage.church.admins.all():
                    passage.sort_order = data[item]
                    passage.save()
            except Passage.DoesNotExist:
                pass
    return JsonResponse({'success': True})
