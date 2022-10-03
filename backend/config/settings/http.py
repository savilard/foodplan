from config.settings.environs import env

ALLOWED_HOSTS = [
    env.str('DOMAIN_NAME'),
    'backend',
]
