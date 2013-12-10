from student.models import UserProfile
# import sphinxapi
def search_user(username='',first_name='',last_name='',
                district_id='',school_id='',subject_area_id='',
                grade_level_id='',years_in_education_id='',course_id=''):
    pass
    
#     client = sphinxapi.SphinxClient()
#     # client.SetFieldWeights()
#     client.SetLimits(0, 5)  
#     client.SetServer('127.0.0.1', 9312)
#     client.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)
    
#     # if course_id:
#     #     # todo: Implement multi course.
#     #     # read http://sphinxsearch.com/forum/view.html?id=8901
#     #     client.SetFilter('course_id',[course_id])
    
#     cond=list()
#     # refer to:
#     # http://sphinxsearch.com/docs/current.html#extended-syntax
#     # 5.3. Extended query syntax

#  # select a.user_id,b.email,a.course_id from student_courseenrollment a inner join auth_user b on a.user_id=b.id order by a.course_id;
# # select a.user_id,b.email,group_concat(a.course_id,' ') from student_courseenrollment a inner join auth_user b on a.user_id=b.id where b.is_active and not b.is_staff and not b.is_superuser and a.course_id  like 'WestEd%' group by a.user_id;

    
#     if course_id:
#         cond.append('@course "WestEd/002/002"')
#     if username:
#         cond.append("@username %s" % username)
#     if first_name:
#         cond.append("@first_name %s" % first_name)
#     if last_name:
#         cond.append("@last_name %s" % last_name)
#     if district_id:
#         cond.append("@district_id %s" % district_id)
#     if school_id:
#         cond.append("@school_id %s" % school_id)        
#     if subject_area_id:
#         cond.append("@subject_area_id %s" % subject_area_id)        
#     if grade_level_id:
#         cond.append("@grade_level_id %s" % grade_level_id)        
#     if years_in_education_id:
#         cond.append("@years_in_education_id %s" % years_in_education_id)        
#     result=client.Query(' '.join(cond))

#     profiles=list()       
 
#     if result:
#         # status ,matches ,fields ,time ,total_found ,warning ,attrs ,words ,error ,total
#         matches=result['matches']
#         for item in matches:
#             profiles.append(UserProfile.objects.get(user_id=item['id']))
        
#     return profiles

# from django_sphinx_db.backend.models import SphinxModel, SphinxField
# class User(SphinxModel):
#     class Meta:
#         # This next bit is important, you don't want Django to manage
#         # the table for this model.
#         managed = False

#     user_name = SphinxField()
#     first_name = SphinxField()
#     id = SphinxField()
