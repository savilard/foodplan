from .environs import env

MEDIA_URL = '/media/'
MEDIA_ROOT = env('MEDIA_ROOT', cast=str, default='media')
