'''
django admin pages for courseware model
'''

from student.models import UserProfile, UserTestGroup, CourseEnrollmentAllowed
from student.models import CourseEnrollment, Registration, PendingNameChange
from student.models import ResourceLibrary, ResourceLibraryCategory, ResourceLibrarySubclassSite, \
							ResourceLibrarySubclass, CmsLoginInfo, StaticContent
from ratelimitbackend import admin

admin.site.register(UserProfile)

admin.site.register(UserTestGroup)

admin.site.register(CourseEnrollment)

admin.site.register(CourseEnrollmentAllowed)

admin.site.register(Registration)

admin.site.register(PendingNameChange)

admin.site.register(ResourceLibrarySubclassSite)

admin.site.register(ResourceLibrarySubclass)

admin.site.register(ResourceLibraryCategory)

admin.site.register(ResourceLibrary)

admin.site.register(CmsLoginInfo)

admin.site.register(StaticContent)