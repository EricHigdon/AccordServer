from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import Template, RequestContext
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import random
from .models import *
from .forms import *
from .decorators import http_basic_auth

# Create your views here.
@http_basic_auth
def modified(request, church_pk):
    church = get_object_or_404(Church, pk=church_pk)
    response = JsonResponse({'modified': church.modified}, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    return response

@http_basic_auth
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
    forms = church.forms.all()
    items = church.news_items.all().order_by('sort_order')
    for page in page_objects:
        if page != page_objects[0]:
            extra_classes = 'cached'
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
                submission = FormSubmission(form=form, content=msg_html)
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
