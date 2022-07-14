from split_settings.tools import include

from .environs import env

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG', cast=bool, default=False)

_base_settings = (
    './auth.py',
    './boilerplate.py',
    './db.py',
    './environs.py',
    './i18n.py',
    './installed_apps.py',
    './http.py',
    './media.py',
    './middleware.py',
    './static.py',
    './templates.py',
    './timezone.py',
)

include(*_base_settings)
