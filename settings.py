# Django settings for store project.

import os
import socket
import sys
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

TEMPLATE_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

if socket.gethostname() == "gottastitchemall":
  DEBUG = False
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'django_store',                      # Or path to database file if using sqlite3.
        'USER': 'app_runner',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
  }
else:
  DEBUG = True
  DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.sqlite3',
	'NAME': 'store.db',
    }
  }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
index_path = "./index"

if socket.gethostname() == "gottastitchemall":
	MEDIA_ROOT = '/web/static/media'
	index_path = "./store/index"
else:
	MEDIA_ROOT = os.path.abspath('./media')
	index_path = "./index"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7t0433b_fg+y1y=l)-qfnj)obv+%1oe_a8g5m7sy$)5zl)6&w_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'store.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/willm1/store.twoevils.net/store/templates'
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'store',
    'mptt',
    'whoosh',
)

def debug_extras(): return {}
if DEBUG:
	def real_debug():
		from django.db import connection
		return connection.queries
	debug_extras = real_debug

def addExtraStuff(request):
	from forms import SearchForm
	import store.models
	tree = store.models.FandomHierarchy.objects.extra(select={"sub_images": """
                        SELECT COUNT(DISTINCT pattern_id) from store_pattern_fandoms
                        WHERE fandomhierarchy_id in (
                                SELECT id FROM store_fandomhierarchy m2 where m2.tree_id = store_fandomhierarchy.tree_id
                                                                   and m2.lft between store_fandomhierarchy.lft and store_fandomhierarchy.rght)
                """})
	return {
		"debug": debug_extras(),
		"tree": tree,
		"search": SearchForm(),
	}

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.contrib.messages.context_processors.messages", "settings.addExtraStuff")

ALLOWED_HOSTS = ['localhost', 'store.twoevils.net', 'gotta-stitch-em-all.com']
