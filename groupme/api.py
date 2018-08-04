import requests
from django.conf import settings
import json


class GroupMeAPI():

    def send_request(self, method, url, data):
        token = getattr(settings, 'GROUPME_TOKEN', None)
        url = 'https://api.groupme.com/v3/{}?token={}'.format(url, token)
        response = requests.request(method, url, json=data)
        if response.status_code in [200, 201]:
            try:
                return response.json()['response']
            except (KeyError, json.decoder.JSONDecoderError):
                pass
        elif response.status_code == 400:
            print(response.json()['meta']['errors'])

    def get_groups(self):
        url = 'groups'
        data = {
            'omit': 'memberships',
            'per_page': 1000,
        }
        response = self.send_request('GET', url, data)
        return response

    def send_message(self, group_id, message):
        url = 'groups/{}/messages'.format(group_id)
        response = self.send_request('POST', url, {'message': message})
        return response

    def create_bot(self, bot_name, group_id, callback):
        url = 'bots'
        data = {'bot': {'name': bot_name, 'group_id': group_id, 'callback_url': callback}}
        return self.send_request('POST', url, data)

    def delete_bot(self, bot_id):
        url = 'bots/destroy'
        return self.send_request('POST', url, {'bot_id': bot_id})