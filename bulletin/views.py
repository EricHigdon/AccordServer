from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import Template, RequestContext
from django.template.loader import render_to_string
from .models import *
from .forms import *
from .decorators import http_basic_auth
import feedparser
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):   
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = super(UserViewSet, self).get_queryset(*args, **kwargs)
        if self.request.user.is_authenticated():
            queryset = queryset.filter(pk=self.request.user.pk)
        return queryset

    def get_object(self):
        return self.request.user
    
@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    device = None
    try:
        device = APNSDevice.objects.get(device_id=instance.username)
    except (APNSDevice.DoesNotExist, ValueError):
        pass
    try:
        device = GCMDevice.objects.get(device_id=instance.username)
    except (GCMDevice.DoesNotExist, ValueError):
        pass
    if device is not None:
        device.user = instance
        device.save()

class ModifiedAPI(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, church_pk):
        church = get_object_or_404(Church, pk=church_pk)
        modified = church.modified
        if request.user.is_authenticated:
            user_churches = Church.objects.filter(
                users=request.user
            ).exclude(pk=church.pk)
            for user_church in user_churches:
                user_church.users.remove(request.user)
            if not church.users.filter(pk=request.user.pk).exists():
                church.users.add(request.user)
        
        latest_form_start = Form.objects.current().filter(
            church_id=church.pk
        ).order_by('-start_datetime')
        if latest_form_start:
            latest_form_start = latest_form_start[0].start_datetime
            if latest_form_start is not None and latest_form_start > modified:
                modified = latest_form_start
        latest_form_end = Form.objects.past().filter(
            church_id=church.pk
        ).order_by('-end_datetime')
        if latest_form_end:
            latest_form_end = latest_form_end[0].end_datetime
            if latest_form_end is not None and latest_form_end > modified:
                modified = latest_form_end
            
        latest_news_start = Item.objects.current().filter(
            church_id=church.pk
        ).order_by('-start_datetime')
        if latest_news_start:
            latest_news_start = latest_news_start[0].start_datetime
            if latest_news_start is not None and latest_news_start > modified:
                modified = latest_news_start
        latest_news_end = Item.objects.past().filter(
            church_id=church.pk
        ).order_by('-end_datetime')
        if latest_news_end:
            latest_news_end = latest_news_end[0].end_datetime
            if latest_news_end is not None and latest_news_end > modified:
                modified = latest_news_end
            
        latest_passage_start = Passage.objects.current().filter(
            church_id=church.pk
        ).order_by('-start_datetime')
        if latest_passage_start:
            latest_passage_start = latest_passage_start[0].start_datetime
            if latest_passage_start is not None and latest_passage_start > modified:
                modified = latest_passage_start
        latest_passage_end = Passage.objects.past().filter(
            church_id=church.pk
        ).order_by('-end_datetime')
        if latest_passage_end:
            latest_passage_end = latest_passage_end[0].end_datetime
            if latest_passage_end is not None and latest_passage_end > modified:
                modified = latest_passage_end
            
        latest_campaignentry_start = CampaignEntry.objects.current().filter(
            campaign__church_id=church.pk
        ).order_by('-start_datetime')
        if latest_campaignentry_start:
            latest_campaignentry_start = latest_campaignentry_start[0].start_datetime
            if latest_campaignentry_start is not None and latest_campaignentry_start > modified:
                modified = latest_campaignentry_start
        latest_campaignentry_end = CampaignEntry.objects.past().filter(
            campaign__church_id=church.pk
        ).order_by('-end_datetime')
        if latest_campaignentry_end:
            latest_campaignentry_end = latest_campaignentry_end[0].end_datetime
            if latest_campaignentry_end is not None and latest_campaignentry_end > modified:
                modified = latest_campaignentry_end
        
        response = JsonResponse({'modified': modified}, safe=False)
        response['Access-Control-Allow-Origin'] = '*'
        return response

def api(request, church_pk):
    extra_classes = ''
    pages = []
    forms = []
    church = get_object_or_404(Church, pk=church_pk)
    if request.user in church.admins.all():
        is_admin = True
    else:
        is_admin = False
    page_objects = church.pages.all()
    forms = Form.objects.current().filter(church_id=church.pk)
    items = Item.objects.current().filter(church_id=church.pk)
    passages = Passage.objects.current().filter(church_id=church.pk)
    if church.podcast_url:
        feed = feedparser.parse(church.podcast_url)['entries'][:10]
    else:
        feed = None

    for page in page_objects:
        if page != page_objects[0]:
            extra_classes = 'cached'
        t = Template(page.template)
        c = RequestContext(request, {
            'static_url': settings.STATIC_URL,
            'items': items,
            'passages': passages,
            'page': page,
            'extra_classes': extra_classes,
            'is_admin': is_admin,
            'forms': forms,
            'feed': feed,
            'church': church
        })
        pages.append({'title': page.title, 'content': t.render(c)})
    response = JsonResponse({'pages': pages}, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response

@http_basic_auth
def contact(request):
    if request.method == 'POST':
        post_data = dict(request.POST)
        file_data = request.FILES.items()
        recipients = post_data.pop('recipient')[0].split(",")
        token = post_data.pop('csrfmiddlewaretoken')
        form_pk = post_data.pop('form')[0]
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        reply_email = request.POST.get('email', None)
        if reply_email is None:
            reply_email = request.POST.get('Email', None)
        if form_pk is not None:
            try:
                form = Form.objects.get(pk=form_pk)
                email_context = {
                    'form': form,
                    'post_data': post_data,
                    'user_agent': user_agent
                }
                msg_plain = render_to_string('bulletin/contact-email.txt', email_context)
                msg_html = render_to_string('bulletin/contact-email.html', email_context)
                submission = FormSubmission(form_name=form.name, content=msg_html, church=form.church)
                submission.save()
                email = EmailMultiAlternatives(
                    form.name,
                    msg_plain,
                    'Fairfieldwestbaptist@gmail.com',
                    recipients,
                    ['eric.s.higdon@gmail.com'],
                    reply_to=[reply_email]
                )
                for key, upload in file_data:
                    email.attach(upload.name, upload.read(), upload.content_type)
                email.attach_alternative(msg_html, "text/html")
                email.send()
            except Church.DoesNotExist:
                print('error')
    response = JsonResponse({'success':True})
    response['Access-Control-Allow-Origin'] = '*'
    return response

@http_basic_auth
def form(request, form_id):
    template = 'bulletin/form.html'
    form = get_object_or_404(Form, pk=form_id)
    formset = ContactForm(instance=form)
    response = render(request, template, {'form': formset, 'contact_form': form})
    response['Access-Control-Allow-Origin'] = '*'
    return response
