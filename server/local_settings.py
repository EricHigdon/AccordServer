DEBUG = True
# Legacy Settings
PUSH_NOTIFICATIONS_SETTINGS = {
    'GCM_API_KEY': 'AIzaSyDDNTILe2EW44CZHd21rlZCrfdXD0J48zs',
    'APNS_CERTIFICATE': '/certs/fwbc-dev.pem',
    'APNS_TOPIC': 'com.erichigdon.accord',
    'APNS_HOST': 'gateway.push.apple.com',
}
#PUSH_NOTIFICATIONS_SETTINGS = {
#    "CONFIG": "push_notifications.conf.AppConfig",
#    "APPLICATIONS": {
#        "FWBC_GCM": {
#            # PLATFORM (required) determines what additional settings are required.
#            "PLATFORM": "GCM",
#            # required GCM setting
#            "API_KEY": 'AIzaSyDDNTILe2EW44CZHd21rlZCrfdXD0J48zs',
#        },
#        "FWBC_APNS": {
#            "PLATFORM": "APNS",
#            #"CERTIFICATE": "/certs/accord/dist.pem",
#            "CERTIFICATE": "fwbc-dev.pem",
#            'TOPIC': 'com.erichigdon.accord',
#            #'HOST': 'gateway.push.apple.com',
#        },
#        #"LIFT_GCM": {
#        #    "PLATFORM": "GCM",
#        #    "API_KEY": 'AIzaSyDDNTILe2EW44CZHd21rlZCrfdXD0J48zs',
#        #},
#        #"LIFT_APNS": {
#        #    "PLATFORM": "APNS",
#        #    'CERTIFICATE': 'lift-dev.pem',
#        #    #'HOST': 'gateway.push.apple.com',
#        #},
#    }
#}

def get_true(item):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': get_true
}

#STATIC_URL = '/static/'
#UPLOAD_PATH = 'img/uploads/'
#UPLOAD_URL = '/Users/erichigdon/venvs/churchapp/lib/python3.5/site-packages/django/contrib/admin/static/' + UPLOAD_PATH

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'accordapp',
#        'USER': 'root',
#        'PASSWORD': '2Corinthians2:15',
#        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#        'PORT': '3306',
#        'OPTIONS': {
#            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#        },
#    }
#}
