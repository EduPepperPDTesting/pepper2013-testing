"""
Settings for the LMS that runs alongside the CMS on AWS
"""

# We intentionally define lots of variables that aren't used, and
# want to import all variables from base settings files
# pylint: disable=W0401, W0614

from ..dev import *
from siteconf import *
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

REMINDSTORE = {
    'ENGINE': 'xmodule.remindstore.MongoRemindStore',
    'OPTIONS': {
        'db': 'remind',
        'collection': 'rmodule',
        'collection_aid': 'bulletin_status',
        'collection_status': 'rmodule_status',
        'host': MONGO_HOST,
        'port': MONGO_PORT,        
        'user':MONGO_USER,
        'password':MONGO_PASSWORD,
    }
}
MESSAGESTORE = {
    'ENGINE': 'xmodule.remindstore.MongoMessageStore',
    'OPTIONS': {
        'db': 'remind',
        'collection': 'message_board',
        'host': MONGO_HOST,
        'port': MONGO_PORT,        
        'user':MONGO_USER,
        'password':MONGO_PASSWORD,
    }
}
CHUNKSSTORE = {
    'ENGINE': 'xmodule.remindstore.MongoChunksStore',
    'OPTIONS': {
        'db': 'remind',
        'collection': 'chunks',
        'host': MONGO_HOST,
        'port': MONGO_PORT,        
        'user':MONGO_USER,
        'password':MONGO_PASSWORD,
    }
}
RECORDTIMESTORE = {
    'OPTIONS': {
        'db': 'assist',
        'collection': 'record_time',
        'collection_page': 'page_time',
        'collection_discussion': 'discussion_time',
        'collection_portfolio': 'portfolio_time',
        'host': MONGO_HOST,
        'port': MONGO_PORT,        
        'user':MONGO_USER,
        'password':MONGO_PASSWORD,
    }
}