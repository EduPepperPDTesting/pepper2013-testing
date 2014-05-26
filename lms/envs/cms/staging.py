from ..dev import *

import os,sys
sys.path.append("..") # => /home/tahoe/edx_all
from siteconf import *


# ========================================================================
MITX_FEATURES['ENABLE_SQL_TRACKING_LOGS'] = False

# ========================================================================
MITX_FEATURES['AUTH_USE_MIT_CERTIFICATES'] = False

SUBDOMAIN_BRANDING['edge'] = 'edge'
SUBDOMAIN_BRANDING['preview.edge'] = 'edge'
VIRTUAL_UNIVERSITIES = ['edge']

# Turn off this flag because it will render 'Edit / QA' links for all instructor viewings of
# modules. Since - for now - those links point to github (for XML based authoring), it seems broken
# to people using it. Once we can update those links to properly link back to Studio,
# then we can turn this flag back on, as well as enabling in aws.py configurations.
MITX_FEATURES['ENABLE_LMS_MIGRATION'] = False

META_UNIVERSITIES = {}

modulestore_options = {
    'default_class': 'xmodule.raw_module.RawDescriptor',
    'db': 'xmodule',
    'host': MONGO_HOST,
    'port': MONGO_PORT,       
    'user':MONGO_USER,
    'password':MONGO_PASSWORD,
    'collection': 'modulestore',
    'fs_root': DATA_DIR,
    'render_template': 'mitxmako.shortcuts.render_to_string',
}

MODULESTORE = {
    'default': {
        'ENGINE': 'xmodule.modulestore.mongo.MongoModuleStore',
        'OPTIONS': modulestore_options
    },
}

CONTENTSTORE = {
    'ENGINE': 'xmodule.contentstore.mongo.MongoContentStore',
    'OPTIONS': {
        'db': 'xcontent',
        'host': MONGO_HOST,
        'port': MONGO_PORT,           
        'user':MONGO_USER,
        'password':MONGO_PASSWORD,        
    }
}

USERSTORE = {
    'OPTIONS': {
        'db': 'userstore',
        'host': MONGO_HOST,
        'port': MONGO_PORT,        
        'user':MONGO_USER,
        'password':MONGO_PASSWORD,
    }
}

INSTALLED_APPS += (
    # Mongo perf stats
    'debug_toolbar_mongo',
    )

DEBUG_TOOLBAR_PANELS += (
   'debug_toolbar_mongo.panel.MongoDebugPanel',
   )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# PIPELINE=False 
# PIPELINE_ENABLED=False
STATIC_ROOT = ENV_ROOT / "staticfiles/lms"

# MITX_FEATURES['USE_DJANGO_PIPELINE']=True
