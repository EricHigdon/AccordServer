from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bulletin.models import *
from display.models import *
from .forms import *
from django.forms import inlineformset_factory
from bulletin.decorators import http_basic_auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
import json
# Create your views here.

def index(request):
    return redirect('dashboard')
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
    form_submissions = FormSubmission.objects.filter(form__church=church)[:5]
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
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
        try:
            edit_item = Item.objects.get(pk=edit_pk)
        except Item.DoesNotExist:
            edit_item = None
    else:
        edit_item = None
    if request.method == 'POST':
        print(request.FILES)
        form = NewsItemForm(request.POST, request.FILES, instance=edit_item)
        if form.is_valid():
            form.save(church)
            form = NewsItemForm()
            if edit_pk is not None:
                return redirect('news')
            church.modified = timezone.now()
            church.save()
    else:
        form = NewsItemForm(instance=edit_item)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
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
        item.church.modified = timezone.now()
        item.church.save()
    return redirect('news')

@csrf_exempt
@http_basic_auth
def reorder_item(request):
    changed = False
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        for item in data:
            try:
                news_item = Item.objects.get(pk=item)
                if request.user in news_item.church.admins.all():
                    changed = True
                    news_item.sort_order = data[item]
                    news_item.save()
            except Item.DoesNotExist:
                pass
    if changed:
        church.modified = timezone.now()
        church.save()
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
            church.modified = timezone.now()
            church.save()
    else:
        form = ImNewForm(instance=church)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
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
        try:
            edit_form = Form.objects.get(pk=edit_pk)
        except Form.DoesNotExist:
            edit_form = None
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
                church.modified = timezone.now()
                church.save()
                if edit_pk is not None:
                    return redirect('connect')
    else:
        form = ConnectForm(instance=edit_form)
        field_form = FieldFormSet(instance=edit_form)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
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
        church.modified = timezone.now()
        church.save()
    return redirect('connect')

@csrf_exempt
@http_basic_auth
def reorder_form(request):
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    changed = False
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        for item in data:
            try:
                form = Form.objects.get(pk=item)
                if request.user in form.church.admins.all():
                    changed = True
                    form.sort_order = data[item]
                    form.save()
            except Form.DoesNotExist:
                pass
    if changed:
        church.modified = timezone.now()
        church.save()
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
        try:
            edit_passage = Passage.objects.get(pk=edit_pk)
        except Passage.DoesNotExist:
            edit_passage = None
    else:
        edit_passage = None
    if request.method == 'POST':
        form = PassageItemForm(request.POST, instance=edit_passage)
        if form.is_valid():
            form.save(church)
            form = PassageItemForm()
            church.modified = timezone.now()
            church.save()
            if edit_pk is not None:
                return redirect('service')
    else:
        form = PassageItemForm(instance=edit_passage)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'edit_pk': edit_pk,
        'form': form,
        'church': church,
        'active': 'service'
    }
    return render(request, template, context)

@login_required
def delete_passage(request, item_pk):
    passage = Passage.objects.get(pk=item_pk)
    if request.user in passage.church.admins.all():
        passage.delete()
        church.modified = timezone.now()
        church.save()
    return redirect('service')

@csrf_exempt
@http_basic_auth
def reorder_passage(request):
    changed = False
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        for item in data:
            try:
                passage = Passage.objects.get(pk=item)
                if request.user in passage.church.admins.all():
                    changed = True
                    passage.sort_order = data[item]
                    passage.save()
            except Passage.DoesNotExist:
                pass
    if changed:
        church.modified = timezone.now()
        church.save()
    return JsonResponse({'success': True})

@login_required
def my_church(request):
    template = 'interface/my-church.html'
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    if request.method == 'POST':
        form = MyChurchForm(request.POST, request.FILES, instance=church)
        if form.is_valid():
            form.save()
            church.modified = timezone.now()
            church.save()
    else:
        form = MyChurchForm(instance=church)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'form': form,
        'church': church,
        'active': 'my-church'
    }
    return render(request, template, context)

@login_required
def send_message(request):
    template = 'interface/send-message.html'
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MessageForm()
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'form': form,
        'church': church,
        'active': 'send-message'
    }
    return render(request, template, context)

@login_required
def display(request):
    template = 'interface/display.html'
    try:
        church = Church.objects.get(admins=request.user)
    except Church.DoesNotExist:
        return redirect('create_church')
    edit_pk = request.GET.get('edit_pk', None)
    if edit_pk is not None:
        try:
            edit_slide = Slide.objects.get(pk=edit_pk)
        except Slide.DoesNotExist:
            edit_slide = None
    else:
        edit_slide = None
    if request.method == 'POST':
        print(request.FILES)
        form = SlideForm(request.POST, request.FILES, instance=edit_slide)
        if form.is_valid():
            form.save(church)
            form = SlideForm()
            if edit_pk is not None:
                return redirect('display')
            church.modified = timezone.now()
            church.save()
    else:
        form = SlideForm(instance=edit_slide)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'edit_pk': edit_pk,
        'form': form,
        'church': church,
        'active': 'display'
    }
    return render(request, template, context)

@login_required
def delete_slide(request, item_pk):
    item = Slide.objects.get(pk=item_pk)
    if request.user in slide.church.admins.all():
        item.delete()
        item.church.modified = timezone.now()
        item.church.save()
    return redirect('display')
