from django.db import models
from django.conf import settings
import pymongo
# from pymongo.objectid import ObjectId
import logging
# log = logging.getLogger("tracking")

class MongoDiscussionRating(object):

    def __init__(self, host, db, collection, port=27017, default_class=None, user=None, password=None,
                 mongo_options=None, **kwargs):

        super(MongoDiscussionRating, self).__init__(**kwargs)

        if mongo_options is None:
            mongo_options = {}

        self.collection = pymongo.connection.Connection(
                host=host,
                port=port,
                tz_aware=True,
                **mongo_options
        )[db][collection]

        if user is not None and password is not None:
            self.collection.database.authenticate(user, password)

        # Force mongo to report errors, at the expense of performance
        self.collection.safe = True
    
    def get_rating(self, thread_id, user_id):
        return self.collection.find_one(
                {
                    'comment_id':thread_id,
                    'user_id':user_id
                },
                {
                    'rating': 1,
                    '_id': 0
                }
        )

    def set_rating(self, thread_id, user_id, rating):
        return self.collection.update(
                {
                    'comment_id':thread_id,
                    'user_id':user_id
                },
                {
                    '$set':{'rating':rating}
                },
                True
        )

    def get_avg_rating(self, thread_id, user_id):
        return self.collection.find(
                {
                    'comment_id':thread_id
                },
                {
                    'rating': 1, '_id': 0
                }
        )
    
def discussion_rating_store():
    options =  {
        'collection': 'contents_rating',
    }
    options.update(settings.DISCUSSION_RATING_STORE['OPTIONS'])    
    return MongoDiscussionRating(**options)
