
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd3*4gcwdb=wr-!9xdy5$*(!m93o+k%Seqs(#4!#k_at_hw10n^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


## celery
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'



