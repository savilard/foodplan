from config.settings.environs import env

STATIC_URL = env('STATIC_ROOT', default='/static/')
STATIC_ROOT = '/var/www/django/static'
