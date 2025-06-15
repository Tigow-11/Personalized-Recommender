from pathlib import Path
import os
import pymysql

# ✅ Install PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

# ✅ Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secret Key
SECRET_KEY = 'your-secret-key'

# ✅ Debug Mode (Turn off in production)
DEBUG = True
ALLOWED_HOSTS = []

# ✅ Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recommendation',            # Your app
    'widget_tweaks',             # For form styling
]

# ✅ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# ✅ URL routing
ROOT_URLCONF = 'learning_recommender.urls'

# ✅ Templates
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# ✅ WSGI
WSGI_APPLICATION = 'learning_recommender.wsgi.application'

# ✅ MySQL Database using XAMPP
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'learning_recommender_db',     # Your created DB
        'USER': 'root',            # Default XAMPP MySQL user
        'PASSWORD': '',            # Empty password (default)
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# ✅ Password validators (you can add later)
AUTH_PASSWORD_VALIDATORS = []

# ✅ Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# In settings.py
STATICFILES_DIRS = [BASE_DIR / "static"]


STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]

# ✅ Auto Primary Key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
