from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "library"
    SECURITY_PASSWORD_SALT = "library"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-token"

    # Celery configurations for Redis
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/1"
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    timezone = 'Asia/Kolkata'

    # Cache configurations for Redis
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/2'
    CACHE_DEFAULT_TIMEOUT = 200

    JWT_SECRET_KEY = SECRET_KEY
    REDIS_URL = "redis://localhost:6379"