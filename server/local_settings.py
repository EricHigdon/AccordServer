DEBUG = True
PUSH_NOTIFICATIONS_SETTINGS = {
    'GCM_API_KEY': 'AIzaSyDDNTILe2EW44CZHd21rlZCrfdXD0J48zs',
    #'APNS_CERTIFICATE': '/certs/accord/dev.pem',
    'APNS_CERTIFICATE': '/certs/accord/dist.pem',
    'APNS_HOST': 'gateway.push.apple.com',
}

#STATIC_URL = '/static/'
#UPLOAD_PATH = 'img/uploads/'
#UPLOAD_URL = '/Users/erichigdon/venvs/churchapp/lib/python3.5/site-packages/django/contrib/admin/static/' + UPLOAD_PATH

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'accordapp',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
