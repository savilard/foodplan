import environ

env = environ.Env()
environ.Env.read_env('backend/.env')

__all__ = [
    env,
]
