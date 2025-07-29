from pathlib import Path
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '127.0.0.1:8000', 'ahmedhashim.pythonanywhere.com']

# SITE_ID = 4

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"], 
        "APP_DIRS": True,  
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.context_module.global_context",
            ],
        },
    },
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
DEBUG = True


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'



# python manage.py migrate --settings=project.settings.dev
# python manage.py runserver --settings=project.settings.dev
# python manage.py collectstatic --settings=project.settings.dev
# python manage.py createsuperuser --settings=project.settings.dev
