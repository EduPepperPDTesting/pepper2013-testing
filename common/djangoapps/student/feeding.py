from django.conf import settings
from importlib import import_module
# import django_comment_client.utils as utils
# from courseware.courses import get_course_with_access
import pymongo
import logging

from pytz import UTC
import datetime

log = logging.getLogger("tracking")
from bson import ObjectId
from collections import OrderedDict


class MongoBaseStore(object):
    def __init__(self, host, db, port, collection="",
                 default_class=None, user=None, password=None, mongo_options=None, **kwargs):

        if mongo_options is None:
            mongo_options = {}

        self.collection = pymongo.connection.Connection(
            host=host, port=port, tz_aware=True, **mongo_options
        )[db][collection]

        if user is not None and password is not None:
            self.collection.database.authenticate(user, password)

        self.collection.safe = True

    # def _find_one(self):
    #     item = self.collection.find_one(
    #         sort=[('date', pymongo.ASCENDING)],
    #     )
    #     return item

    def get_item(self, cond):
        return self.collection.find_one(cond)

    def insert(self, item):
        return self.collection.insert(item)

    def find(self, cond):
        return self.collection.find(cond)

    def find_one(self, cond):
        return self.collection.find_one(cond)

    def aggregate(self, cond):
        return self.collection.aggregate(cond)

    def update(self, cond, item, upsert=False, multi=True):
        self.collection.update(cond, item, upsert=upsert, multi=multi)

    def remove(self, cond):
        self.collection.remove(cond)

    def set_item(self, name, value, user_id, vertical_id, start_time):
        return self.collection.update({
                'user_id': user_id,
                'vertical_id': vertical_id,
                'start_time': start_time
            },
            {'$set': {name: value}})


class DashboardFeedingStore(MongoBaseStore):
    def __init__(self, host, db, port,
                 user=None, password=None, mongo_options=None, **kwargs):
        # super(MongoBaseStore, self).__init__(**kwargs)
        MongoBaseStore.__init__(self, host, db, collection="dashboard_feeding", port=port, **kwargs)

    def get_likes(self, feeding_id):
        doc = self.find_one({"_id": ObjectId(feeding_id)})
        return doc["likes"] if doc else []

    def get_feeding(self, feeding_id):
        doc = self.find_one({"_id": ObjectId(feeding_id)})
        return doc

    def is_like(self, feeding_id, user_id):
        return self.find({"_id": ObjectId(feeding_id), "likes": {"$elemMatch": {"user_id": long(user_id)}}}).count()

    def add_like(self, feeding_id, user_id, date):
        # $addToSet == "insert if not exists" else use $push
        self.remove_like(feeding_id, user_id)
        self.update({"_id": ObjectId(feeding_id)},
                    {"$push": {"likes": {"user_id": long(user_id), "date": date}}}, False, True)

    def remove_like(self, feeding_id, user_id):
        self.update({"_id": ObjectId(feeding_id)},
                    {"$pull": {"likes": {"user_id": long(user_id)}}}, False, True)

    def top_level_for_user(self, user_id, type=None, year=None, month=None, page_size=None, page=None, before=None):
        results = []

        # ** fields needed
        fields = {"date": 1, "content": 1, "user_id": 1, "expiration_date": 1,
                  "images": 1, "type": 1, "sub_of": 1, "receivers": 1, "likes": 1}
        fields["month"] = {"$month": '$date'}
        fields["year"] = {"$year": '$date'}


        # ** cond
        cond = {"$and": [{"$or": [{"receivers": {"$elemMatch": {"$eq": user_id}}},  # user is receiver
                                  {"receivers": {"$elemMatch": {"$eq": 0}}}]},      # for every one
                         {"$or": [{"expiration_date": {"$gte": before}},  # before expiration
                                  {"expiration_date": {"$eq": None}       # expiration not setted
                                   }]}],
                "sub_of": None}  # is top leve;

        # *** filter cond
        if month:
            cond["month"] = int(month)

        if year:
            cond["year"] = int(year)

        if type:
            cond["type"] = type

        # ** sort order
        so = OrderedDict([("type", 1), ("date", -1)])

        command = [{"$project": fields}, {"$match": cond}, {"$sort": so}]

        # ** paged
        if page > 0:
            command.append({"$skip": page * page_size})
        command.append({"$limit": page_size})

        cursor = self.aggregate(command)

        # cursor = self.find({"$or": [{"receivers": {"$elemMatch": {"$eq": 1}}},
        #                             {"receivers": {"$elemMatch": {"$eq": 0}}}],  # global
        #                     "sub_of": None})

        for p in cursor["result"]:
            # p = dict((k, p[k]) for k in ("_id", "content", "user_id"))
            results.append(p)
        return results

    def remove_feeding(self, feeding_id):
        self.remove({"_id": ObjectId(feeding_id)})
        self.remove({"sub_of": ObjectId(feeding_id)})

    def get_sub(self, feeding_id):
        results = []
        cursor = self.find({"sub_of": ObjectId(feeding_id)})
        for p in cursor:
            results.append(p)
        return results

    def get_all_sub(self, feeding_id):
        results = []
        cursor = self.find({"top_level": ObjectId(feeding_id)})
        for p in cursor:
            results.append(p)
        return results

    def create(self, user_id, type, content, date, receivers=[],
               sub_of=None, top_level=None, expiration_date=None, images=None):
        data = {"type": type, "user_id": user_id, "content": content, "receivers": receivers, "date": date}

        if sub_of:
            data["sub_of"] = ObjectId(sub_of)

        if top_level:
            data["top_level"] = ObjectId(top_level)

        if expiration_date:
            data["expiration_date"] = expiration_date

        if images:
            data["images"] = images

        return self.insert(data)


def dashboard_feeding_store():
    options = {}
    options.update(settings.FEEDINGSTORE['OPTIONS'])
    return DashboardFeedingStore(**options)
