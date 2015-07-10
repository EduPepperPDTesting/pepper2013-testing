# -*-coding:utf-8-*-

from datetime import datetime
from elasticsearch import Elasticsearch
from student.models import CourseEnrollment, UserProfile


import logging
log = logging.getLogger("tracking")

es=Elasticsearch()

INDEX_NAME = 'people'
DOC_TYPE   = 'user'

MAPPING_LONG={'index':'not_analyzed', 'type':'long'}
MAPPING_STRING={'index':'not_analyzed', 'type':'string'}
MAPPING_DATE={'index':'not_analyzed', 'type':'date'}

es_fields={
 '_id':{'mapping':None, 'searching':'term'},   
 'user_id':{'mapping':MAPPING_STRING,'searching':'term'},
 'email_lower':{'mapping':MAPPING_STRING,'searching':'wildcard'},
 'username_lower':{'mapping':MAPPING_STRING,'searching':'prefix'},
 'first_name_lower':{'mapping':MAPPING_STRING,'searching':'prefix'},
 'last_name_lower':{'mapping':MAPPING_STRING,'searching':'prefix'},
 'email':{'mapping':MAPPING_STRING,'searching':'wildcard'},
 'username':{'mapping':MAPPING_STRING,'searching':'prefix'},
 'first_name':{'mapping':MAPPING_STRING,'searching':'prefix'},
 'last_name':{'mapping':MAPPING_STRING,'searching':'prefix'},
 'is_staff':{'mapping':MAPPING_LONG,'searching':'term'},
 'is_active':{'mapping':MAPPING_LONG,'searching':'term'},
 'is_superuser':{'mapping':MAPPING_LONG,'searching':'term'},
 'course':{'mapping':MAPPING_STRING,'searching':'term'},
 'state_id':{'mapping':MAPPING_LONG,'searching':'term'},    
 'district_id':{'mapping':MAPPING_LONG,'searching':'term'},
 'school_id':{'mapping':MAPPING_LONG,'searching':'term'},
 'cohort_id':{'mapping':MAPPING_LONG,'searching':'term'},
 'major_subject_area_id':{'mapping':MAPPING_LONG,'searching':'term'},
 'grade_level_id':{'mapping':MAPPING_LONG,'searching':'term'},
 'years_in_education_id':{'mapping':MAPPING_LONG,'searching':'term'},
 'percent_lunch':{'mapping':MAPPING_LONG,'searching':'term'},
 'percent_iep':{'mapping':MAPPING_LONG,'searching':'term'},
 'percent_eng_learner':{'mapping':MAPPING_LONG,'searching':'term'},
 'last_login':{'mapping':MAPPING_DATE,'searching':'term'},
 'people_of':{'mapping':MAPPING_LONG,'searching':'term'}
}

def delete_index(name):
    # 删除索引
    es.indices.delete(name)

def create_index(name):
    # 创建索引
    es.indices.create(name,ignore=400)

def del_user(id):
    es.delete(index=INDEX_NAME,doc_type=DOC_TYPE, id=id)
    es.indices.refresh()    

def insert_user(id,body):
    # Call create
    # es.create(index=INDEX_NAME,doc_type=DOC_TYPE, body=body, id=id)
    
    # Or call index 
    es.index(index=INDEX_NAME,doc_type=DOC_TYPE, body=body, id=id)
    es.indices.refresh()

def index_user(id,body):
    # update, create if id not exists
    try:
        es.index(index=INDEX_NAME,doc_type=DOC_TYPE, body=body, id=id)
        es.indices.refresh()
    except:
        log.debug("Failed to index user(id=%s)" % id)
        pass

def full_update_user(id,body):
    es.index(index=INDEX_NAME,doc_type=DOC_TYPE, body=body, id=id)
    es.indices.refresh()

def update_user_fields(id,body):
    # 也可以添加新的字段
    es.update(index=INDEX_NAME,doc_type=DOC_TYPE, body={'doc':body}, id=id)
    es.indices.refresh()

def get_user(user_id):
    rec=es.get(index=INDEX_NAME,doc_type=DOC_TYPE,id=user_id)
    return rec.get('_source')

def del_user_people_of(user,owner_id):
    owner_id=str(owner_id)
    # rec=get_user(user.id)
    # if not rec: return

    people_of=[]
    if user.profile.people_of:
        people_of=user.profile.people_of.split(',')
    
    # people_of=rec['people_of']

    # log.debug("============")
    # log.debug(owner_id)

    if owner_id in people_of:
        people_of=filter(lambda a: a != owner_id, people_of)
        # update_user_fields(user_id,{'people_of':people_of})
        # update db
        user.profile.people_of=','.join(people_of)
        user.profile.save()

def add_user_people_of(user,owner_id):
    owner_id=str(owner_id)
    # rec=get_user(user.id)
    # if not rec: return

    people_of=[]
    if user.profile.people_of:
        people_of=user.profile.people_of.split(',')

    # people_of=rec['people_of']
    if not owner_id in people_of:
        people_of.append(owner_id)
        # update_user_fields(user_id,{'people_of':people_of})
        # update db
        
        user.profile.people_of=','.join(people_of)
        user.profile.save()

def update_user_by_script(id,body):
    # todo: finish me
    # refer to: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-update.html
    pass

def search_people(cond):
    r=[]
    result=es.search(index=INDEX_NAME,doc_type=DOC_TYPE,body=cond)
    for rec in result['hits']['hits']:
        u=rec['_source']
        u['user_id']=rec['_id']
        r.append(u)
    return r,result['hits']['total']

def gen_people_search_query(must=None,must_not=None,should=None,start=0,size=20,sort={'last_login':'desc'}):
    cond={'query':{'bool':{}},'from':start,'size':size,'sort':sort}

    def _g(c):
        r=[]
        if not c: return r
        for k in c:
            f=es_fields.get(k)

            if not f:
                continue
            
            if c[k]=='': continue

            searching=f['searching']

            t=None
            if searching=='term':
                t={searching:{k:c[k]}}
            elif searching=='prefix':
                t={searching:{k:c[k]}}
            elif searching=='wildcard':
                t={searching:{k:'*'+c[k].replace('*','\*')+'*'}}
            r.append(t)
        return r
                
    cond['query']['bool']['must']=_g(must)
    if not len(cond['query']['bool']['must']):
        cond['query']['bool']['must'].append({'match_all':{}})    
    cond['query']['bool']['must_not']=_g(must_not)
    cond['query']['bool']['should']=_g(should)
            
    return cond

def update_user_es_info(user):
    if not UserProfile.objects.filter(user_id=user.id).exists():
        return
    
    body={}

    # try:
    #     old=get_user(user.id)
    # except Exception e:
    #     pass
        
    def attr(o,k):
        key=k.replace('_lower','')
        if hasattr(o,key):
            if k.find('_lower')>-1:
                body[k]=getattr(o,key).lower()
            else:
                body[k]=getattr(o,key)

            if isinstance(body[k],bool):
                if body[k]:
                    body[k]=1
                else:
                    body[k]=0
                
    for k in es_fields:
        if not es_fields[k].get('mapping'):
            continue
        attr(user,k)
        attr(user.profile,k)

    # if old:
    #     body['people_of']=old['people_of']
    # else:
    #     body['people_of']=[]

    body['district_id']=user.profile.district_id

    if user.last_login:
        body['last_login']=user.last_login.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    if body['district_id']:
        body['state_id']=user.profile.district.state_id
    else:
        body['state_id']=0

    if user.profile.people_of:
        body['people_of']=[int(i) for i in user.profile.people_of.split(',')]
    else:
        body['people_of']=[]

    log.debug(body['people_of'])

    courses=[]
    for c in CourseEnrollment.enrollments_for_user(user=user):
        courses.append(c.course_id)
    body['course']=courses

    if user.profile.grade_level_id:
        body['grade_level_id']=user.profile.grade_level_id.split(',')
    else:
        body['grade_level_id']=[]

    index_user(user.id, body)
