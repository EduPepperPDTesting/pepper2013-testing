from django.db import models
import logging
log = logging.getLogger("tracking")


class CourseAssignment(models.Model):
    class Meta:
        db_table = 'sso_course_assignments'
    sso_name = models.CharField(blank=False, max_length=255, db_index=True)
    # param_name = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    # param_value = models.CharField(blank=True, null=True, max_length=255, db_index=False)


class CourseAssignmentCourse(models.Model):
    class Meta:
        db_table = 'sso_course_assignment_courses'
    course = models.CharField(blank=False, max_length=255, db_index=True)
    assignment = models.ForeignKey(CourseAssignment, on_delete=models.CASCADE)
