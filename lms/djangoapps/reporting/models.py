from django.db import models
from student.models import User
from django.conf import settings
import pymongo
import logging
import json
from reporting.run_config import RunConfig
from student.models import User, CourseEnrollment
from courseware.models import StudentModule
from xmodule.course_module import CourseDescriptor
from xmodule.modulestore.django import modulestore
from administration.models import PepRegTraining, PepRegInstructor, PepRegStudent
from student.models import District, School, State
log = logging.getLogger("tracking")

def course_from_id(course_id):
    """Return the CourseDescriptor corresponding to this course_id"""
    course_loc = CourseDescriptor.id_to_location(course_id)
    return modulestore().get_instance(course_id, course_loc)

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
    def remove_data(self,db_filter,collection):
        self.set_collection(collection)
        return self.collection.remove(db_filter)

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

    def get_user_course_data(self, user_id, course_id):
        user = User.objects.get(pk=user_id)
        data = {'course_id': course_id, 'user_id': int(user.id), 'state_id': user.profile.district.state.id, 'district_id': user.profile.district.id}
        try:
            data['school_id'] = user.profile.school.id
        except:
            data['school_id'] = ""
        enroll = CourseEnrollment.objects.get(user=user, course_id=course_id)
        data['is_active'] = int(enroll.is_active)
        data['created'] = enroll.created.strftime('%Y-%m-%d')
        return data

    def get_user_data(self, user_id):
        user = User.objects.get(pk=user_id)
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
            data['activate_date'] = user.profile.activate_date.strftime('%Y-%m-%d')
        except:
            data['activate_date'] = ""

        return data

    def get_user_course_date1(self, user_id, course_id):
        course_data = StudentModule.objects.get(student=user_id,course_id=course_id,module_type="course")
        data = course_data.__dict__
        data['state'] = eval(data['state'].replace('false', 'False').replace('true', 'True').replace('null', 'None'))
        data['created'] = data['created'].strftime('%Y-%m-%d')
        data['modified'] = data['modified'].strftime('%Y-%m-%d')
        data['c_course_id'] = data['course_id']
        data['c_student_id'] = data['student_id']
        data['module_id'] = data['module_state_key']
        data.pop('_state')
        data.pop('module_state_key')
        data.pop('id')
        return data

    def get_course_data(self, course_id):
        course_data = course_from_id(course_id)
        data = {}
        try:
            data["course_number"] = str(course_data.display_coursenumber)
        except:
            data["course_number"] = ""
        try:
            data["course_name"] = course_data.display_name
        except:
            data["course_name"] = ""
        try:
            data["organization"] = str(course_data.display_organization)
        except:
            data["organization"] = ""
        try:
            data["start_date"] = course_data.start.strftime('%Y-%m-%d')
        except:
            data["start_date"] = ""
        try:
            data["end_date"] = course_data.end.strftime('%Y-%m-%d')
        except:
            data["end_date"] = ""
        try:
            data["course_run"] = course_data.org
        except:
            data["course_run"] = ""
        return data



def reporting_store(view=None):
    options = {}
    options.update(settings.REPORTINGSTORE['OPTIONS'])
    if view == 'UserInfo':
        return UserInfo(**options)
    elif view == 'DiscussionTime':
        return DiscussionTime(**options)
    elif view == 'CourseTime':
        return CourseTime(**options)
    elif view == 'PortfolioTime':
        return PortfolioTime(**options)
    elif view == 'ExternalTime':
        return ExternalTime(**options)
    elif view == 'AdjustmentTime':
        return AdjustmentTime(**options)
    elif view == 'PdTime':
        return PdTime(**options)
    elif view == 'StudentCourseenrollment':
        return StudentCourseenrollment(**options)
    elif view == 'CoursewareStudentmodule':
        return CoursewareStudentmodule(**options)
    elif view == 'UserCourseProgress':
        return UserCourseProgress(**options)
    elif view == 'ModuleStore':
        return ModuleStore(**options)
    elif view == 'PepregTraining':
        return PepregTraining(**options)
    elif view == 'PepregStudent':
        return PepregStudent(**options)    
    else:
        return MongoReportingStore(**options)

class UserInfo(MongoReportingStore):
        
    def report_update_data(self, user_id):
        affected_collection = ['user_info', 'UserView', 'UserCourseView']
        data = self.get_user_data(user_id)
        data = {"$set": data}
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "user_info":
                db_filter = {'user_id': int(user_id)}
                self.collection.update(db_filter, data, False)
            elif tmp == "UserView":
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data, False)
            elif tmp =="UserCourseView":
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data, False, multi=True)

    def report_insert_data(self, user_id):
        affected_collection = ['user_info', 'UserView']
        data = self.get_user_data(user_id)
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "user_info":
                self.collection.insert(data)
            elif tmp == "UserView":
                data['current_course'] = 0
                data['complete_course'] = 0
                data['course_time'] = 0
                data['external_time'] = 0
                data['discussion_time'] = 0
                data['portfolio_time'] = 0
                data['pd_time'] = 0
                data['collaboration_time'] = 0
                data['total_time'] = 0
                data['school_year'] = "current"
                self.collection.insert(data)

    def report_remove_data(self, user_id):
        affected_collection = ['user_info', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == 'user_info':
                db_filter = {'user_id': int(user_id)}
            else:
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
            self.collection.remove(db_filter)

class DiscussionTime(MongoReportingStore):

    def report_update_data(self, user_id, course_id, time):
        affected_collection = ['discussion_time', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "discussion_time":
                data = {'$inc': {'time': time}}
                db_filter = {'user_id': int(user_id), 'course_id': course_id}
                self.collection.update(db_filter, data, True)
            elif tmp == "UserView":
                data = {'$inc': {'total_time': time, 'discussion_time': time, 'collaboration_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                data = {'$inc': {'total_time': time, 'discussion_time': time, 'collaboration_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id), 'course_id': course_id}
                self.collection.update(db_filter, data)

class CourseTime(MongoReportingStore):

    def report_update_data(self, user_id, course_id, time):
        affected_collection = ['course_time', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "course_time":
                data = {'$inc': {'time': time}}
                db_filter = {'user_id': int(user_id), 'course_id': course_id}
                self.collection.update(db_filter, data, True)
            elif tmp == "UserView":
                data = {'$inc': {'total_time': time, 'course_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                data = {'$inc': {'total_time': time, 'course_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id), 'course_id': course_id}
                self.collection.update(db_filter, data)

class PortfolioTime(MongoReportingStore):

    def report_update_data(self, user_id, time):
        affected_collection = ['portfolio_time', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "portfolio_time":
                data = {'$inc': {'time': time}}
                db_filter = {'user_id': int(user_id)}
                self.collection.update(db_filter, data, True)
            elif tmp == "UserView":
                data = {'$inc': {'total_time': time, 'portfolio_time': time, 'collaboration_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                data = {'$inc': {'total_time': time, 'portfolio_time': time, 'collaboration_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data, multi=True)

class ExternalTime(MongoReportingStore):

    def report_update_data(self, user_id, course_id, time, external_id = "", weight = ""):
        affected_collection = ['t_external_time', 'external_time', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "external_time":
                data = {'$inc': {'r_time': time}}
                db_filter = {'user_id': int(user_id), 'course_id': course_id}
                self.collection.update(db_filter, data, True)
            elif tmp == "t_external_time":
                if external_id:
                    data = {'$set': {'weight': weight}}
                    db_filter = {'user_id': user_id, 'course_id': course_id, 'external_id': external_id, 'type': 'combinedopenended'}
                    self.collection.update(db_filter, data, True)
                else:
                    continue
            elif tmp == "UserView":
                data = {'$inc': {'total_time': time, 'external_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                data = {'$inc': {'total_time': time, 'external_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id), 'course_id': course_id}
                self.collection.update(db_filter, data)

class AdjustmentTime(MongoReportingStore):

    def report_update_data(self, user_id, course_id, time, type):
        affected_collection = ['adjustment_time', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "adjustment_time":
                if type == 'portfolio':
                    data = {'$inc': {'time': time}}
                    db_filter = {'user_id': int(user_id), 'type': type}
                elif type == 'discussion' or type == "external" or type == "courseware":
                    data = {'$inc': {'time': time}}
                    db_filter = {'user_id': int(user_id), 'course_id': course_id, 'type': type}
                self.collection.update(db_filter, data, True)
            elif tmp == "UserView":
                if type == 'portfolio':
                    data = {'$inc': {'total_time': time, 'portfolio_time': time, 'collaboration_time': time}}
                elif type == 'discussion':
                    data = {'$inc': {'total_time': time, 'discussion_time': time, 'collaboration_time': time}}
                elif type == 'external':
                    data = {'$inc': {'total_time': time, 'external_time': time}}
                elif type == 'courseware':
                    data = {'$inc': {'total_time': time, 'course_time': time}}   
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                if type == 'portfolio':
                    data = {'$inc': {'total_time': time, 'portfolio_time': time, 'collaboration_time': time}}
                    db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                    self.collection.update(db_filter, data, multi=True)
                elif type == 'discussion':
                    data = {'$inc': {'total_time': time, 'discussion_time': time, 'collaboration_time': time}}
                    db_filter = {'school_year': 'current', 'user_id': int(user_id), 'course_id': course_id}
                    self.collection.update(db_filter, data)
                elif type == 'external':
                    data = {'$inc': {'total_time': time, 'external_time': time}}
                    db_filter = {'school_year': 'current', 'user_id': int(user_id), 'course_id': course_id}
                    self.collection.update(db_filter, data)
                elif type == 'courseware':
                    data = {'$inc': {'total_time': time, 'course_time': time}}
                    db_filter = {'school_year': 'current', 'user_id': int(user_id), 'course_id': course_id}
                    self.collection.update(db_filter, data)

class PdTime(MongoReportingStore):

    def report_update_data(self, user_id, credit):
        affected_collection = ['pd_time', 'UserView', 'UserCourseView']
        time = 3600 * int(credit)
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "pd_time":
                data = {'$inc': {'credit': time}}
                db_filter = {'user_id': int(user_id)}
                self.collection.update(db_filter, data, True)
            elif tmp == "UserView":
                data = {'$inc': {'total_time': time, 'pd_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                data = {'$inc': {'total_time': time, 'pd_time': time}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data, multi=True)

class StudentCourseenrollment(MongoReportingStore):

    def report_update_data(self, user_id, course_id, is_active = 1):
        affected_collection = ['student_courseenrollment', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "student_courseenrollment":
                if is_active == 1:
                    data = self.get_user_course_data(user_id, course_id)
                    db_filter = {'course_id': course_id, 'user_id': int(user_id)}
                    self.collection.update(db_filter, data, True)
                else:
                    db_filter = {'course_id': course_id, 'user_id': int(user_id)}
                    self.collection.remove(db_filter)
                    continue
            elif tmp == "UserView":
                data = {'$inc': {'current_course': is_active}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                if is_active == 1:
                    data = self.get_insert_data(int(user_id), course_id)
                    self.collection.insert(data)
                else:
                    db_filter = {'course_id': course_id, 'user_id': int(user_id), 'school_year': 'current'}
                    self.collection.remove(db_filter)

    def get_insert_data(self, user_id, course_id):
        user_data = self.get_user_data(user_id)
        course_data = self.get_course_data(course_id)
        user_course_data = self.get_user_course_data(user_id, course_id)
        user_data.update(course_data)
        data = {}
        data["enrollment_date"] = user_course_data['created']
        data["complete_date"] = ""
        data["portfolio_url"] = "/courses/" + course_id + "portfolio/about_me/" + str(user_id)
        data["course_time"] = 0
        data["external_time"] = 0
        data["discussion_time"] = 0
        data["portfolio_time"] = 0
        data["pd_time"] = 0
        data["collaboration_time"] = 0
        data["total_time"] = 0
        data["progress"] = 0
        data["user_id"] = user_id
        data["course_id"] = course_id
        data["school_year"] = "current"
        data.update(user_data)
        return data

class CoursewareStudentmodule(MongoReportingStore):

    def report_update_data(self, user_id, course_id, is_complete):
        affected_collection = ['courseware_studentmodule', 'UserView', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "courseware_studentmodule":
                data = self.get_user_course_date1(user_id, course_id)
                db_filter = {'student_id': int(user_id), 'course_id': course_id, 'module_type':"course"}
                self.collection.update(db_filter, data, True)
            elif tmp == "UserView":
                if is_complete:
                    data = {'$inc': {'complete_course': 1, 'current_course': -1}}
                else:
                    data = {'$inc': {'complete_course': -1, 'current_course': 1}}
                db_filter = {'school_year': 'current', 'user_id': int(user_id)}
                self.collection.update(db_filter, data)
            elif tmp == "UserCourseView":
                if is_complete:
                    course_data = self.get_user_course_date1(user_id, course_id)
                    data = {"$set":{"complete_date":course_data['state']['complete_date'][0:10]}}
                else:
                    data = {"$set":{"complete_date":""}}
                db_filter = {'user_id': int(user_id), 'course_id': course_id, 'school_year': 'current'}
                self.collection.update(db_filter, data)

class ModuleStore(MongoReportingStore):

    def report_update_data(self, course_id):
        affected_collection = ['modulestore', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "modulestore":
                data = self.get_insert_data(course_id)
                data.pop('_id')
                db_filter = {'course_id': course_id, '_id.category':'course'}
                self.collection.update(db_filter, data)
                data1 = self.get_course_data(course_id)
                db_filter1 = {'q_course_id': course_id}
                self.collection.update(db_filter1, data1, multi=True)
            if tmp == "UserCourseView":
                data = {'$set' : self.get_course_data(course_id)}
                db_filter = {'course_id': course_id}
                self.collection.update(db_filter, data, True, multi=True)

    #  creata_course,   '_id.category':'course'
    def report_insert_data(self, course_id):
        affected_collection = ['modulestore']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "modulestore":
                course_data = self.get_insert_data(course_id)
                self.collection.insert(course_data)

    # publish_draft, '_id.category':'problem,combinedopenended'
    def report_update_problem(self, location, is_publish=True):
        affected_collection = 'modulestore'
        course_data, graded = self.get_course_data_by_location(location)
        arr = location.split('/')
        vertical_data = modulestore().collection.find({'_id.category':arr[4], '_id.org':arr[2], '_id.name':arr[5], '_id.course': arr[3]})
        for tmp in vertical_data:
            if len(tmp['definition']['children']) > 0:
                for tmp1 in tmp['definition']['children']:
                    arr1 = tmp1.split('/')
                    unit_data = modulestore().collection.find({'_id.category':arr1[4], '_id.org':arr1[2], '_id.name':arr1[5], '_id.course': arr1[3]})
                    for tmp2 in unit_data:
                        if tmp2['_id']['category'] == 'problem' or tmp2['_id']['category'] == "combinedopenended":
                            self.set_collection(affected_collection)
                            module_id = tmp2['_id']['tag'] + '://' + tmp2['_id']['org']  + '/' + tmp2['_id']['course']  + '/' + tmp2['_id']['category']  + '/' + tmp2['_id']['name']
                            db_filter = {'module_id': module_id}
                            if is_publish and graded:
                                course_data['module_id'] = module_id
                                course_data.update(tmp2)
                                data = {'$set' : course_data}
                                self.collection.update(db_filter, course_data, True)
                            else:
                                self.collection.remove(db_filter)

    # sequential mark graded
    def report_update_assignment_problem(self, location, graderType):
        arr = location.split('/')
        sequential_data = modulestore().collection.find({'_id.category':arr[4], '_id.org':arr[2], '_id.name':arr[5], '_id.course': arr[3]})
        for tmp in sequential_data:
            if len(tmp['definition']['children']) > 0:
                for tmp1 in tmp['definition']['children']:
                    if graderType == "Assignment":
                        self.report_update_problem(tmp1)
                    else:
                        self.report_update_problem(tmp1, False)

    def get_parent_location(self, location, category):
        data = modulestore().collection.find({'_id.category':category, 'definition.children':{'$in':[location]}})
        parent_location = ""
        for tmp in data:
            parent_location = tmp['_id']['tag'] + '://' + tmp['_id']['org']  + '/' + tmp['_id']['course']  + '/' + tmp['_id']['category']  + '/' + tmp['_id']['name']
        return parent_location

    def get_course_data_by_location(self, location):
        result = {}
        graded = False
        sequential_location = self.get_parent_location(location, 'sequential')
        arr = sequential_location.split('/')
        sequential_data = modulestore().collection.find({'_id.category':arr[4], '_id.org':arr[2], '_id.name':arr[5], '_id.course': arr[3]})
        for tmp in sequential_data:
            result['vertical_num'] = tmp['definition']['children'].index(location) + 1
            try:
                result['sequential_name'] = tmp['metadata']['display_name']
            except:
                result['sequential_name'] = ""
            try:
                graded = tmp['metadata']['graded']
            except:
                graded = False

        chapter_location = self.get_parent_location(sequential_location, 'chapter')
        course_location = self.get_parent_location(chapter_location, 'course')
        arr = course_location.split('/')
        course_data = modulestore().collection.find({'_id.category':arr[4], '_id.org':arr[2], '_id.name':arr[5], '_id.course': arr[3]})
        for tmp in course_data:
            result['q_course_id'] = '/'.join([tmp['_id']['org'], tmp['_id']['course'], tmp['_id']['name']])
            try:
                result['organization'] = tmp['metadata']['display_organization']
            except:
                result['organization'] = ""
            try:
                result['end_date'] = tmp['metadata']['end'][0:10]
            except:
                result['end_date'] = ""
            try:    
                result['start_date'] = tmp['metadata']['start'][0:10]
            except:
                result['start_date'] = ""
            try:    
                result['course_name'] = tmp['metadata']['display_name']
            except:
                result['course_name'] = ""
            try:    
                result['course_number'] = tmp['metadata']['display_coursenumber']
            except:
                result['course_number'] = ""
        return result, graded

    def get_insert_data(self, course_id):
        org, course, name = course_id.split('/');
        course_date = modulestore().collection.find({'_id.category':'course', '_id.org':org, '_id.name':name, '_id.course': course})
        result = {}
        for tmp in course_date:
            result.update(tmp)
        result['course_id'] = course_id
        return result

class PepregStudent(MongoReportingStore):

    def report_update_data(self, training_id, user_id, is_delete=False):
        affected_collection = ['pepreg_student', 'PepRegStudentView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == 'pepreg_student':
                if user_id:
                    if is_delete:
                        db_filter = {'training_id': int(training_id), 'student_id': int(user_id)}
                        self.collection.remove(db_filter)
                    else:
                        data = self.get_training_student_data(training_id, user_id)
                        db_filter = {'training_id': int(training_id), 'student_id': int(user_id)}
                        self.collection.update(db_filter, data, True)
                else:
                    db_filter = {'training_id': int(training_id)}
                    self.collection.remove(db_filter)
            if tmp == 'PepRegStudentView':
                if user_id:
                    if is_delete:
                        db_filter = {'training_id': int(training_id), 'student_id': int(user_id), 'school_year': 'current'}
                        self.collection.remove(db_filter)
                    else:
                        data = self.get_training_student_data(training_id, user_id)
                        data['school_year'] = 'current'
                        data['key'] = 'current_' + str(training_id)
                        if data['instructor_id'] != 'NULL':
                            data['instructor_status'] = 'Yes'
                        else:
                            data['instructor_status'] = 'No'
                        db_filter = {'training_id': int(training_id), 'student_id': int(user_id), 'school_year': 'current'}
                        self.collection.update(db_filter, data, True)
                else:
                    db_filter = {'training_id': int(training_id), 'school_year': 'current'}
                    self.collection.remove(db_filter)

    def get_training_student_data(self, training_id, user_id):
        result = {}
        student_data = PepRegStudent.objects.get(training_id=training_id, student=user_id)
        result['training_id'] = int(training_id)
        result['student_id'] = int(user_id)
        result['student_status'] = student_data.student_status
        result['student_credit'] = student_data.student_credit
        if PepRegInstructor.objects.filter(training_id=training_id, instructor_id=user_id).exists():
            result['instructor_id'] = user_id
        else:
            result['instructor_id'] = 'NULL'
        return result


class PepregTraining(MongoReportingStore):

    def report_update_data(self, training_id, is_delete=False):
        affected_collection = ['pepreg_training', 'PepRegTrainingView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == 'pepreg_training':
                if is_delete:
                    db_filter = {'training_id': int(training_id)}
                    self.collection.remove(db_filter)
                else:
                    data = self.get_training_data(training_id)
                    db_filter = {'training_id': int(training_id)}
                    self.collection.update(db_filter, data, True)
            if tmp == 'PepRegTrainingView':
                if is_delete:
                    db_filter = {'training_id': int(training_id), 'school_year': 'current'}
                    self.collection.remove(db_filter)
                else:
                    data = self.get_training_data(training_id)
                    data['school_year'] = 'current'
                    data['key'] = 'current_' + str(data['training_id'])
                    db_filter = {'training_id': int(training_id), 'school_year': 'current'}
                    self.collection.update(db_filter, data, True)

    def get_training_data(self, training_id):
        result = {}
        training_data = PepRegTraining.objects.get(id=training_id)
        result['training_id'] = int(training_id)
        result['type'] = training_data.type
        result['district_id'] = training_data.district_id
        result['description'] = training_data.description
        result['subject'] = training_data.subject
        result['name'] = training_data.name
        result['pepper_course'] = training_data.pepper_course
        result['training_date'] = training_data.training_date.strftime('%Y-%m-%d')
        result['training_time_start'] = training_data.training_time_start.strftime('%H:%M:%S')
        result['training_time_end'] = training_data.training_time_end.strftime('%H:%M:%S')
        result['geo_location'] = training_data.geo_location
        result['classroom'] = training_data.classroom
        result['credits'] = training_data.credits
        result['attendancel_id'] = training_data.attendancel_id
        result['allow_registration'] = training_data.allow_registration
        result['allow_attendance'] = training_data.allow_attendance
        result['allow_validation'] = training_data.allow_validation
        result['max_registration'] = training_data.max_registration
        result['user_create_id'] = training_data.user_create_id
        result['date_create'] = training_data.date_create.strftime('%Y-%m-%d')
        result['state_id'] = training_data.district.state.id
        result['district'] = training_data.district.name
        result['school'] = School.objects.get(id=training_data.school_id).name
        return result


class ProblemPoint(MongoReportingStore):
    pass

class UserCourseProgress(MongoReportingStore):

    def report_update_data(self, user_id, course_id, progress):
        affected_collection = ['user_course_progress', 'UserCourseView']
        for tmp in affected_collection:
            self.set_collection(tmp)
            if tmp == "user_course_progress":
                data = {'$set': {'progress': progress*100}}
                db_filter = {'user_id': int(user_id), 'course_id': course_id}
                self.collection.update(db_filter, data, True)
            if tmp == "UserCourseView":
                data = {'$set': {'progress': progress*100}}
                db_filter = {'user_id': int(user_id), 'course_id': course_id, 'school_year': 'current'}
                self.collection.update(db_filter, data)