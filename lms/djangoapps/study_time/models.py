from django.conf import settings
from importlib import import_module
import django_comment_client.utils as utils
from courseware.courses import get_course_with_access
import pymongo
import logging
log = logging.getLogger("tracking")


class MongoRecordTimeStore(object):

    # TODO (cpennington): Enable non-filesystem filestores
    def __init__(self, host, db, collection, collection_page, collection_discussion, collection_portfolio, collection_external, collection_result_set,
                 port=27017, default_class=None, user=None, password=None, mongo_options=None, **kwargs):

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
        self.collection_discussion = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection_discussion]
        self.collection_portfolio = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection_portfolio]
        self.collection_external = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection_external]
        self.collection_result_set = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection_result_set]
        if user is not None and password is not None:
            self.collection.database.authenticate(user, password)
            self.collection_page.database.authenticate(user, password)
            self.collection_discussion.database.authenticate(user, password)
            self.collection_portfolio.database.authenticate(user, password)
            self.collection_external.database.authenticate(user, password)
            self.collection_result_set.database.authenticate(user, password)
        # Force mongo to report errors, at the expense of performance
        self.collection.safe = True
        self.collection_page.safe = True
        self.collection_discussion.safe = True
        self.collection_portfolio.safe = True
        self.collection_external.safe = True
        self.collection_result_set.safe = True

    def _find_one(self):
        item = self.collection.find_one(
            sort=[('date', pymongo.ASCENDING)],
        )
        return item

    def get_item(self, user_id, vertical_id, start_time):
        return self.collection.find_one(
            {
                'user_id': user_id,
                'vertical_id': vertical_id,
                'start_time': start_time
            }
        )

    def insert_item(self, item):
        self.collection.insert(item)

    def set_item(self, name, value, user_id, vertical_id, start_time):
        return self.collection.update(
            {
                'user_id': user_id,
                'vertical_id': vertical_id,
                'start_time': start_time
            },
            {
                '$set': {name: value}
            }
        )

    def get_page_item(self, user_id, vertical_id):
        return self.collection_page.find_one(
            {
                'user_id': user_id,
                'vertical_id': vertical_id
            }
        )

    def set_page_item(self, item, rdata):
        if rdata is not None:
            rdata['time'] = int(rdata['time']) + int(item['time'])
            if rdata['time'] >= 0:
                return self.collection_page.update(
                    {
                        'user_id': item['user_id'],
                        'vertical_id': item['vertical_id']
                    },
                    {
                        '$set': {'time': rdata['time']}

                    }
                )
        else:
            return self.collection_page.save(item)

    def return_page_items(self, user_id, skip=0, limit=5):
        r = []
        course_id = ''
        cur_course_id = ''
        results = self.collection_page.find({'user_id': user_id}).sort(
            [('course_name', pymongo.ASCENDING),
             ('sort_key', pymongo.ASCENDING)]).skip(skip).limit(limit)

        for data in results:
            data['_id'] = str(data['_id'])
            if course_id == '' or cur_course_id != data['course_id']:
                data['discussion_time'] = self.get_course_time(data['user_id'], data['course_id'], 'discussion')
                data['portfolio_time'] = self.get_course_time(data['user_id'], data['course_id'], 'portfolio')
                course = get_course_with_access(user_id, data['course_id'], 'load')
                data['external_time'] = course.external_course_time
                cur_course_id = data['course_id']
            r.append(data)
        return r

    def get_page_total(self, user_id):
        return self.collection_page.find({'user_id': user_id}).count()

    def get_course_time(self, user_id, course_id, type='', add_time_out=False):
        count_time = 0
        if type == 'courseware':
            if course_id is None:
                course_time = {}
                results = self.collection_page.find({'user_id': user_id})
                for data in results:
                    try:
                        course_time[data['course_id']]['time'] += int(data['time'])
                    except:
                        max_time = int(get_course_with_access(user_id, data['course_id'], 'load').maximum_units_time)
                        course_time[data['course_id']] = {'time': int(data['time']), 'max_time': max_time}

                for cid in course_time:
                    if course_time[cid]['time'] > course_time[cid]['max_time']:
                        course_time[cid]['time'] = course_time[cid]['max_time']
                    count_time += course_time[cid]['time']
            else:
                results = self.collection_page.find(
                    {
                        'user_id': user_id,
                        'course_id': course_id
                    }
                )
                for data in results:
                    count_time += int(data['time'])
                max_time = int(get_course_with_access(user_id, course_id, 'load').maximum_units_time)
                if add_time_out:
                    count_time = count_time - settings.PEPPER_SESSION_EXPIRY
                if count_time > max_time:
                    count_time = max_time
            return count_time

        elif type == 'discussion':
            if course_id is None:
                results = self.collection_discussion.find({'user_id': user_id})
            else:
                results = self.collection_discussion.find(
                    {
                        'user_id': user_id,
                        'course_id': course_id
                    }
                )
        elif type == 'portfolio':
            results = self.collection_portfolio.find({'user_id': user_id})
        for data in results:
            count_time += int(data['time'])
        return count_time

    def set_course_time(self, user_id, course_id, type, time):
        time = int(time)
        if type == 'discussion':
            results = self.collection_discussion.update(
                {
                    'user_id': user_id,
                    'course_id': course_id
                },
                {
                    '$inc': {'time': time}
                },
                True
            )
        elif type == 'portfolio':
            results = self.collection_portfolio.update(
                {
                    'user_id': user_id
                },
                {
                    '$inc': {'time': time}
                },
                True
            )
        return results

    def get_stats_time(self, user_id):
        course_time = self.get_course_time(user_id, None, 'courseware')
        discussion_time = self.get_course_time(user_id, None, 'discussion')
        portfolio_time = self.get_course_time(user_id, None, 'portfolio')
        return course_time, discussion_time, portfolio_time

    def set_external_time(self, user_id, course_id, type, external_id, weight):
        if type == 'combinedopenended':
            return self.collection_external.update(
                {
                    'user_id': user_id,
                    'course_id': course_id,
                    'external_id': external_id,
                    'type': type
                },
                {
                    '$set': {'weight': weight}
                },
                True
            )

    def del_external_time(self, user_id, course_id, type, external_id):
        return self.collection_external.remove(
            {
                'user_id': user_id,
                'course_id': course_id,
                'external_id': external_id,
                'type': type
            }
        )

    def get_external_time(self, user_id, course_id):
        count_weight = 0
        results = self.collection_external.find(
            {
                'user_id': user_id,
                'course_id': course_id
            }

        )
        for data in results:
            count_weight += int(data['weight'])
        course = get_course_with_access(user_id, course_id, 'load')
        return count_weight * int(course.external_course_time)

    def set_time_report_result(self, user_id, data):
        return self.collection_result_set.update(
            {
                'user_id': user_id
            },
            {
                '$set': {'data': data}
            },
            True
        )
    def get_time_report_result(self, user_id):
        result = self.collection_result_set.find_one({'user_id': user_id})
        if result is not None:
            return result['data']
        else:
            return []

def record_time_store():
    options = {}
    options.update(settings.RECORDTIMESTORE['OPTIONS'])
    return MongoRecordTimeStore(**options)
