from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import Template, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
import random
from .models import *
from .forms import *
from .decorators import http_basic_auth

# Create your views here.
def main(request, slug):
    template = 'bulletin/base.html'
    extra_classes = ''
    pages = []
    church = get_object_or_404(Church, slug=slug)
    if request.user == church.admin:
        is_admin = True
    else:
        is_admin = False
    page_objects = church.pages.all()
    for page in page_objects:
        if page != page_objects[0]:
            extra_classes = 'cached'
        items = page.items.all()
        t = Template(page.template)
        c = RequestContext(request, {
            'static_url':settings.STATIC_URL,
            'items': items,
            'page':page,
            'extra_classes':extra_classes,
            'is_admin':is_admin
        })
        pages.append({'title':page.title, 'content':t.render(c)})
    context = {'pages':pages, 'is_admin':is_admin}
    response = render(request, template, context)
    response['Cache-Control'] = 'max-age=0, no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Thu, 01 Jan 1970 00:00:01 GMT'
    return response

def update(request, slug, action, item_id):
    try:
        church = Church.objects.get(slug=slug, admin=request.user)
        if action == 'update':
            item = Item.objects.get(pk=item_id)
        else:
            item = None
    except:
        return JsonResponse({'success':False})
    if request.method == 'POST':
        form = ItemForm(data=request.POST, files=request.FILES, instance=item)
        if form.is_valid():
            form.save()
            instance = form.instance
            return JsonResponse({'success':True, 'title':instance.title, 'image':instance.image.url, 'content':instance.content})
        else:
            return JsonResponse({'success':False, 'errors':form.errors})
    else:
        initial = {}
        if action == 'add':
            initial['page'] = item_id
        form = ItemForm(instance=item, initial=initial)
        template = 'bulletin/form.html'
        if action == 'add':
            item = Page.objects.get(pk=item_id)
        context = {'form':form, 'church':church, 'item':item, 'action':action}
        return render(request, template, context)

def manifest(request):
    template = 'bulletin/cache.manifest'
    context = {'version': random.random()}
    return render(request, template, context, content_type='text/cache-manifest')

def api(request, slug):
    extra_classes = ''
    pages = []
    forms = []
    church = get_object_or_404(Church, slug=slug)
    if request.user == church.admin:
        is_admin = True
    else:
        is_admin = False
    page_objects = church.pages.all()
    forms = church.forms.all()
    for page in page_objects:
        if page != page_objects[0]:
            extra_classes = 'cached'
        items = page.items.all().order_by('sort_order')
        t = Template(page.template)
        c = RequestContext(request, {
            'static_url': settings.STATIC_URL,
            'items': items,
            'page': page,
            'extra_classes': extra_classes,
            'is_admin': is_admin,
            'forms': forms,
            'church': church
        })
        pages.append({'title': page.title, 'content': t.render(c)})
    response = JsonResponse({'pages': pages}, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def contact(request):
    if request.method == 'POST':
        post_data = dict(request.POST)
        file_data = request.FILES.items()
        recipients = post_data.pop('recipient')[0].split(",")
        subject = post_data.pop('form')[0]
        token = post_data.pop('csrfmiddlewaretoken')
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        reply_email = request.POST.get('email', None)
        if reply_email is None:
            reply_email = request.POST.get('Email', None)
        email_context = {
            'post_data': post_data,
            'user_agent': user_agent
        }
        msg_plain = render_to_string('bulletin/contact-email.txt', email_context)
        msg_html = render_to_string('bulletin/contact-email.html', email_context)
        email = EmailMultiAlternatives(
            subject,
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
    response = JsonResponse({'success':True})
    response['Access-Control-Allow-Origin'] = '*'
    return response

@http_basic_auth
def form(request, form_id):
    template = 'bulletin/form.html'
    form = get_object_or_404(Form, pk=form_id)
    formset = ContactForm(instance=form)
    response = render(request, template, {'form': formset})
    response['Access-Control-Allow-Origin'] = '*'
    return response
