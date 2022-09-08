from config.settings.environs import env

STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT', default='static')
