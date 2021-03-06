import os  # isort:skip

gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for aps_shared_farm project.

Generated by 'django-admin startproject' using Django 3.1.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^c%#9^hmr#o#3%aa8th!toc7cf0*o^db6(k4-+07lfg#+di(j8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition


ROOT_URLCONF = 'aps_shared_farm.urls'

WSGI_APPLICATION = 'aps_shared_farm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'aps_shared_farm', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
SITE_ID = 1
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'aps_shared_farm', 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',

            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware', #NEW, added for Caching, Incomplete
]

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'rest_framework',
    'drf_yasg',
    'rest_framework.authtoken',
    'core.apps.CoreConfig',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',
    'djangocms_file',
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_googlemap',
    'djangocms_video',
    'aps_shared_farm',
    'aldryn_apphooks_config',
    'parler',
    'taggit',
    'taggit_autosuggest',
    'meta',
    'sortedm2m',
    'djangocms_blog',
    'sharedfarm',
    'aps_plugins',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'formtools',

]

LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
    ('bn', gettext('bn')),
)

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'code': 'en',
            'name': gettext('en'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
        {
            'code': 'bn',
            'name': gettext('bn'),
            'fallbacks': ['en'],
            'public': True,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}
LOGIN_REDIRECT_URL = '/sharedfarm/#farms'   ##Added for redirecting after login - 13-03-2022
LOGIN_URL = '/accounts/login'
LOGOUT_URL = '/accounts/logout'
CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('home.html', 'Home'),
    ('about.html', 'About'),
    ('technology.html', 'Technology'),
    ('policy.html', 'Policy'),
    ('terms.html', 'Terms'), # NEW added Terms and Condition template 
)

X_FRAME_OPTIONS = 'SAMEORIGIN'

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {

    'feature': {
        "plugins": ('Section_With_Image_Background_Plugin',),
        'name': "Heading Feature",
        'plugin_labels': {
            'Section_With_Image_Background_Plugin': 'Add Heading Background Image'
        },
        'limits': {
            'global': 1,
        },
    },
    'who_we_are_text': {
        'plugins': ('WhoWeAreLandingTextPlugin',),
        'name': 'Who We Are short description',
        'plugin_labels': {
            'Section_With_Image_Background_Plugin': 'Add a short description under Who We Are'
        },
        'limits': {
            'global': 1,
        },
    },
    'banner_text': {
        'plugins': ('TextPlugin',),
        'name': 'Banner short description',
        'plugin_labels': {
            'TextPlugin': 'Add a short description over banner'
        },
        'limits': {
            'local': 1,
        },
    },
    'app_link': {
        'plugins': ('SharedFarmBannerAppURLPlugin',),
        'name': 'SharedFarm App URL',
        'plugin_labels': {
            'SharedFarmBannerAppURLPlugin': 'Add sharedfarm app url'
        },
        'limits': {
            'global': 1,
        },
    },
    'image_fields': {
        'plugins': ('SharedFarmBannerImagePlugin',),
        'name': 'SharedFarm banner images',
        'plugin_labels': {
            'SharedFarmBannerImagePlugin': 'Add banner images'
        },
        'limits': {
            'global': 1,
        },
    },
    'policy_text': {
        'plugins': ('PolicyPlugin'),
        'name': 'Policy Plugin',
        'plugin_label': {
            'PolicyPlugin': 'Add a policy'
        },
    },
    'terms_text': {     # NEW, added for Terms of Service 23/03/2022
        'plugins': ('TermsOfServicePlugin'),
        'name': 'Terms of Service Plugin',
        'plugin_label': {
            'TermsOfServicePlugin': 'Add a Terms of Service'
        },
    },
    'footer_links_services': {
        'plugins': ('FooterPlugin',),
        'name': 'Footer Services Plugin',
        'plugin_label': {
            'FooterPlugin': 'Add Footer Sercices Link'
        },
    },
    'footer_links_qlinks': {
        'plugins': ('FooterPlugin',),
        'name': 'Footer Quick Links',
        'plugin_label': {
            'FooterPlugin': 'Add Footer Quick Link'
        },
    },
    'footer_links_support': {
        'plugins': ('FooterPlugin',),
        'name': 'Footer Support Plugin',
        'plugin_label': {
            'FooterPlugin': 'Add Footer Support Link'
        },
    },
    'footer_links_socials': {
        'plugins': ('FooterPlugin',),
        'name': 'Footer Socials Plugin',
        'plugin_label': {
            'FooterPlugin': 'Add Footer Socials'
        },
        'limits': {
            'global': 4,
        },
    },
    'header_links_socials': {
        'plugins': ('FooterPlugin',),
        'name': 'Header Socials Plugin',
        'plugin_label': {
            'FooterPlugin': 'Add Header Footer Links or Socials'
        },
        'limits': {
            'global': 4,
        },
    },
    'footer_links_apps': {
        'plugins': ('FooterPlugin',),
        'name': 'App Store Plugin',
        'plugin_label': {
            'FooterPlugin': 'Add Footer App Store Links'
        },
        'limits': {
            'global': 3,
        },
    },
}

# DATABASES = {
#     'default': {
#         'CONN_MAX_AGE': 0,
#         'ENGINE': 'django.db.backends.sqlite3',
#         'HOST': 'localhost',
#         'NAME': 'project_sharedfarm.db',
#         'PASSWORD': '',
#         'PORT': '',
#         'USER': ''
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'aps_shared_farm/db_local.cnf'),
            # Changed from db_live.cnf here
        },
    }
}
# without docker
# CELERY_BROKER_URL = "redis://0.0.0.0:6379"
# CELERY_RESULT_BACKEND = "redis://0.0.0.0:6379"
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)
META_SITE_PROTOCOL = 'http'  # set 'http' for non ssl enabled websites
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True  # django-meta 1.x+
META_USE_SCHEMAORG_PROPERTIES = True  # django-meta 2.x+
PARLER_DEFAULT_LANGUAGE_CODE = 'en'
PARLER_DEFAULT_ACTIVATE = True
PARLER_LANGUAGES = {
    1: (
        {'code': 'en', },
        {'code': 'bn', },
    ),
    'default': {
        'fallbacks': ['en'],
    }
}
AUTH_USER_MODEL = 'core.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'core.util.CustomAuthenticationBackend',  # to be able to login with email or phone
]

# TOKEN_EXPIRED_AFTER_SECONDS = 604800
TOKEN_EXPIRED_AFTER_SECONDS = 600
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
        'core.util.ExpiringTokenAuthentication',  # custom authentication class
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',

    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}
HMS_URL = 'http://shurjohms.com'
HMS_USERNAME = 'sharedfarm'
HMS_PASSWORD = 'AhXxdAlGdXPtoUZC'
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        # 'Basic': {
        #     'type': 'basic'
        # },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

from celery.schedules import crontab
import aps_shared_farm.tasks

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "aps_shared_farm.tasks.sample_task",
        "schedule": crontab(minute="*/1"),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info.jouthokhamar@gmail.com'  # sender's email-id
EMAIL_HOST_PASSWORD = 'tjvwvxgewxkmvjox'  # password associated with above email-id
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
FCM_API_KEY = "AAAAJOnYlbg:APA91bEhE71hXBtJf_FRYCTlIz1rPn0x0WaRlaoW5aZ8hujFMJ-arN5rF_dtgPdIp0492ciNMo0OsQnR8UxNO9_iicF7UeqtMf8jdjA8kwgAR58iZw6b4_5_Ds7LSFALW43eyU3dccCa"
