import os


class BaseConfig(object):
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'redis')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.environ.get('CACHE_REDIS_PORT', 6379))
    CACHE_REDIS_DB = int(os.environ.get('CACHE_REDIS_DB', 0))
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
