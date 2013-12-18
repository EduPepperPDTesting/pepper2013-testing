from student.models import UserProfile, People
from django.core.paginator import Paginator
import sphinxapi
import socket

import logging
log = logging.getLogger("tracking")


class JuncheePaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=5, orphans=0, allow_empty_first_page=True):
        
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num

    def page(self, number):
        self.page_num = number
        return super(JuncheePaginator, self).page(number)

    def _page_range_ext(self):
        if self.num_pages <= self.range_num:
            return range(1, self.num_pages + 1)
        num_list = []
        start=int(self.page_num-round(self.range_num/2))
        if start<1:start=1
        end=int(start+self.range_num)
        if end>self.num_pages: end=self.num_pages
        for i in range(start, end+1):
            num_list.append(i)
        return num_list

    page_range_ext = property(_page_range_ext)

class Filter():
    def __init__(self,item_decorator=None):
        self.client=sphinxapi.SphinxClient()
        self.cond=list()
        self.result=None
        self.item_decorator=item_decorator
        # max_matches:
        # 0 means default
        # can't be larger than max_matches in sphinx.conf
        self.max_matches=0

    def SetLimits(self,offset,limit):
        self.client.SetLimits(offset,limit,self.max_matches)
        
    def SetServer(self,host,port):
        self.client.SetServer(host,port)
        
    def SetFilter(self,attribute, values, exclude=0):
        self.client.SetFilter(attribute, values, exclude)

    def SetMatchMode(self,mode):
        self.client.SetMatchMode(mode)

    def SetMaxMatches(self,count):
        self.max_matches=count
        
    def AddCond(self,cond):
        self.cond.append(cond)  
        
    def count(self):
        self.SetLimits(0,1)
        self.Query()
        if self.result:
            return self.result['total_found']
        else:
            return 0
        
    def __getitem__(self,key):
        # the key is a slice()
        stop=key.stop
        start=key.start
        if stop<1: stop=1
        self.SetLimits(start,stop) 
        # re-calc range, cause we fetch the current page from sphinx only.
        if start>1:
            stop=stop-start
            start=0
        self.Query()
        ret=list()
        if self.result and self.item_decorator:
            for i,item in enumerate(self.result['matches']):
                self.result['matches'][i]=self.item_decorator(item)
            ret=self.result['matches'][start:stop]
        return ret
    
    def Query(self):
        try:
            self.result=self.client.Query(' '.join(self.cond),'people_user,delta')
            # log.debug(' '.join(self.cond))
        except socket.error, msg:
            raise Exception("Failed to connect sphinx")

def search_user(me,username='',first_name='',last_name='',
                district_id='',school_id='',subject_area_id='',
                grade_level_id='',years_in_education_id='',course_id='',email=''):

    """
    refer to:
    http://sphinxsearch.com/docs/current.html#extended-syntax
    5.3. Extended query syntax

    testing mysql query:
    select a.user_id,b.email,a.course_id from student_courseenrollment a inner join auth_user b on a.user_id=b.id order by a.course_id;
    select a.user_id,b.email,group_concat(a.course_id,' ') from student_courseenrollment a inner join auth_user b on
    a.user_id=b.id where b.is_active and not b.is_staff and not b.is_superuser and a.course_id  like 'WestEd%' group by a.user_id;
    """
    
    def dc(item):
        profile=UserProfile.objects.get(user_id=item['id'])
        f=People.objects.filter(user_id=me.id).filter(people_id=profile.user_id)
        profile.student_people_id=None
        if f.exists():
            profile.student_people_id=f[0].id
        return profile
    
    f=Filter(dc)
    # f.SetFieldWeights()
    # f.SetLimits(0, 5)
    
    f.SetMaxMatches(10000)
    
    f.SetServer('127.0.0.1', 9312)
    f.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)
    # f.AddCond('@user_id !%s' % me.id)

    f.SetFilter('user_id',[me.id],True)

    if email:
        f.AddCond('@email "%s"' % email)    
    if course_id:
        f.AddCond('@course "%s"' % course_id)
    if username:
        f.AddCond('@username "^%s*"' % username)
    if first_name:
        f.AddCond('@first_name "^%s*"' % first_name)
    if last_name:
        f.AddCond('@last_name "^%s*"' % last_name)
    if district_id:
        f.AddCond("@district_id %s" % district_id)
    if school_id:
        f.AddCond("@school_id %s" % school_id)        
    if subject_area_id:
        f.AddCond("@subject_area_id %s" % subject_area_id)        
    if grade_level_id:
        f.AddCond('@grade_level_id "%s"' % grade_level_id)        
    if years_in_education_id:
        f.AddCond("@years_in_education_id %s" % years_in_education_id)
    
    # if len(f.cond)==1:
    #     f.SetMatchMode(sphinxapi.SPH_MATCH_FULLSCAN)

    return f

