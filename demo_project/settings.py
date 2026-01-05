from pathlib import Path
import os

# BASE_DIR should point at the Django project folder (where manage.py, db.sqlite3, templates/ and static/ live)
BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'dev-secret-key-change-me'
DEBUG = True
ALLOWED_HOSTS = ['.onrender.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'demo_project.core.apps.CoreConfig',
    'demo_project.gamify.apps.GamifyConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo_project.urls'

TEMPLATES = [
    {
        'BACKEND':'django.template.backends.django.DjangoTemplates',
        'DIRS':[ BASE_DIR / 'templates' ],
        'APP_DIRS':True,
        'OPTIONS':{'context_processors':[
            'django.template.context_processors.debug','django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages',
        ]},
    }
]

# Sanity check: warn at startup if the configured templates directory doesn't exist
_templates_dir = TEMPLATES[0]['DIRS'][0]
if not _templates_dir.exists():
    import warnings
    warnings.warn(f"Templates directory {_templates_dir} does not exist; check BASE_DIR and project layout", RuntimeWarning)

}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=True
USE_TZ=True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Where unauthenticated users are redirected to log in
LOGIN_URL = '/login/'
# Where users are redirected after login/logout
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
