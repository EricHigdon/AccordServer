from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bulletin.models import *
from display.models import *
from .forms import *
from register.resources import RegistrantResource
from django.forms import inlineformset_factory
from bulletin.decorators import http_basic_auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
import json
# Create your views here.

def get_church(request, prefetch=None):
    church = Church.objects.filter(admins=request.user)
    if request.GET.get('church_pk', None):
        request.session['church_pk'] = request.GET.get('church_pk')
    if church.count() > 1:
        request.session['churches'] = [{'pk':church.pk, 'name':church.name} for church in church.only('pk', 'name').all()]
        if request.session.get('church_pk', None):
            church = church.filter(pk=request.session.get('church_pk'))
    elif church.count() == 0:
        return None
    if prefetch is not None:
        church = church.prefetch_related(*prefetch)
    church = church.first()
    request.session['church_pk'] = church.pk
    return church

def index(request):
    template = 'interface/index.html'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = None
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, template, context)

@login_required
def dashboard(request):
    template = 'interface/dashboard.html'
    church = get_church(request)
    if church is None:
        redirect('create_church')

    form_submissions = church.form_submissions.all()
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
    church = get_church(request)
    if church is None:
        redirect('create_church')
    edit_pk = request.GET.get('edit_pk', None)
    if edit_pk is not None:
        try:
            edit_item = Item.objects.get(pk=edit_pk)
        except Item.DoesNotExist:
            edit_item = None
    else:
        edit_item = None
    if request.method == 'POST':
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
    current_items = Item.objects.current().filter(church_id=church.pk)
    upcoming_items = Item.objects.upcoming().filter(church_id=church.pk)
    past_items = Item.objects.past().filter(church_id=church.pk)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'edit_pk': edit_pk,
        'form': form,
        'church': church,
        'current_items': current_items,
        'upcoming_items': upcoming_items,
        'past_items': past_items,
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
        news_item.church.modified = timezone.now()
        news_item.church.save()
    return JsonResponse({'success': True})

@login_required
def im_new(request):
    template = 'interface/im-new.html'
    church = get_church(request)
    if church is None:
        redirect('create_church')
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
    church = get_church(request)
    if church is None:
        redirect('create_church')
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
    current_forms = Form.objects.current().filter(church_id=church.pk)
    upcoming_forms = Form.objects.upcoming().filter(church_id=church.pk)
    past_forms = Form.objects.past().filter(church_id=church.pk)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'edit_pk': edit_pk,
        'form': form,
        'field_form': field_form,
        'church': church,
        'current_forms': current_forms,
        'upcoming_forms': upcoming_forms,
        'past_forms': past_forms,
        'active': 'connect'
    }
    return render(request, template, context)

@login_required
def delete_form(request, form_pk):
    form = Form.objects.get(pk=form_pk)
    if request.user in form.church.admins.all():
        form.delete()
        form.church.modified = timezone.now()
        form.church.save()
    return redirect('connect')

@csrf_exempt
@http_basic_auth
def reorder_form(request):
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
        form.church.modified = timezone.now()
        form.church.save()
    return JsonResponse({'success': True})

@login_required
def service(request):
    template = 'interface/service.html'
    church = get_church(request)
    if church is None:
        redirect('create_church')
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
    current_passages = Passage.objects.current().filter(church_id=church.pk)
    upcoming_passages = Passage.objects.upcoming().filter(church_id=church.pk)
    past_passages = Passage.objects.past().filter(church_id=church.pk)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'edit_pk': edit_pk,
        'form': form,
        'church': church,
        'current_passages': current_passages,
        'upcoming_passages': upcoming_passages,
        'past_passages': past_passages,
        'active': 'service'
    }
    return render(request, template, context)

@login_required
def delete_passage(request, item_pk):
    passage = Passage.objects.get(pk=item_pk)
    if request.user in passage.church.admins.all():
        passage.delete()
        passage.church.modified = timezone.now()
        passage.church.save()
    return redirect('service')

@csrf_exempt
@http_basic_auth
def reorder_passage(request):
    changed = False
    passage = None
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
    if passage is not None and changed:
        passage.church.modified = timezone.now()
        passage.church.save()
    return JsonResponse({'success': True})

@login_required
def my_church(request):
    template = 'interface/my-church.html'
    church = get_church(request)
    if church is None:
        redirect('create_church')
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
def campaigns(request):
    template = 'interface/campaigns.html'
    church = get_church(request)
    if church is None:
        redirect('create_church')
    campaign_pk = request.GET.get('campaign_pk', None)
    edit_campaign_pk = request.GET.get('edit_campaign_pk', None)
    if campaign_pk is not None:
        campaign_pk = int(campaign_pk)
        try:
            campaign = Campaign.objects.get(pk=campaign_pk)
        except Campaign.DoesNotExist:
            campaign = None
    else:
        campaign = None
    edit_pk = request.GET.get('edit_pk', None)
    if campaign is not None:
        if edit_pk is not None:
            try:
                campaignentry = CampaignEntry.objects.get(pk=edit_pk, campaign__church_id=church.pk)
            except CampaignEntry.DoesNotExist:
                campaignentry = None
        else:
            campaignentry = None
        if request.method == 'POST':
            form = CampaignEntryForm(request.POST, request.FILES, instance=campaignentry)
            if form.is_valid():
                campaignentry = form.save(campaign)
                form = CampaignEntryForm()
                if edit_pk is not None:
                    return redirect(reverse('campaigns')+'?campaign_pk={}'.format(campaignentry.campaign_id))
                church.modified = timezone.now()
                church.save()
        else:
            form = CampaignEntryForm(instance=campaignentry)
        current_entries = CampaignEntry.objects.current().filter(campaign_id=campaign.pk)
        upcoming_entries = CampaignEntry.objects.upcoming().filter(campaign_id=campaign.pk)
        past_entries = CampaignEntry.objects.past().filter(campaign_id=campaign.pk)
    else:
        if edit_campaign_pk is not None:
            try:
                edit_campaign = church.campaigns.get(pk=edit_campaign_pk)
            except Campaign.DoesNotExist:
                edit_campaign = None
        else:
            edit_campaign = None
        if request.method == 'POST':
            form = CampaignForm(request.POST, request.FILES, instance=edit_campaign)
            if form.is_valid():
                edit_campaign = form.save(church)
                form = CampaignForm()
                if edit_campaign_pk is not None:
                    return redirect(reverse('campaigns')+'?campaign_pk={}'.format(edit_campaign.pk))
                church.modified = timezone.now()
                church.save()
        else:
            form = CampaignForm(instance=edit_campaign)
        current_entries = []
        upcoming_entries = []
        past_entries = []
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'edit_pk': edit_pk,
        'campaign_pk': campaign_pk,
        'edit_campaign_pk': edit_campaign_pk,
        'church': church,
        'form': form,
        'campaign': campaign,
        'current_entries': current_entries,
        'upcoming_entries': upcoming_entries,
        'past_entries': past_entries,
        'active': 'campaigns'
    }
    return render(request, template, context)

@login_required
def delete_campaignentry(request, item_pk):
    campaignentry = CampaignEntry.objects.get(pk=item_pk)
    if request.user in campaignentry.campaign.church.admins.all():
        campaignentry.delete()
        campaignentry.campaign.church.modified = timezone.now()
        campaignentry.campaign.church.save()
    return redirect(reverse('campaigns')+'?campaign_pk={}'.format(campaignentry.campaign_id))

@login_required
def delete_campaign(request, item_pk):
    campaign = Campaign.objects.get(pk=item_pk)
    if request.user in campaign.church.admins.all():
        campaign.delete()
        campaign.church.modified = timezone.now()
        campaign.church.save()
    return redirect('campaigns')

@csrf_exempt
@http_basic_auth
def reorder_campaignentry(request):
    changed = False
    campaignentry = None
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        for item in data:
            try:
                campaignentry = CampaignEntry.objects.get(pk=item)
                if request.user in campaignentry.campaign.church.admins.all():
                    changed = True
                    campaignentry.sort_order = data[item]
                    campaignentry.save()
            except CampaignEntry.DoesNotExist:
                pass
    if campaignentry is not None and changed:
        campaignentry.campaign.church.modified = timezone.now()
        campaignentry.campaign.church.save()
    return JsonResponse({'success': True})

@login_required
def send_message(request):
    template = 'interface/send-message.html'
    church = get_church(request)
    if church is None:
        redirect('create_church')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save(church)
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
    church = get_church(request)
    if church is None:
        redirect('create_church')
    edit_pk = request.GET.get('edit_pk', None)
    if edit_pk is not None:
        try:
            edit_slide = Slide.objects.get(pk=edit_pk)
        except Slide.DoesNotExist:
            edit_slide = None
    else:
        edit_slide = None
    if request.method == 'POST':
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
    slide = Slide.objects.get(pk=item_pk)
    if request.user in slide.church.admins.all():
        slide.delete()
    return redirect('display')

@login_required
def home(request):
    template = 'interface/home.html'
    church = get_church(request)
    if church is None:
        redirect('create_church')
    if request.method == 'POST':
        form = HomeForm(request.POST, request.FILES, instance=church)
        if form.is_valid():
            form.save()
            church.modified = timezone.now()
            church.save()
            form = HomeForm(instance=church)
    else:
        form = HomeForm(instance=church)
    context = {
        'static_url': settings.STATIC_URL,
        'upload_path': settings.UPLOAD_PATH,
        'form': form,
        'church': church,
        'active': 'home'
    }
    return render(request, template, context)

@login_required
def view_registrant_data(request):
    template = 'interface/registrant-data.html'
    church = get_church(request, prefetch=['registrants'])
    if church is None:
        redirect('create_church')
    events = church.registrants.order_by('event').distinct().values_list(
        'event', flat=True
    )
    event = request.GET.get('event', '')
    registrants = church.registrants.filter(event=event).order_by('-pk')
    edit_pk = request.GET.get('edit_pk', None)
    if edit_pk is not None:
        try:
            edit_registrant = Registrant.objects.get(pk=edit_pk)
        except Registrant.DoesNotExist:
            edit_registrant = None
    else:
        edit_registrant = None
    if request.method == 'POST':
        form = RegistrantForm(request.POST, instance=edit_registrant)
        children_form = ChildrenFormSet(request.POST, instance=edit_registrant)
        if form.is_valid() and children_form.is_valid():
            form.save(church)
            children_form.save()
            form = RegistrantForm()
            if edit_pk is not None:
                return redirect(reverse('registrant_data')+'?event='+event)
    else:
        form = RegistrantForm(instance=edit_registrant)
        children_form = ChildrenFormSet(instance=edit_registrant)
    context = {
        'church': church, 'events': events, 'registrants': registrants,
        'form': form, 'active': 'registrant-data',
        'children_form': children_form
    }
    return render(request, template, context)

####################
##  Export Views  ##
####################
@login_required
def export_registrants(request, event):
    church = get_church(request)
    if church is None:
        redirect('create_church')
    else:
        church = church.pk
    dataset = RegistrantResource(church, event).export()
    response = HttpResponse(content=dataset.csv, content_type='text/csv')
    response['Content-disposition'] = 'attachment; filename={} registrants.csv'.format(event)
    return response

####################
##  Static Views  ##
####################
def privacy_policy(request):
    template = 'interface/privacy-policy.html'
    context = {}
    return render(request, template, context)

def support(request):
    template = 'interface/support.html'
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            form.save()
            form = None
    else:
        form = SupportForm()
    context = {'form': form}
    return render(request, template, context)

def get_started(request):
    template = 'interface/get_started.html'
    if request.method == 'POST':
        form = GetStartedForm(request.POST)
        if form.is_valid():
            form.save()
            form = None
    else:
        form = GetStartedForm()
    context = {'form': form}
    return render(request, template, context)
