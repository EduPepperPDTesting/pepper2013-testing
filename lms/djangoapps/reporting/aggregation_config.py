
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
    },
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
                        }, "$$item.external_time", 0]
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
