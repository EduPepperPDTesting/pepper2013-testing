import pymongo
import sys
sys.path.append('/home/tahoe/pepper/edx-platform/lms/djangoapps/reporting')
from aggregation_config  import *

class MongoReportingStore(object):

    def __init__(self, host='127.0.0.1', db='reporting', port=27018, user=None, password=None,
                 mongo_options=None, **kwargs):

        super(MongoReportingStore, self).__init__(**kwargs)

        if mongo_options is None:
            mongo_options = {}

        self.db = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db]

        if user is not None and password is not None:
            self.db.authenticate(user, password)

        self.collection = None

    def get_aggregate(self, collection, pipeline, disk=False):
        self.db.command({'aggregate': collection,
                         'pipeline': pipeline,
                         'allowDiskUse': disk})

school_year_collection = ['CourseView','AggregateTimerView']
school_year_list = ['','2016-2017','2015-2016','current','all']
reporting = MongoReportingStore()
for tmp in AggregationConfig:
    for tmp2 in school_year_list:
        collection = 'tmp_' + tmp + tmp2
        if tmp2 == '' or tmp2 == 'current':
            school_year = str({"$match":{"school_year":'current'}}) + ','
            if tmp in school_year_collection:
               school_year = str(['$$item.school_year', u'current'])
        elif tmp2 == 'all':
            school_year = ""
            if tmp in school_year_collection:
               school_year = str([1, 1])
        else:
            school_year = str({"$match":{"school_year":tmp2}}) + ','
            if tmp in school_year_collection:
               school_year = str(['$$item.school_year', tmp2])
        aggregate_query = AggregationConfig[str(tmp)]['allfieldquery'].replace(',,', ',').replace('{school_year}', school_year).replace('{collection}',collection).replace('\n', '').replace('\r', '')
        aggregate_query = eval(aggregate_query)
        reporting.get_aggregate(AggregationConfig[tmp]['collection'],aggregate_query)
