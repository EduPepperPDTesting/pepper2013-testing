from django.db import models
from student.models import District, School, State
from django.contrib.auth.models import User
from student.models import UserProfile
from django.conf import settings
import pymongo
import logging
log = logging.getLogger("tracking")


class ImportTask(models.Model):
    class Meta:
        db_table = 'admin_import_task'
    filename = models.CharField(blank=False, max_length=255, db_index=True)
    total_lines = models.IntegerField(blank=False, default=0)
    process_lines = models.IntegerField(blank=False, default=0)
    success_lines = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, db_index=False)
    task_read = models.BooleanField(blank=False, default=0)
    user = models.ForeignKey(User, default=0)


class ImportTaskLog(models.Model):
    class Meta:
        db_table = 'admin_import_task_log'
    task = models.ForeignKey(ImportTask, on_delete=models.PROTECT)
    line = models.IntegerField(blank=False, default=0)
    username = models.CharField(blank=False, max_length=30, db_index=True)
    import_data = models.CharField(blank=False, max_length=255, default='')
    create_date = models.DateTimeField(auto_now_add=True, db_index=False)
    error = models.CharField(blank=False, max_length=255, db_index=True)


class EmailTask(models.Model):
    class Meta:
        db_table = 'admin_email_task'
    total_emails = models.IntegerField(blank=False, default=0)
    process_emails = models.IntegerField(blank=False, default=0)
    success_emails = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, db_index=False)
    task_read = models.BooleanField(blank=False, default=0)
    user = models.ForeignKey(User, default=0)


class CustomEmail(models.Model):
    class Meta:
        db_table = 'admin_custom_emails'
    email_content = models.TextField(blank=False, null=True)
    name = models.CharField(blank=False, max_length=30, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, default=None, blank=True)
    system = models.BooleanField(blank=False, null=False)
    private = models.BooleanField(blank=False, null=False)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True, default=None, blank=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, default=None, blank=True)


class CustomEmailLog(models.Model):
    class Meta:
        db_table = 'admin_custom_emails_log'
    email_name = models.CharField(blank=False, max_length=30, null=False)
    user = models.ForeignKey(User)
    operation = models.CharField(blank=False, max_length=10, null=False)
    datetime = models.DateTimeField(auto_now_add=True)


class EmailTaskLog(models.Model):
    class Meta:
        db_table = 'admin_email_task_log'
    send_date = models.DateTimeField(auto_now_add=True, db_index=False)
    task = models.ForeignKey(EmailTask, on_delete=models.PROTECT)
    username = models.CharField(blank=False, max_length=30, db_index=True)
    email = models.CharField(blank=False, max_length=75, db_index=True)
    district_name = models.CharField(blank=False, max_length=255, db_index=True)
    error = models.CharField(blank=False, max_length=255, db_index=True)


class TimeReportTask(models.Model):
    class Meta:
        db_table = 'admin_time_report_task'
    total_num = models.IntegerField(blank=False, default=0)
    process_num = models.IntegerField(blank=False, default=0)
    success_num = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, db_index=False)
    task_read = models.BooleanField(blank=False, default=0)
    user = models.ForeignKey(User, default=0)


class AdjustmentTimeLog(models.Model):
    class Meta:
        db_table = 'adjustment_time_log'
    user_id = models.IntegerField(blank=False, max_length=11)
    user_email = models.CharField(blank=False, max_length=75, db_index=True)
    admin_email = models.CharField(blank=False, max_length=75, db_index=True)
    type = models.CharField(blank=False, max_length=30, db_index=True)
    adjustment_time = models.IntegerField(blank=False, default=0)
    create_date = models.DateTimeField(auto_now_add=True, db_index=False)
    course_number = models.CharField(blank=False, null=True, max_length=100, db_index=True)
    comments = models.CharField(blank=False, null=True, max_length=756, db_index=True)


class TimeReportPerm(models.Model):
    class Meta:
        db_table = 'time_report_perm'
    user = models.ForeignKey(User, default=0)


class FilterFavorite(models.Model):
    class Meta:
        db_table = 'admin_filter_favorite'
    user = models.ForeignKey(User)
    name = models.CharField(blank=False, max_length=150, db_index=True)
    filter_json = models.CharField(blank=False, max_length=4096, db_index=True)


class Author(models.Model):
    class Meta:
        db_table = 'author'
    name = models.CharField(blank=False, max_length=255, db_index=False)


class CertificateAssociationType(models.Model):
    class Meta:
        db_table = 'certificate_association_type'
    name = models.CharField(blank=False, max_length=255, db_index=False)


class Certificate(models.Model):
    class Meta:
        db_table = 'certificate'
    certificate_name = models.CharField(blank=False, max_length=255, db_index=False)
    certificate_blob = models.TextField(blank=False, null=True)
    readonly = models.BooleanField(default=1)
    association_type = models.ForeignKey(CertificateAssociationType)
    association = models.IntegerField(blank=False)


class HangoutPermissions(models.Model):
    class Meta:
        db_table = 'hangout_permissions'
    district = models.ForeignKey(District, blank=False)
    permission = models.BooleanField(default=1)


class MongoSiteSettingsStore(object):

    def __init__(self, host, db, collection, port=27017, default_class=None, user=None, password=None,
                 mongo_options=None, **kwargs):

        super(MongoSiteSettingsStore, self).__init__(**kwargs)

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

    def get_item(self, identifier):
        return self.collection.find_one(
                {
                    'identifier': identifier,
                }
        )

    def set_item(self, identifier, value, metadata={}):
        return self.collection.update(
                {
                    'identifier': identifier,
                },
                {
                    '$set': {'value': value, 'metadata': metadata},
                },
                True
        )

    def delete_item(self, identifier):
        return self.collection.remove(
                {
                    'identifier': identifier,
                }
        )


def site_setting_store():
    options = {}
    options.update(settings.SITESETTINGSSTORE['OPTIONS'])
    return MongoSiteSettingsStore(**options)


class PepRegTraining(models.Model):
    class Meta:
        db_table = 'pepreg_training'
    type = models.CharField(blank=False, max_length=50, db_index=False)
    district = models.ForeignKey(District)
    description = models.TextField(blank=False, null=True)
    subject = models.CharField(blank=False, max_length=50, db_index=False)
    name = models.CharField(blank=False, max_length=255, db_index=False)
    pepper_course = models.CharField(blank=False, max_length=255, db_index=False)
    training_date = models.DateField(auto_now_add=False, db_index=False)
    training_time_start = models.TimeField(auto_now_add=False, db_index=False, blank=True, null=True)
    training_time_end = models.TimeField(auto_now_add=False, db_index=False, blank=True, null=True)
    geo_location = models.CharField(blank=False, max_length=255, db_index=False)
    geo_props = models.TextField(blank=False, null=True)
    classroom = models.CharField(blank=False, max_length=255, db_index=False)
    credits = models.FloatField(blank=False, default=0)
    attendancel_id = models.CharField(blank=False, max_length=255, db_index=False)
    allow_registration = models.BooleanField(blank=False, default=0)
    max_registration = models.IntegerField(blank=False, default=0)
    allow_attendance = models.BooleanField(blank=False, default=0)
    allow_student_attendance = models.BooleanField(blank=False, default=0)
    allow_validation = models.BooleanField(blank=False, default=0)
    user_create = models.ForeignKey(User, related_name='+')
    date_create = models.DateField(auto_now_add=False, db_index=False)
    user_modify = models.ForeignKey(User, related_name='+')
    date_modify = models.DateField(auto_now_add=False, db_index=False)
    last_date = models.DateField(auto_now_add=False, db_index=False, null=True)
    school_id = models.IntegerField(blank=False, default=0)


class PepRegInstructor(models.Model):
    class Meta:
        db_table = 'pepreg_instructor'
    training = models.ForeignKey(PepRegTraining)
    instructor = models.ForeignKey(User, related_name='+')
    user_create = models.ForeignKey(User, related_name='+')
    date_create = models.DateField(auto_now_add=True, db_index=False)
    all_edit = models.BooleanField(blank=False, default=0)
    all_delete = models.BooleanField(blank=False, default=0)


class PepRegStudent(models.Model):
    class Meta:
        db_table = 'pepreg_student'
    training = models.ForeignKey(PepRegTraining)
    student = models.ForeignKey(User, related_name='+')
    student_status = models.CharField(blank=False, max_length=50, db_index=False)
    student_credit = models.FloatField(blank=False, default=0)
    user_create = models.ForeignKey(User, related_name='+')
    date_create = models.DateField(auto_now_add=True, db_index=False)
    user_modify = models.ForeignKey(User, related_name='+')
    date_modify = models.DateField(auto_now_add=True, db_index=False)

class UserLoginInfo(models.Model):
    class Meta:
        db_table = 'user_login_info'
    user_id = models.IntegerField(blank=False, max_length=11)
    login_time = models.CharField(max_length=30)
    logout_time = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    last_session =  models.IntegerField(blank=False, max_length=15)
    total_session = models.IntegerField(blank=False, max_length=30)
    login_times = models.IntegerField(blank=False, max_length=15, default=1)
    logout_press = models.BooleanField(blank=False, default=0)
    temp_time = models.CharField(max_length=30)

class PepRegTraining_Backup(models.Model):
    class Meta:
        db_table = 'pepreg_training_hist'
    type = models.CharField(blank=False, max_length=50, db_index=False)
    district = models.ForeignKey(District)
    description = models.TextField(blank=False, null=True)
    subject = models.CharField(blank=False, max_length=50, db_index=False)
    name = models.CharField(blank=False, max_length=255, db_index=False)
    pepper_course = models.CharField(blank=False, max_length=255, db_index=False)
    training_date = models.DateField(auto_now_add=False, db_index=False)
    training_time_start = models.TimeField(auto_now_add=False, db_index=False, blank=True, null=True)
    training_time_end = models.TimeField(auto_now_add=False, db_index=False, blank=True, null=True)
    geo_location = models.CharField(blank=False, max_length=255, db_index=False)
    geo_props = models.TextField(blank=False, null=True)    
    classroom = models.CharField(blank=False, max_length=255, db_index=False)
    credits = models.FloatField(blank=False, default=0)
    attendancel_id = models.CharField(blank=False, max_length=255, db_index=False)
    allow_registration = models.BooleanField(blank=False, default=0)
    max_registration = models.IntegerField(blank=False, default=0)
    allow_attendance = models.BooleanField(blank=False, default=0)
    allow_student_attendance = models.BooleanField(blank=False, default=0)
    allow_validation = models.BooleanField(blank=False, default=0)
    user_create = models.ForeignKey(User, related_name='+')
    date_create = models.DateField(auto_now_add=False, db_index=False)
    user_modify = models.ForeignKey(User, related_name='+')
    date_modify = models.DateField(auto_now_add=False, db_index=False)
    last_date = models.DateField(auto_now_add=False, db_index=False, null=True)
    school_id = models.IntegerField(blank=False, default=0)
    school_year = models.CharField(blank=False, max_length=255, db_index=False)
    

class PepRegInstructor_Backup(models.Model):
    class Meta:
        db_table = 'pepreg_instructor_hist'
    training = models.ForeignKey(PepRegTraining)
    instructor = models.ForeignKey(User, related_name='+')
    user_create = models.ForeignKey(User, related_name='+')
    date_create = models.DateField(auto_now_add=True, db_index=False)
    all_edit = models.BooleanField(blank=False, default=0)
    all_delete = models.BooleanField(blank=False, default=0)
    school_year = models.CharField(blank=False, max_length=255, db_index=False)


class PepRegStudent_Backup(models.Model):
    class Meta:
        db_table = 'pepreg_student_hist'
    training = models.ForeignKey(PepRegTraining)
    student = models.ForeignKey(User, related_name='+')
    student_status = models.CharField(blank=False, max_length=50, db_index=False)
    student_credit = models.FloatField(blank=False, default=0)
    user_create = models.ForeignKey(User, related_name='+')
    date_create = models.DateField(auto_now_add=True, db_index=False)
    user_modify = models.ForeignKey(User, related_name='+')
    date_modify = models.DateField(auto_now_add=True, db_index=False)
    school_year = models.CharField(blank=False, max_length=255, db_index=False)