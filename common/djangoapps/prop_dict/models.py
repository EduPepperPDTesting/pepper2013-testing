
from django.db import connection

def dictfetchall(cursor):
    '''Returns a list of all rows from a cursor as a column: result dict.
    Borrowed from Django documentation'''
    desc = cursor.description
    table = []
    # table.append([col[0] for col in desc])
    
    # ensure response from db is a list, not a tuple (which is returned
    # by MySQL backed django instances)
    rows_from_cursor=cursor.fetchall()
    table = table + [list(row) for row in rows_from_cursor]

    b=[]

    for r in table:
        t={}
        for i,d in enumerate(desc):
            t[d[0]]=r[i]
        b.append(t)
        
    return b

def query_list(cursor, query_string):
    cursor.execute(query_string)
    raw_result=dictfetchall(cursor)
    return raw_result


def query_dict(cursor, query_string):
    cursor.execute(query_string)
    raw_result=dictfetchall(cursor)
    if len(raw_result):
        return raw_result[0]

def schools(district_id=0):
    cursor = connection.cursor()
    if district_id>0:
        lst=query_list(cursor, "select * from school where district_id=%s" % (district_id))
    else:
        lst=query_list(cursor, "select * from school")
    return lst

def get_school(id):
    cursor = connection.cursor()
    lst=query_dict(cursor, "select * from school where id=%s" % (id))
    return lst
    
def districts():
    cursor = connection.cursor()
    lst=query_list(cursor, "select * from district")
    return lst

def get_district(id):
    cursor = connection.cursor()
    lst=query_dict(cursor, "select * from district where id=%s" % (id))
    return lst 

def subject_areas():
    cursor = connection.cursor()
    lst=query_list(cursor, "select * from subject_area")
    return lst

def get_subject_area(id):
    cursor = connection.cursor()
    lst=query_dict(cursor, "select * from subject_area where id=%s" % (id))
    return lst


def grade_levels():
    cursor = connection.cursor()
    lst=query_list(cursor, "select * from grade_level")
    return lst

def get_grade_level(id):
    cursor = connection.cursor()
    lst=query_dict(cursor, "select * from grade_level where id=%s" % (id))
    return lst 

def years_in_educations():
    cursor = connection.cursor()
    lst=query_list(cursor, "select * from years_in_education")
    return lst

def get_years_in_education(id):
    cursor = connection.cursor()
    lst=query_dict(cursor, "select * from years_in_education where id=%s" % (id))
    return lst 
