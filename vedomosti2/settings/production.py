import os
import sys
import dj_database_url
from django.conf import settings
from urllib.parse import urlparse, uses_netloc



DEBUG = False
TEMPLATE_DEBUG = False


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# DATABASES = settings.DATABASES

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

# Register database schemes in URLs.
uses_netloc.append('mysql')

try:

    # Check to make sure DATABASES is set in settings.py file.
    # If not default to {}

    if 'DATABASES' not in locals():
        DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})

        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })


        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
except Exception:
    print ('Unexpected error:', sys.exc_info())

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticassets')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = "vedomosti"
MEDIA_URL = "https://%s.s3.amazonaws.com/" % os.environ['AWS_STORAGE_BUCKET_NAME']
MEDIA_ROOT = ''
AWS_ACCESS_KEY_ID = "AKIAJHFEGY6K4QJPYQVQ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_QUERYSTRING_AUTH = False


