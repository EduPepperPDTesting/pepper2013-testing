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


class DashboardFeedingStore(MongoBaseStore):
    def __init__(self, host, db, port,
                 user=None, password=None, mongo_options=None, **kwargs):
        # super(MongoBaseStore, self).__init__(**kwargs)
        MongoBaseStore.__init__(self, host, db, collection="dashboard_feeding", port=port, **kwargs)

    def dismiss(self, feeding_id, user_id):
        self.update({"_id": ObjectId(feeding_id)},
                    {"$push": {"dismiss": long(user_id)}}, False, True)

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

    def top_level_for_user(self, user_id, type=None, year=None, month=None, page_size=None, page=None, before=None, cond_ext={}):
        results = []

        # ** fields needed
        fields = {"__doc__": "$$ROOT", "keep_top": {"$and": [
            {"$eq": ["$type", "announcement"]},
            {"$gte": ["$expiration_date", before]}]}}
        fields["month"] = {"$month": '$date'}
        fields["year"] = {"$year": '$date'}

        # ** cond
        cond = {"$and": [{"$or": [{"__doc__.receivers": {"$in": [user_id]}},  # user is receiver
                                  {"__doc__.receivers": {"$elemMatch": {"$eq": 0}}}]},      # for every one
                         {"__doc__.dismiss": {"$nin": [user_id]}}  # not dismissed
                         ],
                "__doc__.sub_of": None}  # is top leve;

        cond.update(cond_ext)
        
        # *** filter cond
        if month:
            cond["month"] = int(month)

        if year:
            cond["year"] = int(year)

        if type:
            cond["__doc__.type"] = type

        # ** sort order
        so = OrderedDict([("keep_top", -1), ("__doc__.date", -1)])

        command = [{"$project": fields}, {"$match": cond}, {"$sort": so}]

        # ** paged
        if page is not None:
            command.append({"$skip": page * page_size})
        if page_size is not None:
            command.append({"$limit": page_size})

        cursor = self.aggregate(command)

        # cursor = self.find({"$or": [{"receivers": {"$elemMatch": {"$eq": 1}}},
        #                             {"receivers": {"$elemMatch": {"$eq": 0}}}],  # global
        #                     "sub_of": None})

        for p in cursor["result"]:
            # p = dict((k, p[k]) for k in ("_id", "content", "user_id"))
            p.update(p["__doc__"])
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

    def create(self, user_id, type, content, date, receivers=[], attachment_file=None,
               sub_of=None, top_level=None, expiration_date=None, **kwargs):
        data = {
            "type": type,
            "user_id": user_id,
            "content": content,
            "receivers": receivers,
            "date": date}

        data.update(kwargs)
        
        if attachment_file:
            data["attachment_file"] = attachment_file
            
        if sub_of:
            data["sub_of"] = ObjectId(sub_of)

        if top_level:
            data["top_level"] = ObjectId(top_level)

        if expiration_date:
            data["expiration_date"] = expiration_date

        return self.insert(data)

    def get_announcements(self, user_id, organization_type, **kwargs):
        kwargs["type"] = "announcement"
        kwargs["cond_ext"] = {"__doc__.organization_type": organization_type}
        return self.top_level_for_user(user_id, **kwargs)

    def get_posts(self, user_id, **kwargs):
        kwargs["type"] = "post"
        return self.top_level_for_user(user_id, **kwargs)

    def get_post_year_range(self, user_id):
        cond = {"$and": [{"$or": [{"__doc__.receivers": {"$in": [user_id]}},  # user is receiver
                                  {"__doc__.receivers": {"$elemMatch": {"$eq": 0}}}]},  # for every one
                         {"__doc__.dismiss": {"$nin": [user_id]}}  # not dismissed
                         ],
                "__doc__.sub_of": None,   # is top leve;
                "__doc__.type": "post"}

        so = OrderedDict([("__doc__.date", 1)])
        command = [{"$project": {"__doc__": "$$ROOT", "year": {"$year": "$date"}}}, {"$match": cond}, {"$sort": so}]

        cursor = self.aggregate(command)

        count = len(cursor["result"])

        if count:
            return cursor["result"][0]["year"], cursor["result"][count - 1]["year"]
        else:
            return None, None


def dashboard_feeding_store():
    options = {}
    options.update(settings.FEEDINGSTORE['OPTIONS'])
    return DashboardFeedingStore(**options)