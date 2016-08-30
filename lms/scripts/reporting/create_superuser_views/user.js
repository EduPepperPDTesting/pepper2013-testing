// var db = connect("localhost:27018/reporting")

db.UserView.remove({'school_year':'current'});
db.user_info.aggregate({
    $lookup: {
        from: 'course_time',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'course_time'
    }
}, {
    $lookup: {
        from: 'discussion_time',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'discussion_time'
    }
}, {
    $lookup: {
        from: 'portfolio_time',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'portfolio_time'
    }
}, {
    $lookup: {
        from: 'external_time',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'external_time'
    }
}, {
    $lookup: {
        from: 'pd_time',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'pd_time'
    }
}, {
    $lookup: {
        from: 'student_courseenrollment',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'enrollment'
    }
}, {
    $lookup: {
        from: 'courseware_studentmodule',
        localField: 'user_id',
        foreignField: 'c_student_id',
        as: 'studentmodule'
    }
}, {
    $project: {
        user_id: 1,
        email: 1,
        user_name: '$username',
        first_name: 1,
        last_name: 1,
        state: 1,
        district: 1,
        school: 1,
        activate_date: 1,
        subscription_status: 1,
        state_id: 1,
        district_id: 1,
        school_id: 1,
        external_time: {
            $sum: '$external_time.r_time'
        },
        course_time: {
            $sum: '$course_time.time'
        },
        discussion_time: {
            $sum: '$discussion_time.time'
        },
        portfolio_time: {
            $sum: '$portfolio_time.time'
        },
        pd_time: {
            $sum: '$pd_time.credit'
        },
        current_course: {
            $sum: {
                $map: {
                    input: '$enrollment',
                    as: 'item',
                    in : {
                        $cond: [{
                            $eq: ['$$item.is_active', 1]
                        }, 1, 0]
                    }
                }
            }
        },
        complete_course: {
            $sum: {
                $map: {
                    input: '$studentmodule',
                    as: 'item',
                    in : {
                        $cond: [{
                            $eq: ['$$item.state.complete_course', true]
                        }, 1, 0]
                    }
                }
            }
        }
    }
}, {
    $project: {
        user_id: 1,
        email: 1,
        user_name: 1,
        first_name: 1,
        last_name: 1,
        state: 1,
        district: 1,
        school: 1,
        state_id: 1,
        district_id: 1,
        school_id: 1,
        activate_date: 1,
        subscription_status: 1,
        current_course: 1,
        complete_course: 1,
        course_time:1,
        external_time: 1,
        discussion_time: 1,
        portfolio_time: 1,
        pd_time: 1,
        collaboration_time: {
            $add: ['$discussion_time', '$portfolio_time']
        },
        total_time: {
            $add: ['$course_time', '$external_time', '$discussion_time', '$portfolio_time', '$pd_time']
        },
        school_year:{$substr: [ "current", 0, -1 ]}
    }
}).forEach(function(x){
    delete x._id;
    db.UserView.save(x);
})
