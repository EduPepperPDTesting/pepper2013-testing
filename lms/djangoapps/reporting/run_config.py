RunConfig = {
    "new_user_info": {
        'origin_collection':'user_info'
    },
    "new_student_courseenrollment": {
        'origin_collection':'student_courseenrollment'
    },
    "new_courseware_studentmodule":{
        'origin_collection':'courseware_studentmodule'
    },
    "new_external_time":{
        'origin_collection':'external_time',
        'origin_collection1':'adjustment_time'
    },
    "new_pd_time":{
        'origin_collection':'pd_time'
    },
    "new_portfolio_time":{
        'origin_collection':'portfolio_time',
        'origin_collection1':'adjustment_time'
    },
    "new_discussion_time":{
        'origin_collection':'discussion_time',
        'origin_collection1':'adjustment_time'
    },
    "new_course_time":{
        'origin_collection':'course_time',
        'origin_collection1':'adjustment_time'
    },
}



RunConfig["new_user_info"]["query"] = '''
    {"$lookup": {"from": 'course_time',"localField": 'user_id',"foreignField": 'user_id',"as": 'course_time'}}, 
    {"$lookup": {"from": 'discussion_time',"localField": 'user_id',"foreignField": 'user_id',"as": 'discussion_time'}}, 
    {"$lookup": {"from": 'portfolio_time',"localField": 'user_id',"foreignField": 'user_id',"as": 'portfolio_time'}}, 
    {"$lookup": {"from": 'external_time',"localField": 'user_id',"foreignField": 'user_id',"as": 'external_time'}}, 
    {"$lookup": {"from": 'pd_time',"localField": 'user_id',"foreignField": 'user_id',"as": 'pd_time'}}, 
    {"$lookup": {"from": 'student_courseenrollment',"localField": 'user_id',"foreignField": 'user_id',"as": 'enrollment'}}, 
    {"$lookup": {"from": 'courseware_studentmodule',"localField": 'user_id',"foreignField": 'c_student_id',"as": 'studentmodule'}}, 
    {"$project": {
        "user_id": 1,"email": 1,"user_name": '$username',"first_name": 1,"last_name": 1,"state": 1,"cohort": 1,
        "district": 1,"school": 1,"activate_date": 1,"subscription_status": 1,"state_id": 1,"cohort_id": 1,"district_id": 1,
        "school_id": 1,"external_time": {"$sum": '$external_time.r_time'},"course_time": {"$sum": '$course_time.time'},
        "discussion_time": {"$sum": '$discussion_time.time'},"portfolio_time": {"$sum": '$portfolio_time.time'},
        "pd_time": {"$sum": '$pd_time.credit'},
        "current_course": {"$subtract":[{"$sum": {"$map": {"input": '$enrollment',"as": 'item',"in" : {"$cond": [{"$eq": ['$$item.is_active', 1]}, 1, 0]}}}},{"$sum": {"$map": {"input": '$studentmodule',"as": 'item',"in" : {"$cond": [{"$eq": ['$$item.state.complete_course', True]}, 1, 0]}}}}]},
        "complete_course":{"$sum": {"$map": {"input": '$studentmodule',"as": 'item',"in" : {"$cond": [{"$eq": ['$$item.state.complete_course', True]}, 1, 0]}}}}}},{"$project": {"user_id": 1,"email": 1,"user_name": 1,"first_name": 1,"last_name": 1,"state": 1,"cohort": 1,"district": 1,"school": 1,"state_id": 1,"cohort_id" : 1,"district_id": 1,"school_id": 1,"activate_date": 1,"subscription_status": 1,"current_course": 1,"complete_course": 1,"course_time":1,"external_time": 1,"discussion_time": 1, "portfolio_time": 1,"pd_time": 1,"collaboration_time": {"$add": ['$discussion_time', '$portfolio_time']},"total_time": {"$add": ['$course_time', '$external_time', '$discussion_time', '$portfolio_time', '$pd_time']},
        "school_year":{"$substr": [ "current", 0, -1 ]}
        }
    }'''
