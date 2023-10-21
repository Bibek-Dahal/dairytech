
import os

from pathlib import Path
from django.utils.translation import gettext_lazy as _

from django.urls import reverse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG')))
# DEBUG = os.environ.get('DEBUG')   
# DEBUG = False
print('DEBUG===',DEBUG)
print(os.environ.get('DB_USER'))



ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_account',
    'allauth',
    'allauth.account',
    'user',
    'dairyapp',
    'django_nepali',
    'fontawesomefree',
    'django_extensions',
    

    
    
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dairy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dairy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



if bool(int(os.environ.get('PRODUCTION',0))):

    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE"),
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_ROOT_USER"),
            "PASSWORD": os.environ.get("DB_ROOT_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT")
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "my_account.User"

STATIC_URL = '/static/'
STATIC_ROOT = '/home/merodairy/public_html/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/'media'
# STORAGES = {
#     # ...
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }


#allauth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_ADAPTER = 'my_account.adapters.MyAccountAdapter'
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
LOGIN_REDIRECT_URL = 'dairyapp:homepage'
LOGIN_URL = 'account_login'

# LOGOUT_REDIRECT_URL = 'account_login'

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_FORMS = {
    'add_email': 'my_account.forms.MyAddEmailForm',
    'change_password': 'my_account.forms.MyPasswordChangeForm',
    # 'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    'login': 'my_account.forms.MyLoginForm',
    'reset_password': 'my_account.forms.MyPasswordResetFrom',
    'reset_password_from_key': 'my_account.forms.MyPasswordResetFormKey',
    'set_password': 'my_account.forms.MySetPasswordForm',
    'signup': 'my_account.forms.MyUserCreationForm',
    # 'user_token': 'allauth.account.forms.UserTokenForm',
}

LOCALE_PATHS = [
    BASE_DIR/'locale',
]
# LANGUAGE_CODE = 'ne'
LANGUAGES = [
    ("ne", _("Nepali")),
    ("en", _("English")),
]

# Mial Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')


# #Celery 
# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
# CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

DATE_FORMAT = 'Y-m-d'

