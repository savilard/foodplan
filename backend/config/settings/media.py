from config.settings.environs import env

MEDIA_URL = env('MEDIA_ROOT', default='/media/')
MEDIA_ROOT = '/var/www/django/media'
