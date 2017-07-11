
# -----------------------------------
# Aggregation config
# -----------------------------------


# definition aggregation:

AggregationConfig = {
    "UserView": {
        "collection": "UserView"
    },
    "UserCourseView": {
        "collection": "UserCourseView"
    },
    "CourseView": {
        "collection": "student_courseenrollment"
    },
    "CourseAssignmentsView": {
        "collection": "modulestore"
    },
    "AggregateGradesView": {
        "collection": "student_courseenrollment"
    },""
    "AggregateTimerView": {
        "collection": "user_info"
    },
    "PDPlannerView": {
        "collection": "PepRegTrainingView"
    }
}

# aggregation query:  (*placeholder: {user_domain}, {display_columns}, {filters}, {distinct}, {school_year}, {pd_domain})

#  user -------------------------------------------------------------------------------

AggregationConfig["UserView"]["query"] = '''{school_year}{user_domain}
{
    "$group": {
        "_id": "$user_id",
        "user_id": {
            "$last": "$user_id"
        },
        "email": {
            "$last": "$email"
        },
        "user_name": {
            "$last": "$user_name"
        },
        "first_name": {
            "$last": "$first_name"
        },
        "last_name": {
            "$last": "$last_name"
        },
        "state": {
            "$last": "$state"
        },
        "district": {
            "$last": "$district"
        },
        "school": {
            "$last": "$school"
        },
        "activate_date": {
            "$last": "$activate_date"
        },
        "subscription_status": {
            "$last": "$subscription_status"
        },
        "current_course": {
            "$last": "$current_course"
        },
        "complete_course": {
            "$last": "$complete_course",
        },
        "course_time": {
            "$sum": "$course_time"
        },
        "external_time": {
            "$sum": "$external_time"
        },
        "discussion_time": {
            "$sum": "$discussion_time"
        },
        "portfolio_time": {
            "$sum": "$portfolio_time"
        },
        "collaboration_time": {
            "$sum": "$collaboration_time"
        },
        "total_time": {
            "$sum": "$total_time"
        },
        "pd_time": {
            "$sum": "$pd_time"
        }
    }
}, {
    "$project": {
        "user_id": 1,
        "email": 1,
        "user_name": 1,
        "first_name": 1,
        "last_name": 1,
        "state": 1,
        "district": 1,
        "school": 1,
        "activate_date": 1,
        "subscription_status": 1,
        "current_course": 1,
        "complete_course": 1,
        "course_time": 1,
        "external_time": 1,
        "discussion_time": 1,
        "portfolio_time": 1,
        "collaboration_time": 1,
        "total_time": 1,
        "pd_time": 1
    }
}{filters}{display_columns}{distinct}
'''

# user course -------------------------------------------------------------------------------

AggregationConfig["UserCourseView"]["query"] = '''{school_year}{user_domain}
{
    "$group": {
        "_id": {
            "user_id": "$user_id",
            "course_id": "$course_id"
        },
        "user_id": {
            "$last": "$user_id"
        },
        "course_id": {
            "$last": "$course_id"
        },
        "email": {
            "$last": "$email"
        },
        "user_name": {
            "$last": "$user_name"
        },
        "first_name": {
            "$last": "$first_name"
        },
        "last_name": {
            "$last": "$last_name"
        },
        "state": {
            "$last": "$state"
        },
        "district": {
            "$last": "$district"
        },
        "school": {
            "$last": "$school"
        },
        "subscription_status": {
            "$last": "$subscription_status"
        },
        "course_number": {
            "$last": "$course_number"
        },
        "course_name": {
            "$last": "$course_name"
        },
        "course_run": {
            "$last": "$course_run"
        },
        "start_date": {
            "$last": "$start_date"
        },
        "end_date": {
            "$last": "$end_date"
        },
        "organization": {
            "$last": "$organization"
        },
        "enrollment_date": {
            "$last": "$enrollment_date"
        },
        "complete_date": {
            "$last": "$complete_date"
        },
        "portfolio_url": {
            "$last": "$portfolio_url"
        },
        "progress": {
            "$last": "$progress"
        },
        "course_time": {
            "$sum": "$course_time"
        },
        "external_time": {
            "$sum": "$external_time"
        },
        "discussion_time": {
            "$sum": "$discussion_time"
        },
        "portfolio_time": {
            "$sum": "$portfolio_time"
        },
        "collaboration_time": {
            "$sum": "$collaboration_time"
        },
        "total_time": {
            "$sum": "$total_time"
        },
        "pd_time": {
            "$sum": "$pd_time"
        }
    }
}, {
    "$project": {
        "user_id": 1,
        "course_id": 1,
        "email": 1,
        "user_name": 1,
        "first_name":1,
        "last_name": 1,
        "state": 1,
        "district": 1,
        "school": 1,
        "subscription_status": 1,
        "course_number": 1,
        "course_name": 1,
        "course_run": 1,
        "start_date": 1,
        "end_date": 1,
        "organization": 1,
        "enrollment_date": 1,
        "complete_date": 1,
        "portfolio_url": 1,
        "progress": 1,
        "course_time": 1,
        "external_time": 1,
        "discussion_time": 1,
        "portfolio_time": 1,
        "collaboration_time": 1,
        "total_time": 1,
        "pd_time": 1
    }
}{filters}{display_columns}{distinct}'''

#  course -------------------------------------------------------------------------------

AggregationConfig["CourseView"]["query"] = '''{user_domain}{
    "$match": {
        "is_active": 1
    }
}, {
    "$lookup": {
        "from": "user_info",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "user_info"
    }
}, {
    "$project": {
        "user_id": 1,
        "course_id": 1,
        "state_id": "$user_info.state_id",
        "distric_id": "$user_info.distric_id",
        "school_id": "$user_info.school_id",
    }
},{
    "$lookup": {
        "from": "modulestore",
        "localField": "course_id",
        "foreignField": "course_id",
        "as": "course_info"
    }
}, {
    "$lookup": {
        "from": "courseware_studentmodule",
        "localField": "user_id",
        "foreignField": "c_student_id",
        "as": "studentmodule"
    }
}, {
    "$lookup": {
        "from": "UserCourseView",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "user_course_view"
    }
}, {
    "$project": {
        "course_id": 1,
        "complete_course": {
            "$sum": {
                "$map": {
                    "input": "$studentmodule",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$and": [{
                                "$eq": ["$$item.course_id", "$course_id"]
                            }, {
                                "$eq": ["$$item.state.complete_course", True]
                            }]
                        }, 1, 0]
                    }
                }
            }
        },
        "external_time": {
            "$sum": {
                "$map": {
                    "input": "$user_course_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$and": [{
                                "$eq": ["$$item.course_id", "$course_id"]
                            }, {
                                "$eq": {school_year}
                            }]
                        }, "$$item.external_time", 0]
                    }
                }
            }
        },
        "course_time": {
            "$sum": {
                "$map": {
                    "input": "$user_course_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$and": [{
                                "$eq": ["$$item.course_id", "$course_id"]
                            }, {
                                "$eq": {school_year}
                            }]
                        }, "$$item.course_time", 0]
                    }
                }
            }
        },
        "discussion_time": {
            "$sum": {
                "$map": {
                    "input": "$user_course_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$and": [{
                                "$eq": ["$$item.course_id", "$course_id"]
                            }, {
                                "$eq": {school_year}
                            }]
                        }, "$$item.discussion_time", 0]
                    }
                }
            }
        },
        "portfolio_time": {
            "$sum": {
                "$map": {
                    "input": "$user_course_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$and": [{
                                "$eq": ["$$item.course_id", "$course_id"]
                            }, {
                                "$eq": {school_year}
                            }]
                        }, "$$item.portfolio_time", 0]
                    }
                }
            }
        },
        "course_number": "$course_info.metadata.display_coursenumber",
        "course_name": "$course_info.metadata.display_name",
        "course_run": "$course_info._id.org",
        "start_date": "$course_info.metadata.start",
        "end_date": "$course_info.metadata.end",
        "organization": "$course_info.metadata.display_organization"
    }
}, {
    "$project": {
        "course_id": 1,
        "course_number": 1,
        "course_name": 1,
        "course_run": 1,
        "start_date": 1,
        "end_date": 1,
        "organization": 1,
        "complete_course": 1,
        "course_time": 1,
        "external_time": 1,
        "discussion_time": 1,
        "portfolio_time": 1,
        "collaboration_time": {
            "$add": ["$discussion_time", "$portfolio_time"]
        },
        "total_time": {
            "$add": ["$course_time", "$external_time", "$discussion_time", "$portfolio_time"]
        }
    }
}, {
    "$group": {
        "_id": "$course_id",

        "course_number": {
            "$push": {
                "$arrayElemAt": ["$course_number", 0]
            }
        },
        "course_name": {
            "$push": {
                "$arrayElemAt": ["$course_name", 0]
            }
        },
        "enrolled_course_num": {
            "$sum": 1
        },
        "course_run": {
            "$push": {
                "$arrayElemAt": ["$course_run", 0]
            }
        },
        "start_date": {
            "$push": {
                "$arrayElemAt": ["$start_date", 0]
            }
        },
        "end_date": {
            "$push": {
                "$arrayElemAt": ["$end_date", 0]
            }
        },
        "organization": {
            "$push": {
                "$arrayElemAt": ["$organization", 0]
            }
        },
        "complete_course": {
            "$sum": "$complete_course"
        },
        "course_time": {
            "$sum": "$course_time"
        },
        "external_time": {
            "$sum": "$external_time"
        },
        "discussion_time": {
            "$sum": "$discussion_time"
        },
        "portfolio_time": {
            "$sum": "$portfolio_time"
        },
        "collaboration_time": {
            "$sum": "$collaboration_time"
        },
        "total_time": {
            "$sum": "$total_time"
        }
    }
}, {
    "$project": {
        "complete_course": 1,
        "enrolled_course_num": 1,
        "course_time": 1,
        "external_time": 1,
        "discussion_time": 1,
        "portfolio_time": 1,
        "collaboration_time": 1,
        "total_time": 1,
        "course_number": {
            "$arrayElemAt": ["$course_number", 0]
        },
        "course_name": {
            "$arrayElemAt": ["$course_name", 0]
        },
        "course_run": {
            "$arrayElemAt": ["$course_run", 0]
        },
        "start_date": {
            "$substr": [{
                "$arrayElemAt": ["$start_date", 0]
            }, 0, 10]
        },
        "end_date": {
            "$substr": [{
                "$cond": [{
                    "$eq": ["$end_date", []]
                }, "", {
                    "$arrayElemAt": ["$end_date", 0]
                }]
            }, 0, 10]
        },
        "organization": {
            "$arrayElemAt": ["$organization", 0]
        },
        "avg_course_time": {
            "$ceil": {
                "$divide": ["$course_time", "$enrolled_course_num"]
            }
        }
    }
}{filters}{display_columns}{distinct}'''

#  course assignments -------------------------------------------------------------------------------

AggregationConfig["CourseAssignmentsView"]["query"] = '''{
    "$match": {
        "q_course_id": {
            "$exists": True
        }
    }
}, {
    "$project": {
        "course_id": "$q_course_id",
        "course_number": 1,
        "course_name": 1,
        "course_run": "$_id.org",
        "start_date": 1,
        "end_date": 1,
        "organization": 1,
        "sequential_name": 1,
        "vertical_num": 1,
        "display_name": "$metadata.display_name",
        "weight": {
            "$ifNull": ["$metadata.weight", 1]
        }
    }
}{filters}{display_columns}{distinct}'''

#  aggregate grades -------------------------------------------------------------------------------

AggregationConfig["AggregateGradesView"]["query"] = '''{user_domain}{
    "$match": {
        "is_active": 1
    }
}, {
    "$lookup": {
        "from": "user_info",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "user_info"
    }
}, {
    "$project": {
        "user_id": 1,
        "course_id": 1,
        "email": {
            "$arrayElemAt": ["$user_info.email", 0]
        },
        "user_name": {
            "$arrayElemAt": ["$user_info.username", 0]
        },
        "state": {
            "$arrayElemAt": ["$user_info.state", 0]
        },
        "district": {
            "$arrayElemAt": ["$user_info.district", 0]
        },
        "school": {
            "$arrayElemAt": ["$user_info.school", 0]
        },
        "state_id": "$user_info.state_id",
        "district_id": "$user_info.district_id",
        "school_id": "$user_info.school_id"
    }
},{
    "$lookup": {
        "from": "modulestore",
        "localField": "course_id",
        "foreignField": "q_course_id",
        "as": "question_info"
    }
}, {
    "$unwind": "$question_info"
}, {
    "$project": {
        "_id": 0,
        "user_id": 1,
        "email": 1,
        "user_name": 1,
        "state": 1,
        "district": 1,
        "school": 1,
        "course_id": "$question_info.q_course_id",
        "course_number": "$question_info.course_number",
        "course_name": "$question_info.course_name",
        "course_run": "$question_info._id.org",
        "start": "$question_info.start_date",
        "end": "$question_info.end_date",
        "organization": "$question_info.organization",
        "sequential_name": "$question_info.sequential_name",
        "vertical_num": "$question_info.vertical_num",
        "display_name": "$question_info.metadata.display_name",
        "module_id": "$question_info.module_id"
    }
}, {
    "$lookup": {
        "from": "problem_point",
        "localField": "module_id",
        "foreignField": "module_id",
        "as": "problem_point"
    }
}, {
    "$project": {
        "email": 1,
        "user_name": 1,
        "state": 1,
        "district": 1,
        "school": 1,
        "course_number": 1,
        "course_name": 1,
        "course_run": 1,
        "start": 1,
        "end": 1,
        "organization": 1,
        "sequential_name": 1,
        "vertical_num": 1,
        "display_name": 1,
        "point": {
            "$sum": {
                "$map": {
                    "input": "$problem_point",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.user_id", "$user_id"]
                        }, "$$item.point", 0]
                    }
                }
            }
        }
    }
}{filters}{display_columns}{distinct}'''

#  aggregate timer -------------------------------------------------------------------------------

AggregationConfig["AggregateTimerView"]["query"] = '''{user_domain}{

    "$lookup": {
        "from": "UserView",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "user_view"
    }
}, {
    "$project": {
        "user_id": 1,
        "course_time": {
            "$sum": {
                "$map": {
                    "input": "$user_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                           "$eq": {school_year}
                        }, "$$item.course_time", 0]
                    }
                }
            }
        },
        "external_time": {
             "$sum": {
                "$map": {
                    "input": "$user_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                           "$eq": {school_year}
                        }, "$$item.external_time", 0]
                    }
                }
            }
        },
        "discussion_time": {
            "$sum": {
                "$map": {
                    "input": "$user_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                           "$eq": {school_year}
                        }, "$$item.discussion_time", 0]
                    }
                }
            }
        },
        "portfolio_time": {
            "$sum": {
                "$map": {
                    "input": "$user_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                           "$eq": {school_year}
                        }, "$$item.portfolio_time", 0]
                    }
                }
            }
        },
        "pd_time": {
            "$sum": {
                "$map": {
                    "input": "$user_view",
                    "as": "item",
                    "in": {
                        "$cond": [{
                           "$eq": {school_year}
                        }, "$$item.pd_time", 0]
                    }
                }
            }
        }
    }
}, {
    "$project": {
        "user_id": 1,
        "course_time": 1,
        "external_time": 1,
        "discussion_time": 1,
        "portfolio_time": 1,
        "pd_time": 1,
        "collaboration_time": {
            "$add": ["$discussion_time", "$portfolio_time"]
        },
        "total_time": {
            "$add": ["$course_time", "$external_time", "$discussion_time", "$portfolio_time", "$pd_time"]
        }
    }

}, {
    "$group": {
        "_id": "null",
        "course_time": {
            "$sum": "$course_time"
        },
        "external_time": {
            "$sum": "$external_time"
        },
        "discussion_time": {
            "$sum": "$discussion_time"
        },
        "portfolio_time": {
            "$sum": "$portfolio_time"
        },
        "collaboration_time": {
            "$sum": "$collaboration_time"
        },
        "total_time": {
            "$sum": "$total_time"
        },
        "pd_time": {
            "$sum": "$pd_time"
        }
    }
}{filters}{display_columns}{distinct}'''

#  pd planner -------------------------------------------------------------------------------

AggregationConfig["PDPlannerView"]["query"] = '''{school_year}{pd_domain}{
    "$lookup": {
        "from": "PepRegStudentView",
        "localField": "key",
        "foreignField": "key",
        "as": "pegreg_student"
    }
}, {
    "$unwind": {"path":"$pegreg_student", "preserveNullAndEmptyArrays": True}
}, {
    "$lookup": {
        "from": "user_info",
        "localField": "pegreg_student.student_id",
        "foreignField": "user_id",
        "as": "user_info"
    }
},{
    "$project": {
        "training_id": 1,
        "type": 1,
        "district_id": 1,
        "subject": 1,
        "name": 1,
        "pepper_course": 1,
        "training_date": 1,
        "training_time_start": 1,
        "training_time_end": 1,
        "geo_location": 1,
        "classroom": 1,
        "credits": 1,
        "attendancel_id": 1,
        "allow_registration": 1,
        "max_registration": 1,
        "allow_attendance": 1,
        "allow_validation": 1,
        "user_create_id": 1,
        "date_create": 1,
        "description": 1,
        "student_status": "$pegreg_student.student_status",
        "instructor_status": "$pegreg_student.instructor_status",
        "student_credit": "$pegreg_student.student_credit",
        "user_id": "$pegreg_student.student_id",
        "district": 1,
        "school": 1,
        "state_id": 1,
        "school_id": {
            "$ifNull": [{"$arrayElemAt": ["$user_info.school_id", 0]}, "1"]
        },
        "student": {
            "$arrayElemAt": ["$user_info.email", 0]
        },
        "user_state": {
            "$arrayElemAt": ["$user_info.state", 0]
        },
        "user_district": {
            "$arrayElemAt": ["$user_info.district", 0]
        },
        "user_school": {
            "$arrayElemAt": ["$user_info.school", 0]
        }
    }
},{pd_user_domain}{filters}{display_columns}{distinct}'''


#get_create_column_Headers-------------------------------------------------------------------------------
get_create_column_headers = '''
    {
        "$group":{
            "_id":{"column_headers":"$column_headers"},
            "count":{"$sum":1}
        }
    },
    {
        "$out":"collection_column_header"
    }
'''

get_create_row_headers = '''
    {
        "$group":{
            "_id":{"row_headers":"$row_headers"},
            "count":{"$sum":1}
        }
    },
    {
        "$out":"collection_row_header"
    }
'''

#aggregategrades for all field-------------------------------------------------------------------------------------------
AggregationConfig["AggregateGradesView"]["allfieldquery"]='''{
        '$match': {
            'is_active': 1
        }
    },
    {
        '$lookup': {
            'foreignField': 'user_id',
            'as': 'user_info',
            'from': 'user_info',
            'localField': 'user_id'
        }
    }, {
        '$project': {
        'school_id': '$user_info.school_id',
        'state': {'$arrayElemAt': ['$user_info.state', 0]},
        'user_id': 1,
        'school': {'$arrayElemAt': ['$user_info.school', 0]},
        'district': {'$arrayElemAt': ['$user_info.district', 0]},
        'course_id': 1,
        'state_id': '$user_info.state_id',
        'user_name': {'$arrayElemAt': ['$user_info.username', 0]},
        'email': {'$arrayElemAt': ['$user_info.email', 0]},
        'district_id': '$user_info.district_id'
        }
    }, {
        '$lookup': {
            'foreignField': 'q_course_id',
            'as': 'question_info',
            'from': 'modulestore', 
            'localField': 'course_id'
        }
    }, {
        '$unwind': '$question_info'
    }, {
        '$project': {
            'school': 1,
            'user_id': 1,
            'district': 1,
            'course_run': '$question_info._id.org',
            'end': '$question_info.end_date',
            'module_id': '$question_info.module_id',
            'sequential_name': '$question_info.sequential_name',
            'start': '$question_info.start_date',
            'state': 1,
            'vertical_num': '$question_info.vertical_num',
            'course_number': '$question_info.course_number',
            'organization': '$question_info.organization',
            'course_id': '$question_info.q_course_id',
            'course_name': '$question_info.course_name',
            '_id': 0,
            'user_name': 1,
            'email': 1,
            'display_name': '$question_info.metadata.display_name'
        }
    }, {
        '$lookup': {
            'foreignField': 'module_id',
            'as': 'problem_point',
            'from': 'problem_point',
            'localField': 'module_id'
        }
    }, {
        '$project': {
            'point': {
                '$sum': {
                    '$map': {
                        'input': '$problem_point',
                        'as': 'item',
                        'in': {
                            '$cond': [{'$eq': ['$$item.user_id', '$user_id']}, '$$item.point', 0]}
                            }
                        }
                    },
            'vertical_num': 1,
            'end': 1,
            'display_name': 1,
            'school': 1,
            'course_name': 1,
            'district': 1,
            'course_run': 1,
            'sequential_name': 1,
            'start': 1,
            'state': 1,
            'course_number': 1,
            'organization': 1,
            'user_name': 1,
            'email': 1
        }
    }, {
        '$project': {
            'point': 1,
            'vertical_num': 1,
            'course_name': 1,
            'display_name': 1,
            'school': 1,
            'end': 1,
            'district': 1,
            'course_run': 1,
            'sequential_name': 1,
            'start': 1,
            'state': 1,
            'course_number': 1,
            'organization': 1,
            'user_name': 1,
            'email': 1
        }
    }, {
        '$group': {
            'school': {'$push': '$school'},
            'course_name': {'$push': '$course_name'},
            'district': {'$push': '$district'},
            'course_run': {'$push': '$course_run'},
            'point': {'$push': '$point'},
            'state': {'$push': '$state'},
            'end': {'$push': '$end'},
            'start': {'$push': '$start'},
            'sequential_name': {'$push': '$sequential_name'},
            'vertical_num': {'$push': '$vertical_num'},
            'course_number': {'$push': '$course_number'},
            'organization': {'$push': '$organization'},
            '_id': {
                'point': '$point',
                'vertical_num': '$vertical_num',
                'end': '$end',
                'display_name': '$display_name',
                'school': '$school',
                'course_name': '$course_name',
                'district': '$district',
                'course_run': '$course_run',
                'sequential_name': '$sequential_name',
                'start': '$start',
                'state': '$state',
                'course_number': '$course_number',
                'organization': '$organization',
                'user_name': '$user_name',
                'email': '$email'
                },
            'user_name': {'$push': '$user_name'},
            'email': {'$push': '$email'},
            'display_name': {'$push': '$display_name'
            }
        }
    }, {
        '$project': {
            'point': {'$arrayElemAt': ['$point', 0]},
            'vertical_num': {'$arrayElemAt': ['$vertical_num', 0]},
            'course_name': {'$arrayElemAt': ['$course_name', 0]},
            'display_name': {'$arrayElemAt': ['$display_name', 0]},
            'school': {'$arrayElemAt': ['$school', 0]},
            'end': {'$arrayElemAt': ['$end', 0]},
            'district': {'$arrayElemAt': ['$district', 0]},
            'course_run': {'$arrayElemAt': ['$course_run', 0]},
            'sequential_name': {'$arrayElemAt': ['$sequential_name', 0]},
            'start': {'$arrayElemAt': ['$start', 0]},
            'state': {'$arrayElemAt': ['$state', 0]},
            'course_number': {'$arrayElemAt': ['$course_number', 0]},
            'organization': {'$arrayElemAt': ['$organization', 0]},
            'user_name': {'$arrayElemAt': ['$user_name', 0]},
            'email': {'$arrayElemAt': ['$email', 0]
            }
        }
    }, {
        '$out': '{collection}'
        }
'''
#aggregatetimer for all field-------------------------------------------------------------------------------------------
AggregationConfig["AggregateTimerView"]["allfieldquery"]='''{
    '$lookup': {
        'foreignField': 'user_id',
        'as': 'user_view',
        'from': 'UserView',
        'localField': 'user_id'
    }
}, {
    '$project': {
        'user_id': 1,
        'course_time': {
            '$sum': {
                '$map': {
                    'input': '$user_view',
                    'as': 'item',
                    'in': {
                        '$cond': [{'$eq': {school_year}}, '$$item.course_time', 0]
                    }
                }
            }
        },
        'pd_time': {
            '$sum': {
                '$map': {
                    'input': '$user_view',
                    'as': 'item',
                    'in': {
                        '$cond': [{'$eq': {school_year}}, '$$item.course_time', 0]
                    }
                }
            }
        },
        'portfolio_time': {
            '$sum': {
                '$map': {
                    'input': '$user_view',
                    'as': 'item',
                    'in': {
                        '$cond': [{'$eq': {school_year}},'$$item.portfolio_time', 0]}
                }
            }
        },
        'external_time': {
            '$sum': {
                '$map': {
                    'input': '$user_view',
                    'as': 'item',
                    'in': {
                        '$cond': [{'$eq': {school_year}},'$$item.external_time', 0]
                    }
                }
            }
        },
        'discussion_time': {
            '$sum': {
                '$map': {
                    'input': '$user_view',
                    'as': 'item',
                    'in': {
                        '$cond': [{'$eq': {school_year}}, '$$item.discussion_time', 0]}
                    }
                }
            }
        }
    }, {
        '$project': {
            'total_time': {'$add': ['$course_time', '$external_time', '$discussion_time', '$portfolio_time', '$pd_time']},
            'user_id': 1,
            'external_time': 1,
            'course_time': 1,
            'pd_time': 1,
            'portfolio_time': 1,
            'discussion_time': 1,
            'collaboration_time': {'$add': ['$discussion_time', '$portfolio_time']}
        }
    }, {
        '$group': {
            'total_time': {'$sum': '$total_time'},
            'discussion_time': { '$sum': '$discussion_time'},
            'external_time': {'$sum': '$external_time'},
            'course_time': {'$sum': '$course_time'},
            'pd_time': {'$sum': '$pd_time'},
            'portfolio_time': {'$sum': '$portfolio_time'},
            '_id': 'null',
            'collaboration_time': {'$sum': '$collaboration_time'}
            }
        }, {
            '$project': {
                'total_time': 1,
                'course_time': 1,
                'pd_time': 1,
                'portfolio_time': 1,
                'collaboration_time': 1,
                'external_time': 1,
                'discussion_time': 1
                }
            }, {
            '$group': {
                'total_time': {'$push': '$total_time'},
                'discussion_time': {'$push': '$discussion_time'},
                'external_time': {'$push': '$external_time'},
                'course_time': {'$push': '$course_time'},
                'pd_time': {'$push': '$pd_time'},
                'portfolio_time': {'$push': '$portfolio_time'},
                '_id': {
                    'total_time': '$total_time',
                    'course_time': '$course_time',
                    'pd_time': '$pd_time',
                    'portfolio_time': '$portfolio_time',
                    'collaboration_time': '$collaboration_time',
                    'external_time': '$external_time',
                    'discussion_time': '$discussion_time'
                },
                'collaboration_time': {'$push': '$collaboration_time'}
            }
        }, {
            '$project': {
                'total_time': {'$arrayElemAt': ['$total_time', 0]},
                'course_time': {'$arrayElemAt': ['$course_time', 0]},
                'pd_time': {'$arrayElemAt': ['$pd_time', 0]},
                'portfolio_time': {'$arrayElemAt': ['$portfolio_time', 0]},
                'collaboration_time': {'$arrayElemAt': ['$collaboration_time', 0]},
                'external_time': {'$arrayElemAt': ['$external_time', 0]},
                'discussion_time': {'$arrayElemAt': ['$discussion_time', 0]}
            }
        },
    {
        '$out': '{collection}'
    }
'''
#course for all field-------------------------------------------------------------------------------------------
AggregationConfig["CourseView"]["allfieldquery"] = '''{
    '$match': {'is_active': 1}
    }, {
        '$lookup': {
            'foreignField': 'user_id',
            'as': 'user_info',
            'from': 'user_info',
            'localField': 'user_id'}
        }, {
            '$project': {
                'course_id': 1,
                'state_id': '$user_info.state_id',
                'distric_id': '$user_info.distric_id',
                'user_id': 1,
                'school_id': '$user_info.school_id'
                }
            }, {
            '$lookup': {
                'foreignField': 'course_id',
                'as': 'course_info',
                'from': 'modulestore',
                'localField': 'course_id'
            }
        }, {
            '$lookup': {
            'foreignField': 'c_student_id',
            'as': 'studentmodule',
            'from': 'courseware_studentmodule',
            'localField': 'user_id'
            }
        }, {
            '$lookup': {
                'foreignField': 'user_id',
                'as': 'user_course_view',
                'from': 'UserCourseView',
                'localField': 'user_id'
            }
        }, {
            '$project': {
                'end_date': '$course_info.metadata.end',
                'complete_course': {
                    '$sum': {
                        '$map': {
                            'input': '$studentmodule',
                            'as': 'item',
                            'in': {
                                '$cond': [{'$and': [{'$eq': ['$$item.course_id', '$course_id']},
                                {'$eq': ['$$item.state.complete_course', True]}]}, 1, 0]
                                }
                            }
                        }
                    }, 
                    'external_time': {
                        '$sum': {
                            '$map': {
                                'input': '$user_course_view',
                                'as': 'item',
                                'in': {
                                    '$cond': [{'$and': [{'$eq': ['$$item.course_id', '$course_id']},
                                     {'$eq': {school_year}}]}, '$$item.external_time', 0]}
                                    }
                                }
                            },
                    'course_id': 1,
                    'discussion_time': {
                        '$sum': {
                            '$map': {
                                'input': '$user_course_view',
                                'as': 'item',
                                'in': {
                                    '$cond': [{'$and': [{'$eq': ['$$item.course_id', '$course_id']},
                                    {'$eq': {school_year}}]},'$$item.discussion_time', 0]
                                }
                            }
                        }
                    },
                    'course_name': '$course_info.metadata.display_name',
                    'course_time': {
                        '$sum': {
                            '$map': {
                                'input': '$user_course_view',
                                'as': 'item',
                                'in': {
                                    '$cond': [{'$and': [{'$eq': ['$$item.course_id', '$course_id']},
                                    {'$eq': {school_year}}]},
                                    '$$item.course_time', 0]
                                }
                            }
                        }
                    },
                    'course_run': '$course_info._id.org',
                    'portfolio_time': {
                        '$sum': {
                            '$map': {
                                'input': '$user_course_view',
                                'as': 'item',
                                'in': {'$cond': [{'$and': [{'$eq': ['$$item.course_id', '$course_id']},
                                {'$eq': {school_year}}]},
                                '$$item.portfolio_time', 0]
                                }
                            }
                        }
                    }, 
                    'course_number': '$course_info.metadata.display_coursenumber',
                    'organization': '$course_info.metadata.display_organization',
                    'start_date': '$course_info.metadata.start'
                    }
                }, {
                '$project': {
                    'total_time': {'$add': ['$course_time', '$external_time', '$discussion_time', '$portfolio_time']},
                    'course_time': 1,
                    'collaboration_time': {'$add': ['$discussion_time', '$portfolio_time']},
                    'complete_course': 1,
                    'external_time': 1,
                    'course_id': 1,
                    'discussion_time': 1,
                    'course_name': 1,
                    'end_date': 1,
                    'course_run': 1,
                    'portfolio_time': 1,
                    'course_number': 1,
                    'organization': 1,
                    'start_date': 1
                    }
                }, {
                    '$group': {
                        'total_time': {'$sum': '$total_time'},
                        'end_date': {
                            '$push': {'$arrayElemAt': ['$end_date', 0]}
                            },
                        'collaboration_time': {'$sum': '$collaboration_time'},
                        'complete_course': {'$sum': '$complete_course'},
                        'external_time': {'$sum': '$external_time'},
                        'discussion_time': {'$sum': '$discussion_time'},
                        'course_name': {
                            '$push': {'$arrayElemAt': ['$course_name', 0]}
                            },
                        'course_time': {'$sum': '$course_time'},
                        'course_run': {
                            '$push': {'$arrayElemAt': ['$course_run', 0]}
                        },
                        'portfolio_time': {'$sum': '$portfolio_time'},
                        'course_number': {
                            '$push': {'$arrayElemAt': ['$course_number', 0]}
                            },
                        'enrolled_course_num': {'$sum': 1},
                        'organization': {
                            '$push': {'$arrayElemAt': ['$organization', 0]}
                            },
                        '_id': '$course_id',
                        'start_date': {
                            '$push': {'$arrayElemAt': ['$start_date', 0]}
                        }
                    }
                }, {
                    '$project': {
                        'total_time': 1,
                        'course_time': 1,
                        'collaboration_time': 1,
                        'complete_course': 1,
                        'external_time': 1,
                        'discussion_time': 1,
                        'course_name': {'$arrayElemAt': ['$course_name', 0]},
                        'end_date':
                            {'$substr': [{'$cond': [{'$eq': ['$end_date', []]}, '', {'$arrayElemAt': ['$end_date', 0]}]}, 0, 10]},
                        'course_run': {'$arrayElemAt': ['$course_run', 0]}, 
                        'portfolio_time': 1,
                        'avg_course_time': {
                            '$ceil': {'$divide': ['$course_time', '$enrolled_course_num']}
                            }, 
                        'course_number': {'$arrayElemAt': ['$course_number', 0]},
                        'enrolled_course_num': 1, 
                        'organization': {'$arrayElemAt': ['$organization', 0]},
                        'start_date': {'$substr': [{'$arrayElemAt': ['$start_date', 0]}, 0, 10]}
                        }
                    }, {
                        '$project': {
                            'total_time': 1,
                            'course_time': 1,
                            'collaboration_time': 1,
                            'complete_course': {'$substr': ['$complete_course', 0, -1]},
                            'external_time': 1, 
                            'discussion_time': 1, 
                            'course_name': 1, 
                            'end_date': 1, 
                            'course_run': 1, 
                            'portfolio_time': 1, 
                            'avg_course_time': 1, 
                            'course_number': 1, 
                            'enrolled_course_num': {'$substr': ['$enrolled_course_num', 0, -1]}, 
                            'organization': 1, 'start_date': 1}
                        }, {
                            '$group': {
                                'total_time': {'$push': '$total_time'},
                                 '_id': {
                                    'total_time': '$total_time',
                                    'end_date': '$end_date', 
                                    'collaboration_time': '$collaboration_time', 
                                    'complete_course': '$complete_course', 
                                    'external_time': '$external_time', 
                                    'discussion_time': '$discussion_time', 
                                    'course_name': '$course_name', 
                                    'course_time': '$course_time', 
                                    'course_run': '$course_run', 
                                    'portfolio_time': '$portfolio_time', 
                                    'avg_course_time': '$avg_course_time', 
                                    'course_number': '$course_number', 
                                    'enrolled_course_num': '$enrolled_course_num', 
                                    'organization': '$organization', 
                                    'start_date': '$start_date'
                                },
                            'course_name': {'$push': '$course_name'}, 
                            'end_date': {'$push': '$end_date'},
                            'course_time': {'$push': '$course_time'}, 
                            'course_run': {'$push': '$course_run'}, 
                            'portfolio_time': {'$push': '$portfolio_time'}, 
                            'collaboration_time': {'$push': '$collaboration_time'}, 
                            'complete_course': {'$push': '$complete_course'}, 
                            'avg_course_time': {'$push': '$avg_course_time'}, 
                            'course_number': {'$push': '$course_number'}, 
                            'external_time': {'$push': '$external_time'}, 
                            'enrolled_course_num': {'$push': '$enrolled_course_num'}, 
                            'organization': {'$push': '$organization'}, 
                            'discussion_time': {'$push': '$discussion_time'}, 
                            'start_date': {'$push': '$start_date'}
                            }
                        }, {
                            '$project': {
                                'total_time': {'$arrayElemAt': ['$total_time', 0]},
                                'course_time': {'$arrayElemAt': ['$course_time', 0]}, 
                                'collaboration_time': {'$arrayElemAt': ['$collaboration_time', 0]}, 
                                'complete_course': {'$arrayElemAt': ['$complete_course', 0]}, 
                                'external_time': {'$arrayElemAt': ['$external_time', 0]}, 
                                'discussion_time': {'$arrayElemAt': ['$discussion_time', 0]}, 
                                'course_name': {'$arrayElemAt': ['$course_name', 0]}, 
                                'end_date': {'$arrayElemAt': ['$end_date', 0]}, 
                                'course_run': {'$arrayElemAt': ['$course_run', 0]}, 
                                'portfolio_time': {'$arrayElemAt': ['$portfolio_time', 0]}, 
                                'avg_course_time': {'$arrayElemAt': ['$avg_course_time', 0]}, 
                                'course_number': {'$arrayElemAt': ['$course_number', 0]}, 
                                'enrolled_course_num': {'$arrayElemAt': ['$enrolled_course_num', 0]}, 
                                'organization': {'$arrayElemAt': ['$organization', 0]}, 
                                'start_date': {'$arrayElemAt': ['$start_date', 0]}
                            }
                        }, {
                            '$out': '{collection}'
                            }
'''
#course assignments for all field-------------------------------------------------------------------------------------------
AggregationConfig["CourseAssignmentsView"]["allfieldquery"] = '''{
    '$match': {'q_course_id': {'$exists': True}
    }
}, {
    '$project': {
        'end_date': 1,
        'vertical_num': 1,
        'course_id': '$q_course_id',
        'display_name': '$metadata.display_name',
        'course_name': 1,
        'weight': {'$ifNull': ['$metadata.weight', 1]}, 
        'course_run': '$_id.org', 'sequential_name': 1, 
        'course_number': 1, 'organization': 1, 'start_date': 1
    }
}, {
    '$project': {
        'sequential_name': 1,
        'organization': 1,
        'course_name': 1,
        'weight': 1,
        'end_date': 1,
        'course_run': 1,
        'vertical_num': 1,
        'course_number': 1,
        'start_date': 1,
        'display_name': 1
    }
}, {
    '$group': {
        'end_date': {'$push': '$end_date'},
        'vertical_num': {'$push': '$vertical_num'},
        'display_name': {'$push': '$display_name'},
        'course_name': {'$push': '$course_name'},
        'weight': {'$push': '$weight'}, 
        'course_run': {'$push': '$course_run'},
        'sequential_name': {'$push': '$sequential_name'},
        'course_number': {'$push': '$course_number'},
        'organization': {'$push': '$organization'},
        '_id': {
            'organization': '$organization',
            'sequential_name': '$sequential_name',
            'vertical_num': '$vertical_num',
            'display_name': '$display_name',
            'end_date': '$end_date',
            'weight': '$weight',
            'course_run': '$course_run',
            'course_number': '$course_number',
            'course_name': '$course_name',
            'start_date': '$start_date'
        },
        'start_date': {'$push': '$start_date'}
    }
}, {
    '$project': {
        'sequential_name': {'$arrayElemAt': ['$sequential_name', 0]},
        'organization': {'$arrayElemAt': ['$organization', 0]},
        'course_name': {'$arrayElemAt': ['$course_name', 0]},
        'weight': {'$arrayElemAt': ['$weight', 0]},
        'end_date': {'$arrayElemAt': ['$end_date', 0]}, 
        'course_run': {'$arrayElemAt': ['$course_run', 0]}, 
        'vertical_num': {'$arrayElemAt': ['$vertical_num', 0]}, 
        'course_number': {'$arrayElemAt': ['$course_number', 0]}, 
        'start_date': {'$arrayElemAt': ['$start_date', 0]},
        'display_name': {'$arrayElemAt': ['$display_name', 0]}
    }
}, {
    '$out': '{collection}'
    }
'''
#pd planner for all field-------------------------------------------------------------------------------------------
AggregationConfig["PDPlannerView"]["allfieldquery"] = '''{school_year}{
    '$lookup': {
        'foreignField': 'key',
        'as': 'pegreg_student',
        'from': 'PepRegStudentView',
        'localField': 'key'
    }
}, {
    '$unwind': {
        'path': '$pegreg_student', 
        'preserveNullAndEmptyArrays': True
    }
}, {
    '$lookup': {
        'foreignField': 'user_id',
        'as': 'user_info',
        'from': 'user_info',
        'localField': 'pegreg_student.student_id'
    }
}, {
    '$project': {
        'pepper_course': 1,
        'training_time_end': 1,
        'user_create_id': 1,
        'user_district': {'$arrayElemAt': ['$user_info.district', 0]},
        'training_date': 1,
        'credits': 1,
        'user_school': {'$arrayElemAt': ['$user_info.school', 0]},
        'training_time_start': 1,
        'student': {'$arrayElemAt': ['$user_info.email', 0]},
        'user_id': '$pegreg_student.student_id',
        'max_registration': 1,
        'allow_registration': 1,
        'allow_validation': 1,
        'subject': 1,
        'classroom': 1,
        'date_create': 1,
        'school': 1,
        'allow_attendance': 1,
        'student_status': '$pegreg_student.student_status',
        'name': 1,
        'district': 1,
        'user_state': {'$arrayElemAt': ['$user_info.state', 0]},
        'description': 1,
        'instructor_status': '$pegreg_student.instructor_status',
        'district_id': 1,
        'training_id': 1,
        'geo_location': 1,
        'student_credit': '$pegreg_student.student_credit',
        'state_id': 1,
        'attendancel_id': 1,
        'type': 1,
        'school_id': {'$ifNull': [{'$arrayElemAt': ['$user_info.school_id', 0]}, '1']}
    }
}, {
    '$project': {
        'training_time_end': 1,
        'user_create_id': 1,
        'date_create': 1,
        'training_time_start': 1,
        'max_registration': 1,
        'allow_registration': 1,
        'subject': 1,
        'allow_validation': 1,
        'student_status': 1,
        'district': 1,
        'user_state': 1,
        'geo_location': 1,
        'instructor_status': 1,
        'type': 1, 
        'attendancel_id': 1,
        'pepper_course': 1,
        'description': 1,
        'user_district': 1,
        'training_date': 1,
        'credits': 1,
        'student': 1,
        'allow_attendance': 1,
        'student_credit': 1,
        'classroom': 1,
        'school': 1,
        'user_school': 1,
        'name': 1,
        'training_id': 1
    }
}, {
    '$group': {
        'training_time_end': {'$push': '$training_time_end'},
        'user_create_id': {'$push': '$user_create_id'}, 
        'date_create': {'$push': '$date_create'}, 
        'training_time_start': {'$push': '$training_time_start'}, 
        'max_registration': {'$push': '$max_registration'}, 
        'allow_registration': {'$push': '$allow_registration'}, 
        'subject': {'$push': '$subject'}, 
        'allow_attendance': {'$push': '$allow_attendance'}, 
        'student_status': {'$push': '$student_status'}, 
        'district': {'$push': '$district'}, 
        'user_state': {'$push': '$user_state'}, 
        'name': {'$push': '$name'}, 
        'geo_location': {'$push': '$geo_location'}, 
        'instructor_status': {'$push': '$instructor_status'},
        'type': {'$push': '$type'}, 
        'attendancel_id': {'$push': '$attendancel_id'}, 
        'pepper_course': {'$push': '$pepper_course'}, 
        'description': {'$push': '$description'}, 
        'training_date': {'$push': '$training_date'},
        'credits': {'$push': '$credits'}, 
        'student': {'$push': '$student'}, 
        'allow_validation': {'$push': '$allow_validation'},
        'user_district': {'$push': '$user_district'}, 
        'classroom': {'$push': '$classroom'}, 
        'school': {'$push': '$school'}, 
        'user_school': {'$push': '$user_school'}, 
        'student_credit': {'$push': '$student_credit'},
        'training_id': {'$push': '$training_id'},
        '_id': {
            'training_time_end': '$training_time_end',
            'user_create_id': '$user_create_id',
            'date_create': '$date_create',
            'training_time_start': '$training_time_start',
            'max_registration': '$max_registration',
            'allow_registration': '$allow_registration',
            'subject': '$subject',
            'allow_attendance': '$allow_attendance',
            'student_status': '$student_status',
            'district': '$district',
            'user_state': '$user_state',
            'name': '$name',
            'geo_location': '$geo_location',
            'instructor_status': '$instructor_status',
            'type': '$type',
            'attendancel_id': '$attendancel_id',
            'pepper_course': '$pepper_course',
            'description': '$description',
            'training_date': '$training_date',
            'credits': '$credits',
            'student': '$student',
            'allow_validation': '$allow_validation',
            'user_district': '$user_district',
            'classroom': '$classroom',
            'school': '$school', 
            'user_school': '$user_school',
            'student_credit': '$student_credit',
            'training_id': '$training_id'
        }
    }
}, {
    '$project': {
        'training_time_end': {'$arrayElemAt': ['$training_time_end', 0]},
        'user_create_id': {'$arrayElemAt': ['$user_create_id', 0]},
        'date_create': {'$arrayElemAt': ['$date_create', 0]},
        'training_time_start': {'$arrayElemAt': ['$training_time_start', 0]},
        'max_registration': {'$arrayElemAt': ['$max_registration', 0]},
        'allow_registration': {'$arrayElemAt': ['$allow_registration', 0]},
        'subject': {'$arrayElemAt': ['$subject', 0]},
        'allow_validation': {'$arrayElemAt': ['$allow_validation', 0]},
        'student_status': {'$arrayElemAt': ['$student_status', 0]},
        'district': {'$arrayElemAt': ['$district', 0]},
        'user_state': {'$arrayElemAt': ['$user_state', 0]},
        'geo_location': {'$arrayElemAt': ['$geo_location', 0]}, 
        'instructor_status': {'$arrayElemAt': ['$instructor_status', 0]},
        'type': {'$arrayElemAt': ['$type', 0]},
        'attendancel_id': {'$arrayElemAt': ['$attendancel_id', 0]}, 
        'pepper_course': {'$arrayElemAt': ['$pepper_course', 0]}, 
        'description': {'$arrayElemAt': ['$description', 0]}, 
        'user_district': {'$arrayElemAt': ['$user_district', 0]}, 
        'training_date': {'$arrayElemAt': ['$training_date', 0]}, 
        'credits': {'$arrayElemAt': ['$credits', 0]}, 
        'student': {'$arrayElemAt': ['$student', 0]}, 
        'allow_attendance': {'$arrayElemAt': ['$allow_attendance', 0]}, 
        'student_credit': {'$arrayElemAt': ['$student_credit', 0]}, 
        'classroom': {'$arrayElemAt': ['$classroom', 0]}, 
        'school': {'$arrayElemAt': ['$school', 0]}, 
        'user_school': {'$arrayElemAt': ['$user_school', 0]}, 
        'name': {'$arrayElemAt': ['$name', 0]}, 
        'training_id': {'$arrayElemAt': ['$training_id', 0]}
    }
}, {
    '$out': '{collection}'
    }
'''
#user for all field-------------------------------------------------------------------------------------------
AggregationConfig["UserView"]["allfieldquery"] = '''{school_year}{
    '$group': {
        'total_time': {'$sum': '$total_time'},
        'first_name': {'$last': '$first_name'},
        'last_name': {'$last': '$last_name'},
        'user_id': {'$last': '$user_id'},
        'course_time': {'$sum': '$course_time'},
        'district': {'$last': '$district'},
        'activate_date': {'$last': '$activate_date'},
        'portfolio_time': {'$sum': '$portfolio_time'},
        'pd_time': {'$sum': '$pd_time'},
        'school': {'$last': '$school'},
        'discussion_time': {'$sum': '$discussion_time'},
        'current_course': {'$last': '$current_course'},
        'complete_course': {'$last': '$complete_course'},
        'state': {'$last': '$state'},
        'external_time': {'$sum': '$external_time'},
        'subscription_status': {'$last': '$subscription_status'},
        'collaboration_time': {'$sum': '$collaboration_time'},
        '_id': '$user_id',
        'user_name': {'$last': '$user_name'},
        'email': {'$last': '$email'}
    }
}, {
    '$project': {
        'total_time': 1, 
        'first_name': 1, 
        'last_name': 1, 
        'user_id': 1, 
        'course_time': 1,
        'district': 1, 
        'activate_date': 1,
        'portfolio_time': 1, 
        'pd_time': 1, 
        'school': 1, 
        'collaboration_time': 1, 
        'current_course': 1, 
        'complete_course': 1, 
        'state': 1, 
        'external_time': 1, 
        'subscription_status': 1,
        'discussion_time': 1, 
        'user_name': 1, 
        'email': 1
    }
}, {
    '$project': {
        'total_time': 1,
        'first_name': 1,
        'discussion_time': 1,
        'district': 1,
        'course_time': 1,
        'activate_date': 1,
        'portfolio_time': 1,
        'pd_time': 1,
        'school': 1,
        'collaboration_time': 1,
        'complete_course': {'$substr': ['$complete_course', 0, -1]}, 
        'state': 1,
        'last_name': 1,
        'external_time': 1,
        'subscription_status': 1,
        'current_course': {'$substr': ['$current_course', 0, -1]},
        'user_name': 1,
        'email': 1
    }
}, {
    '$group': {
        'total_time': {'$push': '$total_time'},
        'first_name': {'$push': '$first_name'},
        'last_name': {'$push': '$last_name'},
        'course_time': {'$push': '$course_time'},
        'district': {'$push': '$district'},
        'activate_date': {'$push': '$activate_date'},
        '_id': {
            'total_time': '$total_time',
            'first_name': '$first_name',
            'last_name': '$last_name',
            'district': '$district',
            'course_time': '$course_time',
            'activate_date': '$activate_date',
            'portfolio_time': '$portfolio_time',
            'pd_time': '$pd_time',
            'school': '$school',
            'discussion_time': '$discussion_time',
            'current_course': '$current_course', 
            'complete_course': '$complete_course',
            'state': '$state',
            'external_time': '$external_time',
            'subscription_status': '$subscription_status',
            'collaboration_time': '$collaboration_time',
            'user_name': '$user_name',
            'email': '$email'
        },
        'portfolio_time': {'$push': '$portfolio_time'},
        'pd_time': {'$push': '$pd_time'},
        'school': {'$push': '$school'},
        'collaboration_time': {'$push': '$collaboration_time'},
        'current_course': {'$push': '$current_course'},
        'complete_course': {'$push': '$complete_course'},
        'state': {'$push': '$state'},
        'external_time': {'$push': '$external_time'},
        'subscription_status': {'$push': '$subscription_status'}, 
        'discussion_time': {'$push': '$discussion_time'},
        'user_name': {'$push': '$user_name'},
        'email': {'$push': '$email'}
    }
}, {
    '$project': {
        'total_time': {'$arrayElemAt': ['$total_time', 0]},
        'first_name': {'$arrayElemAt': ['$first_name', 0]},
        'discussion_time': {'$arrayElemAt': ['$discussion_time', 0]},
        'district': {'$arrayElemAt': ['$district', 0]},
        'course_time': {'$arrayElemAt': ['$course_time', 0]},
        'activate_date': {'$arrayElemAt': ['$activate_date', 0]},
        'portfolio_time': {'$arrayElemAt': ['$portfolio_time', 0]},
        'pd_time': {'$arrayElemAt': ['$pd_time', 0]},
        'school': {'$arrayElemAt': ['$school', 0]},
        'collaboration_time': {'$arrayElemAt': ['$collaboration_time', 0]},
        'complete_course': {'$arrayElemAt': ['$complete_course', 0]},
        'state': {'$arrayElemAt': ['$state', 0]},
        'last_name': {'$arrayElemAt': ['$last_name', 0]}, 
        'external_time': {'$arrayElemAt': ['$external_time', 0]},
        'subscription_status': {'$arrayElemAt': ['$subscription_status', 0]},
        'current_course': {'$arrayElemAt': ['$current_course', 0]},
        'user_name': {'$arrayElemAt': ['$user_name', 0]},
        'email': {'$arrayElemAt': ['$email', 0]
        }
    }
}, {
    '$out': '{collection}'
    }
'''
#usercourse for all field-------------------------------------------------------------------------------------------
AggregationConfig["UserCourseView"]["allfieldquery"] = '''{school_year}{
    '$group': {
        'last_name': {'$last': '$last_name'},
        'external_time': {'$sum': '$external_time'},
        'complete_date': {'$last': '$complete_date'},
        'course_id': {'$last': '$course_id'},
        'first_name': {'$last': '$first_name'},
        'user_id': {'$last': '$user_id'},
        'course_time': {'$sum': '$course_time'},
        'district': {'$last': '$district'},
        'course_run': {'$last': '$course_run'},
        'portfolio_time': {'$sum': '$portfolio_time'},
        'portfolio_url': {'$last': '$portfolio_url'},
        'state': {'$last': '$state'},
        'course_number': {'$last': '$course_number'},
        'subscription_status': {'$last': '$subscription_status'},
        'progress': {'$last': '$progress'},
        'user_name': {'$last': '$user_name'},
        'start_date': {'$last': '$start_date'},
        'total_time': {'$sum': '$total_time'},
        'end_date': {'$last': '$end_date'},
        'pd_time': {'$sum': '$pd_time'},
        'collaboration_time': {'$sum': '$collaboration_time'},
        'course_name': {'$last': '$course_name'},
        'discussion_time': {'$sum': '$discussion_time'},
        'school': {'$last': '$school'},
        'email': {'$last': '$email'},
        'enrollment_date': {'$last': '$enrollment_date'},
        'organization': {'$last': '$organization'},
        '_id': {'course_id': '$course_id', 'user_id': '$user_id'}
    }
}, {
    '$project': {
        'last_name': 1,
        'external_time': 1,
        'complete_date': 1,
        'course_id': 1,
        'first_name': 1,
        'user_id': 1,
        'course_time': 1,
        'district': 1,
        'course_run': 1,
        'portfolio_time': 1,
        'portfolio_url': 1, 
        'state': 1,
        'course_number': 1,
        'subscription_status': 1,
        'progress': 1,
        'user_name': 1,
        'start_date': 1,
        'total_time': 1,
        'end_date': 1,
        'pd_time': 1,
        'collaboration_time': 1,
        'course_name': 1,
        'discussion_time': 1,
        'school': 1, 
        'email': 1, 
        'enrollment_date': 1, 
        'organization': 1
    }
}, {
    '$project': {
        'last_name': 1,
        'external_time': 1,
        'first_name': 1,
        'course_name': 1,
        'end_date': 1,
        'district': 1,
        'course_run': 1,
        'portfolio_time': 1,
        'portfolio_url': 1,
        'state': 1, 
        'course_number': 1, 
        'subscription_status': 1, 
        'progress': {'$substr': ['$progress', 0, -1]}, 
        'user_name': 1, 
        'email': 1, 
        'total_time': 1, 
        'course_time': 1, 
        'pd_time': 1, 
        'collaboration_time': 1, 
        'complete_date': 1, 
        'discussion_time': 1, 
        'school': 1, 
        'start_date': 1, 
        'enrollment_date': 1, 
        'organization': 1
    }
}, {
    '$group': {
        'last_name': {'$push': '$last_name'},
        'external_time': {'$push': '$external_time'},
        'first_name': {'$push': '$first_name'},
        'course_name': {'$push': '$course_name'},
        'course_time': {'$push': '$course_time'}, 
        'district': {'$push': '$district'},
        'course_run': {'$push': '$course_run'},
        'portfolio_time': {'$push': '$portfolio_time'},
        'portfolio_url': {'$push': '$portfolio_url'},
        'state': {'$push': '$state'},
        'course_number': {'$push': '$course_number'},
        'subscription_status': {'$push': '$subscription_status'},
        'progress': {'$push': '$progress'},
        'user_name': {'$push': '$user_name'},
        'email': {'$push': '$email'},
        'total_time': {'$push': '$total_time'},
        'end_date': {'$push': '$end_date'},
        'pd_time': {'$push': '$pd_time'}, 
        'collaboration_time': {'$push': '$collaboration_time'},
        'complete_date': {'$push': '$complete_date'},
        'discussion_time': {'$push': '$discussion_time'},
        'school': {'$push': '$school'},
        'start_date': {'$push': '$start_date'},
        'enrollment_date': {'$push': '$enrollment_date'},
        'organization': {'$push': '$organization'},
        '_id': {'last_name': '$last_name',
        'external_time': '$external_time',
        'first_name': '$first_name',
        'course_name': '$course_name', 
        'course_time': '$course_time', 
        'district': '$district', 
        'course_run': '$course_run', 
        'portfolio_time': '$portfolio_time', 
        'portfolio_url': '$portfolio_url', 
        'state': '$state', 
        'course_number': '$course_number', 
        'subscription_status': '$subscription_status', 
        'progress': '$progress',
        'user_name': '$user_name', 
        'email': '$email',
        'total_time': '$total_time', 
        'end_date': '$end_date', 
        'pd_time': '$pd_time', 
        'collaboration_time': '$collaboration_time', 
        'complete_date': '$complete_date', 
        'discussion_time': '$discussion_time', 
        'school': '$school', 
        'start_date': '$start_date', 
        'enrollment_date': '$enrollment_date', 
        'organization': '$organization'
        }
    }
}, {
    '$project': {
        'last_name': {'$arrayElemAt': ['$last_name', 0]},
        'external_time': {'$arrayElemAt': ['$external_time', 0]},
        'first_name': {'$arrayElemAt': ['$first_name', 0]}, 
        'course_name': {'$arrayElemAt': ['$course_name', 0]}, 
        'end_date': {'$arrayElemAt': ['$end_date', 0]}, 
        'district': {'$arrayElemAt': ['$district', 0]}, 
        'course_run': {'$arrayElemAt': ['$course_run', 0]}, 
        'portfolio_time': {'$arrayElemAt': ['$portfolio_time', 0]}, 
        'portfolio_url': {'$arrayElemAt': ['$portfolio_url', 0]}, 
        'state': {'$arrayElemAt': ['$state', 0]}, 
        'course_number': {'$arrayElemAt': ['$course_number', 0]}, 
        'subscription_status': {'$arrayElemAt': ['$subscription_status', 0]}, 
        'progress': {'$arrayElemAt': ['$progress', 0]}, 
        'user_name': {'$arrayElemAt': ['$user_name', 0]}, 
        'email': {'$arrayElemAt': ['$email', 0]}, 
        'total_time': {'$arrayElemAt': ['$total_time', 0]}, 
        'course_time': {'$arrayElemAt': ['$course_time', 0]}, 
        'pd_time': {'$arrayElemAt': ['$pd_time', 0]}, 
        'collaboration_time': {'$arrayElemAt': ['$collaboration_time', 0]}, 
        'complete_date': {'$arrayElemAt': ['$complete_date', 0]}, 
        'discussion_time': {'$arrayElemAt': ['$discussion_time', 0]}, 
        'school': {'$arrayElemAt': ['$school', 0]}, 
        'start_date': {'$arrayElemAt': ['$start_date', 0]}, 
        'enrollment_date': {'$arrayElemAt': ['$enrollment_date', 0]}, 
        'organization': {'$arrayElemAt': ['$organization', 0]}
    }
}, {
    '$out': '{collection}'
    }
'''
# ----------------------------------------------------------------------------------------------------------------------------
get_create_int_column_headers = '''
    {
        "$group":{
            "_id":{"column_headers":"$column_headers"},
            "count":{"$sum":1},
            "total":{"$sum":"${aggregate_data}"}
        }
    },
    {
        "$out":"collection_column_header"
    }
'''

get_create_int_row_headers = '''
    {
        "$group":{
            "_id":{"row_headers":"$row_headers"},
            "count":{"$sum":1},
            "total":{"$sum":"${aggregate_data}"}
        }
    },
    {
        "$out":"collection_row_header"
    }
'''