import os


class BaseConfig(object):
    CACHE_TYPE = os.environ.get('CACHE_TYPE')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT')
    CACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB')
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT')