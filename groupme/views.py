from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context
from groupme.api import GroupMeAPI
from groupme.models import SignupList
import json


api = GroupMeAPI()


def send_list(list):
    t = Template(list.message)
    c = Context({'list': list})
    text = t.render(c)
    message = {
        'source_guid': list.id,
        'text': text
    }
    api.send_message(list.group, message)


def deemoji(string):
    return_string = ''
    for character in string:
        try:
            character.encode('ascii')
            return_string += character
        except UnicodeEncodeError:
            pass
    return return_string


@csrf_exempt
def webhook(request, list_pk):
    list = get_object_or_404(SignupList, pk=list_pk)
    message = json.loads(request.body.decode('utf-8'))
    name = deemoji(message['name'])
    text = message['text'].lower()
    if not text.startswith('we need'):
        signed_up = False
        for item in list.items.all():
            if item.title.lower() in text:
                if item.signed_up != '':
                    name = ' {}'.format(name)
                item.signed_up += name
                item.save()
                signed_up = True
            else:
                item.signed_up = ''

        if signed_up:
            send_list(list)

    return HttpResponse()
