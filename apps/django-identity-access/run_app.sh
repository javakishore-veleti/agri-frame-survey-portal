python manage.py makemigrations entitlements
python manage.py migrate

# This creates: username=admin, password=admin, is_staff=True, is_superuser=True, is_active=True.
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@agri.local \
DJANGO_SUPERUSER_PASSWORD=admin \
python manage.py createsuperuser --noinput

python manage.py runserver 0.0.0.0:6080