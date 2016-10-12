DEBUG = True
#STATIC_URL = '/static/'
ALLOWED_HOSTS = [
    'localhost'
]

PUSH_NOTIFICATIONS_SETTINGS = {
        #"GCM_API_KEY": "[your api key]",
        'APNS_CERTIFICATE': 'dev.pem',
}