from config.settings.environs import env

ALLOWED_HOSTS = [
    env.str('DOMAIN_NAME'),
    'backend',
    '127.0.0.1',
]
