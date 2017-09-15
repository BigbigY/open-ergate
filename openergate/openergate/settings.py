"""
Django settings for openergate project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h#cfy_f0&@s50!vojw&7wt2eqk!#c6t77y*no-awasa3^g!u=w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'user',
    'workflow',
    'djcelery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'openergate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+"/templates",],
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

WSGI_APPLICATION = 'openergate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# admin认证url
LOGIN_URL = '/user/login/'


#分页
PAGE_LIMIT = 20

import djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

#workflow
TASK_STATE_DICT = {0:'已撤销', 1:'新建中', 2:'已提交,等待审批', 3:'已审批', 4:'已处理', 5:'已结束'}
ACT_TYPE_DICT = {0:'撤销', 1:'同意', 2:'回退修改'}
CREATOR_ACT_TYPE_DICT = {0:'撤销', 1:'确认'}

#email
ADMINS = (
    ('wangyangyang', '962653920@qq.com'),
)
DEFAULT_FROM_EMAIL = SERVER_EMAIL = ''
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = '962653920'
EMAIL_HOST_PASSWORD = 'YY520it@'
EMAIL_PORT = 465
EMAIL_SUBJECT_PREFIX = '[workflow] '
#EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

#访问域名，用于发送邮件返回给用户访问本系统的地址
SYS_API = 'http://10.0.13.134:8000'

# LOG
LOGGING = {
'version': 1,
'disable_existing_loggers': True,
'formatters': {
    'standard': {
        'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  #日志格式
},
'filters': {
},
'handlers': {
    'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        'include_html': True,
        },
    'default': {
        'level':'DEBUG',
        'class':'logging.handlers.RotatingFileHandler',
        'filename':  os.path.join(BASE_DIR + '/logs/','all.log'),
        'maxBytes': 1024*1024*5,                  #文件大小
        'backupCount': 5,                         #备份份数
        'formatter':'standard',                   #使用哪种formatters日志格式
    },
    'error': {
        'level':'ERROR',
        'class':'logging.handlers.RotatingFileHandler',
        'filename':  os.path.join(BASE_DIR + '/logs/','error.log'),
        'maxBytes':1024*1024*5,
        'backupCount': 5,
        'formatter':'standard',
        },
    'console':{
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'standard'
    },
    'request_handler': {
        'level':'DEBUG',
        'class':'logging.handlers.RotatingFileHandler',
        'filename':  os.path.join(BASE_DIR + '/logs/','request.log'),
        'maxBytes': 1024*1024*5,
        'backupCount': 5,
        'formatter':'standard',
        },
    'scprits_handler': {
        'level':'DEBUG',
        'class':'logging.handlers.RotatingFileHandler',
        'filename':  os.path.join(BASE_DIR + '/logs/','script.log'),
        'maxBytes': 1024*1024*5,
        'backupCount': 5,
        'formatter':'standard',
        }
},
'loggers': {
    'django': {
        'handlers': ['default', 'console'],
        'level': 'INFO',
        'propagate': False
    },
    'django.request': {
        'handlers': ['request_handler'],
        'level': 'DEBUG',
        'propagate': False,
        },
    'scripts': {
        'handlers': ['scprits_handler'],
        'level': 'INFO',
        'propagate': False
    },
    'workflow': {
        'handlers': ['default','mail_admins'],
        'level': 'INFO',
        'propagate': True
    },
  }
}
