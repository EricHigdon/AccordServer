#!/usr/bin/env python
import os
import sys
import django
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
    django.setup()
    from push_notifications.models import APNSDevice
    devices = APNSDevice.objects.all()
    devices.send_message(sys.argv[1], sound='default')
