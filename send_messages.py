from push_notifications.models import *
from push_notifications.apns import *
def main(message):
    is_repeat = True
    inactive_ids = []
    skip_ids = []
    while is_repeat:
        try:
            devices = APNSDevice.objects.exclude(pk__in = skip_ids)
            devices.send_message(message, sound='default')
            is_repeat = False
        except APNSServerError as er:
            if er.status == 8:
                inactive_ids.append(devices[er.identifier].pk)
            offset = er.identifier + 1
            skip_ids = skip_ids + [d.pk for d in devices[:offset]]
    print('inactive:', inactive_ids)
    print('skipped:', skip_ids)