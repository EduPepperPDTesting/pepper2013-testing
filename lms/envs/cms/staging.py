from ..dev import *
from siteconf import *
import sys

sys.path.append("..")  # => /home/tahoe/edx_all

sys.path.append(PROJECT_ROOT + "/sso/")

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
    'db': MONGO_DB_XMODULE,
    'host': MONGO_HOST,
    'port': MONGO_PORT,
    'user': MONGO_USER,
    'password': MONGO_PASSWORD,
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
        'db': MONGO_DB_XCONTENT,
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}

USERSTORE = {
    'OPTIONS': {
        'db': MONGO_DB_USERSTORE,
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
REMINDSTORE = {
    'ENGINE': 'xmodule.remindstore.MongoRemindStore',
    'OPTIONS': {
        'db': MONGO_DB_REMIND,
        'collection': 'rmodule',
        'collection_aid': 'bulletin_status',
        'collection_status': 'rmodule_status',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
MESSAGESTORE = {
    'ENGINE': 'xmodule.remindstore.MongoMessageStore',
    'OPTIONS': {
        'db': MONGO_DB_REMIND,
        'collection': 'message_board',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
MYACTIVITYSTORE = {
    'ENGINE': 'xmodule.remindstore.MongoMyActivityStore',
    'OPTIONS': {
        'db': MONGO_DB_REMIND,
        'collection': 'my_activity',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
MYACTIVITYSTATICSTORE = {
    'ENGINE': 'xmodule.remindstore.MongoMyActivityStaticStore',
    'OPTIONS': {
        'db': MONGO_DB_REMIND,
        'collection': 'my_activity_static',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
CHUNKSSTORE = {
    'ENGINE': 'xmodule.remindstore.MongoChunksStore',
    'OPTIONS': {
        'db': MONGO_DB_REMIND,
        'collection': 'chunks',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
DISCUSSION_RATING_STORE = {
    'OPTIONS': {
        'db': MONGO_DB_DISCUSS,
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
RECORDTIMESTORE = {
    'OPTIONS': {
        'db': MONGO_DB_ASSIST,
        'collection': 'record_time',
        'collection_page': 'page_time',
        'collection_discussion': 'discussion_time',
        'collection_portfolio': 'portfolio_time',
        'collection_external': 'external_time',
        'collection_result_set': 'result_set',
        'collection_adjustment': 'adjustment_time',
        'collection_aggregate': 'aggregate_time',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
VIEWCOUNTERSTORE = {
    'OPTIONS': {
        'db': MONGO_DB_ASSIST,
        'collection': 'view_counter',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
POLLSTORE = {
    'OPTIONS': {
        'db': MONGO_DB_ASSIST,
        'collection_poll': 'polls',
        'collection_answers': 'poll_answers',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
SITESETTINGSSTORE = {
    'OPTIONS': {
        'db': MONGO_DB_ASSIST,
        'collection': 'site_settings',
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'user': MONGO_USER,
        'password': MONGO_PASSWORD,
    }
}
REPORTINGSTORE = {
    'OPTIONS': {
        'db': MONGO3_DB_REPORTING,
        'host': MONGO3_HOST,
        'port': MONGO3_PORT,
        'user': MONGO3_USER,
        'password': MONGO3_PASSWORD,
    }
}

FEEDINGSTORE = {
    'OPTIONS': {
        'db': MONGO3_DB_FEEDING,
        'host': MONGO3_HOST,
        'port': MONGO3_PORT,
        'user': MONGO3_USER,
        'password': MONGO3_PASSWORD
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

# DATABASE_ROUTERS = ['dbrouter.RwSplittingRouter']

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# PIPELINE = False
# PIPELINE_ENABLED = False
STATIC_ROOT = ENV_ROOT / "staticfiles/lms"

# MITX_FEATURES['USE_DJANGO_PIPELINE']=True


SESSION_SAVE_EVERY_REQUEST = True

# -----------------------------------------------------------------------------
# disable django debug toolbars
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INSTALLED_APPS = tuple([app for app in INSTALLED_APPS if not app.startswith('debug_toolbar')])
MIDDLEWARE_CLASSES = tuple([mcl for mcl in MIDDLEWARE_CLASSES if not mcl.startswith('debug_toolbar')])
