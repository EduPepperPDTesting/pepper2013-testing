from django.db import models
from student.models import User
from django.conf import settings
import pymongo
import logging
import json
from reporting.run_config import RunConfig
log = logging.getLogger("tracking")


class Categories(models.Model):
    class Meta:
        db_table = 'reporting_categories'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    order = models.IntegerField(default=0)


class Reports(models.Model):
    class Meta:
        db_table = 'reporting_reports'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    distinct = models.BooleanField(blank=True, default=False)
    category = models.ForeignKey(Categories, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    access_level = models.CharField(blank=True, default='System', max_length=10)
    access_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)
    report_type = models.IntegerField(default=0)


class Views(models.Model):
    class Meta:
        db_table = 'reporting_views'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    collection = models.CharField(blank=False, max_length=255, db_index=True)


class ViewColumns(models.Model):
    class Meta:
        db_table = 'reporting_view_columns'
    name = models.CharField(blank=False, max_length=255, db_index=True)
    description = models.CharField(blank=True, null=True, max_length=255, db_index=False)
    column = models.CharField(blank=False, max_length=255, db_index=True)
    data_type = models.CharField(blank=True, max_length=4, default='text')
    view = models.ForeignKey(Views, on_delete=models.CASCADE)
    custom_filter = models.IntegerField(default=0)


class ViewRelationships(models.Model):
    class Meta:
        db_table = 'reporting_view_relationships'
    left = models.ForeignKey(ViewColumns, on_delete=models.PROTECT, related_name='viewrelationships_left')
    right = models.ForeignKey(ViewColumns, on_delete=models.PROTECT, related_name='viewrelationships_right')


class ReportViews(models.Model):
    class Meta:
        db_table = 'reporting_report_views'
    view = models.ForeignKey(Views, on_delete=models.CASCADE)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False, null=False, default=0)


class ReportViewColumns(models.Model):
    class Meta:
        db_table = 'reporting_report_view_columns'
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    column = models.ForeignKey(ViewColumns, on_delete=models.PROTECT)
    order = models.IntegerField(default=0)


class ReportFilters(models.Model):
    class Meta:
        db_table = 'reporting_report_filters'
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    conjunction = models.CharField(blank=True, null=True, max_length=3)
    column = models.ForeignKey(ViewColumns, on_delete=models.PROTECT)
    value = models.CharField(blank=False, max_length=255)
    operator = models.CharField(blank=False, max_length=2)
    order = models.IntegerField(blank=False, null=False, default=0)

class ReportMatrixColumns(models.Model):
    class Meta:
        db_table = 'reporting_matrix_columns'
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    column_headers = models.IntegerField(blank=False, null=False)
    row_headers = models.IntegerField(blank=False, null=False)
    aggregate_data = models.IntegerField(blank=False, null=False)
    aggregate_type = models.IntegerField(default=0)


class MongoReportingStore(object):

    def __init__(self, host, db, port=27018, user=None, password=None,
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

    def set_collection(self, collection):
        self.collection = self.db[collection]

    # TODO: see about updating pymongo so this will work.
    # def get_collections(self):
    #     return self.db.collection_names()

    # TODO: test this code to make sure it works as expected.
    # def get_columns(self, collection):
    #     self.set_collection(collection)
    #     return reduce(
    #         lambda all_keys, rec_keys: all_keys | set(rec_keys),
    #         map(lambda d: d.keys(), self.collection.find()),
    #         set()
    #     )
    def insert_datas(self,datas,collection):
        self.set_collection(collection)
        for index,val in enumerate(datas):
            self.collection.insert(val)
        return True
    def update_data(self,db_filter,data,collection):
        self.set_collection(collection)
        data = {"$set":data}
        return self.collection.update(db_filter,data,True)

    def get_datas(self,collection,db_filter={},db_sort=['_id',1]):
        self.set_collection(collection)
        return self.collection.find(db_filter).sort(db_sort[0],db_sort[1])

    def get_page(self, collection, start, num, db_filter={}, db_sort=['$natural', 1, 0]):
        self.set_collection(collection)
        if db_sort[0] != '$natural' and db_sort[2] == 1:
            return self.get_page_int_sort(collection, db_filter, db_sort, start, num)
        else:
            return self.collection.find(db_filter).sort(db_sort[0], db_sort[1]).skip(start).limit(num)

    def get_matrix_page(self, collection, start, num, db_sort, db_filter={}):
        self.set_collection(collection)
        return self.collection.find(db_filter).sort(db_sort[0], db_sort[1]).skip(start).limit(num)

    def get_count(self, collection, db_filter={}):
        self.set_collection(collection)
        return self.collection.find(db_filter).count()

    def del_collection(self, collection):
        self.set_collection(collection)
        self.collection.drop()

    def get_collection_stats(self, collection):
        fun = 'function(){return db.' + collection + '.stats()}'
        self.db.system_js.collection_stats = fun
        return self.db.system_js.collection_stats()

    def get_aggregate(self, collection, pipeline, disk=False):
        return self.db.command({'aggregate': collection,
                         'pipeline': pipeline,
                         'allowDiskUse': disk})

    def get_page_int_sort(self, collection, db_filter, db_sort, start, num):
        field = db_sort[0]
        order = db_sort[1]
        db_filter = json.dumps(db_filter)
        a = 'c1'
        b = 'c2'
        if order < 0:
            a = 'c2'
            b = 'c1'
        val = 'return db.' + collection + '.find(' + db_filter + ').toArray()\
        .sort(function(c1, c2){return {a}.' + field + ' - {b}.' + field + '})'
        val = val.replace('{a}', a).replace('{b}', b)
        cursor = list(self.db.eval(val))
        return cursor[start:start + num]

    def update_user_view(self, user):
        data = get_user_data(user)
        self.update_data({'school_year': 'current','user_id':int(user.id)}, data,RunConfig["new_user_info"]["collection"])

    def insert_user_view(self, user):
        collection = "new_user_info"
        rs.del_collection(collection)
        rs.set_collection(collection)
        data = get_user_data(user)
        rs.collection.insert(data)
        query = eval(RunConfig[collection]["query"].replace('\n', '').replace('\r', '').replace(',,', ','))
        result = rs.get_aggregate(collection,query)
        for tmp in result['result']:
            rs.set_collection(RunConfig[collection]["collection"])
            rs.collection.insert(tmp)

    def delete_user_view(self, ids):
        collection = "user_info"
        rs.set_collection(RunConfig[collection]["collection"])
        for tmp in ids:
            rs.collection.remove({"user_id":int(tmp),"school_year":"current"})


    def get_user_data(user):
        data = {'email':user.email, 'user_id': user.id, 'user_name': user.username}
        try:
            data['first_name'] = user.first_name
        except:
            data['first_name'] = ""
        try:
            data['last_name'] = user.last_name
        except:
            data['last_name'] = ""
        try:
            data['district_id'] = user.profile.district.id
            data['district'] = user.profile.district.name
            data['state_id'] = user.profile.district.state.id
            data['state'] = user.profile.district.state.name
        except:
            data['district_id'] = ""
            data['district'] = ""
            data['state_id'] = ""
            data['state'] = ""
        try:
            data['school_id'] = user.profile.school.id
            data['school'] = user.profile.school.name
        except:
            data['school_id'] = ""
            data['school'] = ""
        try:
            data['subscription_status'] = user.profile.subscription_status
        except:
            data['subscription_status'] = ""
        try:
            data['cohort_id'] = user.profile.cohort.id
            data["cohort"] = user.profile.cohort.code
        except:
            data['cohort_id'] = ""
            data["cohort"] = ""
        try:
            data['activate_date'] = user.profile.activate_date.strftime('%b-%d-%y %H:%M:%S')
        except:
            data['activate_date'] = ""

        return data

def reporting_store():
    options = {}
    options.update(settings.REPORTINGSTORE['OPTIONS'])
    return MongoReportingStore(**options)
