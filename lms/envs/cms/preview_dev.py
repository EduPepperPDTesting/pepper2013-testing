"""
Settings for the LMS that runs alongside the CMS on AWS
"""

# We intentionally define lots of variables that aren't used, and
# want to import all variables from base settings files
# pylint: disable=W0401, W0614

from .dev import *
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
        'ENGINE': 'xmodule.modulestore.draft.DraftModuleStore',
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB_W,
        'USER': MYSQL_USER_W,
        'PASSWORD': MYSQL_PASSWORD_W,
        'HOST': MYSQL_HOST_W,
        'PORT': MYSQL_PORT_W,
    },
    'read': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB_R,
        'USER': MYSQL_USER_R,
        'PASSWORD': MYSQL_PASSWORD_R,
        'HOST': MYSQL_HOST_R,
        'PORT': MYSQL_PORT_R,
    },
}

DATABASE_ROUTERS = ['dbrouter.RwSplittingRouter']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# PIPELINE=False 
# PIPELINE_ENABLED=False
STATIC_ROOT = ENV_ROOT / "staticfiles/lms"

# MITX_FEATURES['USE_DJANGO_PIPELINE']=True