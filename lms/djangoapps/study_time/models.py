from django.conf import settings
from importlib import import_module
from bson import ObjectId
from django.views.decorators import csrf
import django_comment_client.utils as utils
from courseware.courses import get_course_with_access
from django.contrib.auth.models import User
import pymongo
import logging
log = logging.getLogger("tracking")


class MongoRecordTimeStore(object):

    # TODO (cpennington): Enable non-filesystem filestores
    def __init__(self, host, db, collection, collection_page, collection_course, port=27017, default_class=None,
                 user=None, password=None, mongo_options=None, **kwargs):

        super(MongoRecordTimeStore, self).__init__(**kwargs)

        if mongo_options is None:
            mongo_options = {}

        self.collection = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection]
        self.collection_page = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection_page]
        self.collection_course = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection_course]
        if user is not None and password is not None:
            self.collection.database.authenticate(user, password)
            self.collection_page.database.authenticate(user, password)
            self.collection_course.database.authenticate(user, password)
        # Force mongo to report errors, at the expense of performance
        self.collection.safe = True
        self.collection_page.safe = True
        self.collection_course.safe = True

    def _find_one(self):
        item = self.collection.find_one(
            sort=[('date', pymongo.ASCENDING)],
        )
        return item

    def get_item(self, user_id, vertical_id, start_time):
        return self.collection.find_one({'user_id': user_id, 'vertical_id': vertical_id, 'start_time': start_time})

    def insert_item(self, item):
        self.collection.insert(item)

    def set_item(self, name, value, user_id, vertical_id, start_time):
        return self.collection.update({'user_id': user_id, 'vertical_id': vertical_id, 'start_time': start_time}, {'$set': {name: value}})

    def get_page_item(self, user_id, vertical_id):
        return self.collection_page.find_one({'user_id': user_id, 'vertical_id': vertical_id})

    def set_page_item(self, item, rdata):
        if rdata is not None:
            rdata['time'] = int(rdata['time']) + int(item['time'])
            return self.collection_page.update({'user_id': item['user_id'], 'vertical_id': item['vertical_id']}, {'$set': {'time': rdata['time']}})
        else:
            return self.collection_page.save(item)

    def return_page_items(self, user_id, skip=0, limit=5):
        r = []
        course_id = ''
        cur_course_id = ''
        results = self.collection_page.find({'user_id': user_id}).sort([('course_name', pymongo.ASCENDING), ('sort_key', pymongo.ASCENDING)]).skip(skip).limit(limit)
        for data in results:
            data['_id'] = str(data['_id'])
            data['course_id'] = data['location'].split('/courseware/')[0]
            if course_id == '' or cur_course_id != data['course_id']:
                data['discussion_time'] = self.get_course_time(data['user_id'], data['course_id'], 'discussion')
                course = get_course_with_access(User.objects.get(id=user_id), data['course_id'], 'load')
                data['external_time'] = course.external_course_time
                cur_course_id = data['course_id']
            r.append(data)
        return r

    def get_page_total(self, user_id):
        return self.collection_page.find({'user_id': user_id}).count()

    def get_course_time(self, user_id, course_id, type):
        rdata = self.collection_course.find_one({'user_id': user_id, 'course_id': course_id})
        if rdata is None:
            return 0
        else:
            try:
                return rdata[type]
            except:
                return 0

    def set_course_time(self, user_id, course_id, type, time):
        return self.collection_course.update({'user_id': user_id, 'course_id': course_id}, {'$set': {type: time}}, True)


def recordTimeStore():
    options = {}
    options.update(settings.RECORDTIMESTORE['OPTIONS'])
    return MongoRecordTimeStore(**options)
