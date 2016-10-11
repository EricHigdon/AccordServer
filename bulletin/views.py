from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import Template, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
import random
from .models import *
from .forms import *

# Create your views here.
def main(request, slug):
    template = 'bulletin/base.html'
    extra_classes = ''
    pages = []
    bulletin = get_object_or_404(Bulletin, slug=slug)
    if request.user == bulletin.admin:
        is_admin = True
    else:
        is_admin = False
    page_objects = bulletin.pages.all()
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
        bulletin = Bulletin.objects.get(slug=slug, admin=request.user)
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
        context = {'form':form, 'bulletin':bulletin, 'item':item, 'action':action}
        return render(request, template, context)

def manifest(request):
    template = 'bulletin/cache.manifest'
    context = {'version': random.random()}
    return render(request, template, context, content_type='text/cache-manifest')

def api(request, slug):
    extra_classes = ''
    pages = []
    forms = []
    bulletin = get_object_or_404(Bulletin, slug=slug)
    if request.user == bulletin.admin:
        is_admin = True
    else:
        is_admin = False
    page_objects = bulletin.pages.all()
    forms = bulletin.forms.all()
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
            'bulletin': bulletin
        })
        pages.append({'title': page.title, 'content': t.render(c)})
    response = JsonResponse({'pages': pages}, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        post_data = dict(request.POST)
        file_data = request.FILES.items()
        recipient = post_data.pop('recipient')[0].split(",")
        subject = post_data.pop('form')[0]
        email_context = {
            'post_data': post_data
        }
        msg_plain = render_to_string('bulletin/contact-email.txt', email_context)
        email = EmailMessage(
            subject,
            msg_plain,
            request.POST.get('email', 'Fairfieldwestbaptist@gmail.com'),
            recipient
        )
        for key, upload in file_data:
            email.attach(upload.name, upload.read(), upload.content_type)
        email.send()
    response = JsonResponse({'success':True})
    response['Access-Control-Allow-Origin'] = '*'
    return response

def form(request, form_id):
    template = 'bulletin/form.html'
    form = get_object_or_404(Form, pk=form_id)
    formset = ContactForm(instance=form)
    response = render(request, template, {'form': formset})
    response['Access-Control-Allow-Origin'] = '*'
    return response