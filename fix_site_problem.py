# python manage.py shell
from django.contrib.sites.models import Site
Site.objects.filter(id=1).update(domain='ahmedhashim.pythonanywhere.com', name='Localhost')


# python manage.py shell
# from django.core.cache import cache
# cache.clear()

# # امسح مجلدات المايجريشن (ماعدا __init__.py)
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete

# # أنشئ المايجريشن من جديد
# python manage.py makemigrations
# python manage.py migrate
