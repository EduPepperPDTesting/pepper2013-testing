"""
MongoRemindStore backed by Mongodb.

"""

import pymongo
import sys
import logging
import copy
import datetime
from importlib import import_module
from django.conf import settings
from xmodule.modulestore.exceptions import ItemNotFoundError
log = logging.getLogger(__name__)
from bson import ObjectId
# TODO (cpennington): This code currently operates under the assumption that
# there is only one revision for each item. Once we start versioning inside the CMS,
# that assumption will have to change

class MongoRemindStore(object):

    # TODO (cpennington): Enable non-filesystem filestores
    def __init__(self, host, db, collection,collection_aid,port=27017, default_class=None,
                 user=None, password=None, mongo_options=None, **kwargs):

        super(MongoRemindStore, self).__init__(**kwargs)

        if mongo_options is None:
            mongo_options = {}

        self.collection = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection]
        self.collection_aid = pymongo.connection.Connection(
            host=host,
            port=port,
            tz_aware=True,
            **mongo_options
        )[db][collection_aid]

        if user is not None and password is not None:
            self.collection.database.authenticate(user, password)
            self.collection_aid.database.authenticate(user, password)
        # Force mongo to report errors, at the expense of performance
        self.collection.safe = True
        self.collection_aid.safe = True


    def _find_one(self):
        item = self.collection.find_one(
            sort=[('date', pymongo.ASCENDING)],
        )
        return item

    def return_items(self,user_id=-1,skip=0,limit=5):
        if user_id==-1:
            results = self.collection.find().skip(skip).limit(limit)
        else:
            results = self.collection.find({'$or':[{'user_id':str(user_id)},{'user_id':0}]}).sort("date",pymongo.DESCENDING).skip(skip).limit(limit)
            r=[]
            for data in results:
                data['_id']=str(data['_id'])
                try:
                    ismultiple=data['multiple']
                except:
                    ismultiple='false'
                    data['multiple']='false'
                if str(data['user_id'])=='0' or ismultiple=='true':
                    status = self.collection_aid.find_one({'user_id':str(user_id),'aid':data['_id']})
                    if status!=None:
                        data['activate'] = 'true'
                    else:
                        data['activate'] = 'false'
                r.append(data)
            return r
    def items_count(self,user_id=-1):
        #valid_interval = (datetime.datetime.now()-datetime.timedelta(4)).isoformat()
        #count = self.collection.find({'user_id':user_id,'activate':'false','date':{'$gt':str(valid_interval)}}).count()
        count = self.collection.find({'user_id':str(user_id),'activate':'false','multiple':{'$exists':False}}).count()
        results = self.collection.find({'$or':[{'user_id':str(user_id),'multiple':{'$exists':True}},{'user_id':0}]})
        for data in results:
            status = self.collection_aid.find_one({'user_id':user_id,'aid':str(data['_id'])})
            if status == None:
                count+=1
        return count
    def insert_item(self,item):
        self.collection.insert(item)

    def set_item(self,id,name,value,user_id,record_id,ismultiple,return_item=False):
        if return_item==True:
            self.collection.update({'_id':ObjectId(id)},{'$set':{name:value}})
            results = self.collection.find({'_id':ObjectId(id)})
            r=[]
            for data in results:
                r.append(data)
            return r
        else:
            if str(record_id) =='0' or ismultiple=='true':
                #return self.collection_aid.update({'aid':str(id),'user_id':user_id},{'$set':{'user_id':user_id}},True)
                return self.collection_aid.save({'aid':str(id),'user_id':user_id})
            else:
                return self.collection.update({'_id':ObjectId(id)},{'$set':{name:value}})
    def get_total(self,user_id):
        return self.collection.find({'$or':[{'user_id':str(user_id)},{'user_id':0}]}).count()


class MongoMessageStore(object):

    # TODO (cpennington): Enable non-filesystem filestores
    def __init__(self, host, db, collection,port=27017, default_class=None,
                 user=None, password=None, mongo_options=None, **kwargs):

        super(MongoMessageStore, self).__init__(**kwargs)

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


    def return_items(self,id_1,id_2,skip=0,limit=5):

        results = self.collection.find({'$or':[{'sender_id':id_1,'recipient_id':id_2},{'sender_id':id_2,'recipient_id':id_1},{'sender_id':id_1,'recipient_id':0},{'sender_id':id_2,'recipient_id':0}]}).sort("date",pymongo.DESCENDING).skip(skip).limit(limit)
        r=[]
        for data in results:
            data['_id']=str(data['_id'])
            r.append(data)
        return r

    def insert_item(self,item):
        self.collection.insert(item)

    def get_total(self,id_1,id_2):
        return self.collection.find({'$or':[{'sender_id':id_1,'recipient_id':id_2},{'sender_id':id_2,'recipient_id':id_1},{'sender_id':id_1,'recipient_id':0},{'sender_id':id_2,'recipient_id':0}]}).count()

class MongoChunksStore(object):

    # TODO (cpennington): Enable non-filesystem filestores
    def __init__(self, host, db, collection,port=27017, default_class=None,
                 user=None, password=None, mongo_options=None, **kwargs):

        super(MongoChunksStore, self).__init__(**kwargs)

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


    def return_vertical_item(self, user_id, vertical_id):
        results=self.collection.find({'user_id':user_id,'vertical_id':vertical_id})
        r=[]
        for data in results:
            data['_id']=str(data['_id'])
            r.append(data)
        return r

    def return_items(self, user_id, skip=0, limit=5):
        r=[]
        results=self.collection.find({'user_id':user_id}).sort([('courseTitle',pymongo.ASCENDING),('sort_key',pymongo.ASCENDING)]).skip(skip).limit(limit)
        for data in results:
            data['_id']=str(data['_id'])
            r.append(data)
        return r

    def save_item(self,item):
        count = self.collection.find({'user_id':item['user_id'],'vertical_id':item['vertical_id']}).count()
        if count>0:
            self.collection.update({'user_id':item['user_id'],'vertical_id':item['vertical_id']},{'$set':{'note':item['note']}})
        else:
            self.collection.insert(item)

    def delete_item(self, user_id, vertical_id):
        self.collection.remove({'user_id':user_id,'vertical_id':vertical_id})

    def get_total(self,user_id):
        return self.collection.find({'user_id':user_id}).count()


_REMINDSTORE = {}
_MESSAGESTORE = {}
_CHUNKSSTORE = {}

def load_function(path):
    """
    Load a function by name.

    path is a string of the form "path.to.module.function"
    returns the imported python object `function` from `path.to.module`
    """
    module_path, _, name = path.rpartition('.')
    return getattr(import_module(module_path), name)


def remindstore(name='default'):
    if name not in _REMINDSTORE:
        class_ = load_function(settings.REMINDSTORE['ENGINE'])
        options = {}
        options.update(settings.REMINDSTORE['OPTIONS'])
        if 'ADDITIONAL_OPTIONS' in settings.REMINDSTORE:
            if name in settings.REMINDSTORE['ADDITIONAL_OPTIONS']:
                options.update(settings.REMINDSTORE['ADDITIONAL_OPTIONS'][name])
        _REMINDSTORE[name] = class_(**options)

    return _REMINDSTORE[name]

def messagestore(name='default'):
    if name not in _MESSAGESTORE:
        class_ = load_function(settings.MESSAGESTORE['ENGINE'])
        options = {}
        options.update(settings.MESSAGESTORE['OPTIONS'])
        if 'ADDITIONAL_OPTIONS' in settings.MESSAGESTORE:
            if name in settings.MESSAGESTORE['ADDITIONAL_OPTIONS']:
                options.update(settings.MESSAGESTORE['ADDITIONAL_OPTIONS'][name])
        _MESSAGESTORE[name] = class_(**options)

    return _MESSAGESTORE[name]

def chunksstore(name='default'):
    if name not in _CHUNKSSTORE:
        class_ = load_function(settings.CHUNKSSTORE['ENGINE'])
        options = {}
        options.update(settings.CHUNKSSTORE['OPTIONS'])
        if 'ADDITIONAL_OPTIONS' in settings.CHUNKSSTORE:
            if name in settings.CHUNKSSTORE['ADDITIONAL_OPTIONS']:
                options.update(settings.CHUNKSSTORE['ADDITIONAL_OPTIONS'][name])
        _CHUNKSSTORE[name] = class_(**options)

    return _CHUNKSSTORE[name]

def num_sort(x):
    num = x.split(":")[0]
    r=0
    modulus=1000000
    if num.find(".")>0:
        digitalArr=num.split(".")
        for d in digitalArr:
            modulus/=100
            try: 
                r+=int(d)*modulus
            except:
                return r 
        return r
    else:
        return x