
# -----------------------------------
# Aggregation config
# -----------------------------------


# definition aggregation:

AggregationConfig = {
    "UserView": {
        "collection": "user_info"
    },
    "UserCourseView": {
        "collection": "student_courseenrollment"
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
    }
}

# aggregation query:  (*placeholder: {user_domain}, {display_columns}, {filters}, {distinct})

#  user -------------------------------------------------------------------------------

AggregationConfig["UserView"]["query"] = '''{user_domain}
    {
    "$lookup": {
        "from": "course_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "course_time"
    }
}, {
    "$lookup": {
        "from": "discussion_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "discussion_time"
    }
}, {
    "$lookup": {
        "from": "portfolio_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "portfolio_time"
    }
}, {
    "$lookup": {
        "from": "external_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "external_time"
    }
}, {
    "$lookup": {
        "from": "student_courseenrollment",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "enrollment"
    }
}, {
    "$lookup": {
        "from": "courseware_studentmodule",
        "localField": "user_id",
        "foreignField": "c_student_id",
        "as": "studentmodule"
    }
}, {
    "$project": {
        "user_id": 1,
        "email": 1,
        "user_name": "$username",
        "first_name": 1,
        "last_name": 1,
        "state": 1,
        "district": 1,
        "school": 1,
        "activate_date": 1,
        "subscription_status": 1,
        "external_time": {
            "$sum": "$external_time.r_time"
        },
        "course_time": {
            "$sum": "$course_time.time"
        },
        "discussion_time": {
            "$sum": "$discussion_time.time"
        },
        "portfolio_time": {
            "$sum": "$portfolio_time.time"
        },
        "current_course": {
            "$sum": {
                "$map": {
                    "input": "$enrollment",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.is_active", 1]
                        }, 1, 0]
                    }
                }
            }
        },
        "complete_course": {
            "$sum": {
                "$map": {
                    "input": "$studentmodule",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.state.complete_course", True]
                        }, 1, 0]
                    }
                }
            }
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
        "collaboration_time": {
            "$add": ["$discussion_time", "$portfolio_time"]
        },
        "total_time": {
            "$add": ["$course_time", "$external_time", "$discussion_time", "$portfolio_time"]
        }
    }
}{filters}{display_columns}{distinct}
'''

# user course -------------------------------------------------------------------------------

AggregationConfig["UserCourseView"]["query"] = '''{user_domain}{
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
        "enrollment_date": {
            "$substr": ["$created", 0, 10]
        },
        "user_name": {
            "$arrayElemAt": ["$user_info.username", 0]
        },
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
        "subscription_status": {
            "$arrayElemAt": ["$user_info.subscription_status", 0]
        },
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
        "localField": "course_id",
        "foreignField": "c_course_id",
        "as": "studentmodule"
    }
}, {
    "$lookup": {
        "from": "course_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "course_time"
    }
}, {
    "$lookup": {
        "from": "discussion_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "discussion_time"
    }
}, {
    "$lookup": {
        "from": "portfolio_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "portfolio_time"
    }
}, {
    "$lookup": {
        "from": "external_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "external_time"
    }
}, {
    "$lookup": {
        "from": "user_course_progress",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "user_progress"
    }
}, {
    "$project": {
        "user_id": 1,
        "course_id": 1,
        "user_progress": 1,
        "email": 1,
        "user_name": 1,
        "state": 1,
        "district": 1,
        "school": 1,
        "subscription_status": 1,
        "enrollment_date": 1,
        "course_number": {
            "$arrayElemAt": ["$course_info.metadata.display_coursenumber", 0]
        },
        "course_name": {
            "$arrayElemAt": ["$course_info.metadata.display_name", 0]
        },
        "course_run": {
            "$arrayElemAt": ["$course_info._id.org", 0]
        },
        "start_date": {
            "$substr": [{
                "$arrayElemAt": ["$course_info.metadata.start", 0]
            }, 0, 10]
        },
        "end_date": {
            "$substr": [{
                "$cond": [{
                    "$eq": ["$course_info.metadata.end", []]
                }, "", {
                    "$arrayElemAt": ["$course_info.metadata.end", 0]
                }]
            }, 0, 10]
        },
        "organization": {
            "$arrayElemAt": ["$course_info.metadata.display_organization", 0]
        },
        "cur_studentmodule": {
            "$filter": {
                "input": "$studentmodule",
                "as": "item",
                "cond": {
                    "$eq": ["$$item.student_id", "$user_id"]
                }

            }
        },
        "portfolio_url": {
            "$concat": ["/courses/", "$course_id", "/portfolio/about_me/", {
                "$substr": ["$user_id", 0, -1]
            }]
        },
        "course_time": {
            "$sum": {
                "$map": {
                    "input": "$course_time",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.course_id", "$course_id"]
                        }, "$$item.time", 0]
                    }
                }
            }
        },
        "external_time": {
            "$sum": {
                "$map": {
                    "input": "$external_time",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.course_id", "$course_id"]
                        }, "$$item.r_time", 0]
                    }
                }
            }
        },
        "discussion_time": {
            "$sum": {
                "$map": {
                    "input": "$discussion_time",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.course_id", "$course_id"]
                        }, "$$item.time", 0]
                    }
                }
            }
        },
        "portfolio_time": {
            "$sum": "$portfolio_time.time"
        },
        "progress": {
            "$sum": {
                "$map": {
                    "input": "$user_progress",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.course_id", "$course_id"]
                        }, "$$item.progress", 0]
                    }
                }
            }

        }
    }
}, {
    "$project": {
        "user_id": 1,
        "course_id": 1,
        "email": 1,
        "user_name": 1,
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
        "complete_date": {
            "$substr": [{
                "$arrayElemAt": ["$cur_studentmodule.state.complete_date", 0]
            }, 0, 10]
        },
        "portfolio_url": 1,
        "progress": {
            "$concat": [{
                "$substr": ["$progress", 0, -1]
            }, "%"]
        },
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
        "from": "course_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "course_time"
    }
}, {
    "$lookup": {
        "from": "discussion_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "discussion_time"
    }
}, {
    "$lookup": {
        "from": "portfolio_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "portfolio_time"
    }
}, {
    "$lookup": {
        "from": "external_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "external_time"
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
                    "input": "$external_time",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.course_id", "$course_id"]
                        }, "$$item.r_time", 0]
                    }
                }
            }
        },
        "course_time": {
            "$sum": {
                "$map": {
                    "input": "$course_time",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.course_id", "$course_id"]
                        }, "$$item.time", 0]
                    }
                }
            }
        },
        "discussion_time": {
            "$sum": {
                "$map": {
                    "input": "$discussion_time",
                    "as": "item",
                    "in": {
                        "$cond": [{
                            "$eq": ["$$item.course_id", "$course_id"]
                        }, "$$item.time", 0]
                    }
                }
            }
        },
        "portfolio_time": {
            "$sum": "$portfolio_time.time"
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
        "from": "course_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "course_time"
    }
}, {
    "$lookup": {
        "from": "discussion_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "discussion_time"
    }
}, {
    "$lookup": {
        "from": "portfolio_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "portfolio_time"
    }
}, {
    "$lookup": {
        "from": "external_time",
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "external_time"
    }
}, {
    "$project": {
        "user_id": 1,
        "course_time": {
            "$sum": "$course_time.time"
        },
        "external_time": {
            "$sum": "$external_time.r_time"
        },
        "discussion_time": {
            "$sum": "$discussion_time.time"
        },
        "portfolio_time": {
            "$sum": "$portfolio_time.time"
        }
    }
}, {
    "$project": {
        "user_id": 1,
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
        }
    }
}{filters}{display_columns}{distinct}'''
