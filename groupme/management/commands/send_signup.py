from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls.base import reverse
from groupme.api import GroupMeAPI
from groupme.models import SignupList
from datetime import datetime, timedelta
from groupme.views import send_list


class Command(BaseCommand):
    help = 'sends latest signup lists'

    def handle(self, *args, **options):
        lists = SignupList.objects.filter(start__lte=datetime.now(), bot_id='')
        api = GroupMeAPI()
        for list in lists:
            send_list(list)
            callback = 'https://accordapp.com{}/?token={}'.format(
                reverse('groupme_webhook', args=[list.id]),
                getattr(settings, 'GROUPME_TOKEN', '')
            )
            bot_name = '{} Signup'.format(list.name)
            response = api.create_bot(bot_name, list.group, callback)
            try:
                list.bot_id = response['bot']['bot_id']
                list.save()
            except Exception as e:
                pass

        for list in SignupList.objects.filter(end__lte=datetime.now()).exclude(bot_id=''):
            api.delete_bot(list.bot_id)
