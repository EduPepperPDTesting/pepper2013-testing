from ..dev import *

# ========================================================================
# ========================================================================

MITX_FEATURES['ENABLE_SQL_TRACKING_LOGS'] = False

# ========================================================================
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
    'host': 'localhost',
    'db': 'xmodule',
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
        'host': 'localhost',
        'db': 'xcontent',
    }
}

USERSTORE = {
    'OPTIONS': {
        'host': 'localhost',
        'db': 'userstore',
        'user':None,
        'password':None,
    }
}

INSTALLED_APPS += (
    # Mongo perf stats
    'debug_toolbar_mongo',
    )

DEBUG_TOOLBAR_PANELS += (
   'debug_toolbar_mongo.panel.MongoDebugPanel',
   )

# ========================================================================
# ========================================================================
# ========================================================================
# ========================================================================
# ========================================================================

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
DEBUG = False
# PIPELINE=False 
# PIPELINE_ENABLED=False
STATIC_ROOT = ENV_ROOT / "staticfiles/lms"

# MITX_FEATURES['USE_DJANGO_PIPELINE']=True
