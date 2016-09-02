// var db = connect("localhost:27018/reporting")

db.UserCourseView.remove({'school_year':'current'});
db.student_courseenrollment.aggregate({
    $match: {
        'is_active': 1
    }
}, {
    $lookup: {
        from: 'user_info',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'user_info'
    }
}, {
    $project: {
        user_id: 1,
        course_id: 1,
        enrollment_date: {
            $substr: ['$created', 0, 10]
        },
        user_name: {
            $arrayElemAt: ['$user_info.username', 0]
        },
        email: {
            $arrayElemAt: ['$user_info.email', 0]
        },
        first_name: {
            $arrayElemAt: ['$user_info.first_name', 0]
        },
        last_name: {
            $arrayElemAt: ['$user_info.last_name', 0]
        },
        state: {
            $arrayElemAt: ['$user_info.state', 0]
        },
        district: {
            $arrayElemAt: ['$user_info.district', 0]
        },
        school: {
            $arrayElemAt: ['$user_info.school', 0]
        },
        subscription_status: {
            $arrayElemAt: ['$user_info.subscription_status', 0]
        },
        state_id: 1,
        district_id: 1,
        school_id: 1,
    }
}, {
    $lookup: {
        from: 'modulestore',
        localField: 'course_id',
        foreignField: 'course_id',
        as: 'course_info'
    }
}, {
    $lookup: {
        from: 'courseware_studentmodule',
        localField: 'course_id',
        foreignField: 'c_course_id',
        as: 'studentmodule'
    }
}, {
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
        from: 'user_course_progress',
        localField: 'user_id',
        foreignField: 'user_id',
        as: 'user_progress'
    }
}, {
    $project: {
        user_id: 1,
        course_id: 1,
        user_progress: 1,
        email: 1,
        user_name: 1,
        first_name: 1,
        last_name: 1,
        state: 1,
        district: 1,
        school: 1,
        subscription_status: 1,
        enrollment_date: 1,
        state_id: 1,
        district_id: 1,
        school_id: 1,
        course_number: {
            $arrayElemAt: ['$course_info.metadata.display_coursenumber', 0]
        },
        course_name: {
            $arrayElemAt: ['$course_info.metadata.display_name', 0]
        },
        course_run: {
            $arrayElemAt: ['$course_info._id.org', 0]
        },
        start_date: {
            $substr: [{
                $arrayElemAt: ['$course_info.metadata.start', 0]
            }, 0, 10]
        },
        end_date: {
            $substr: [{
                $cond: [{
                    $eq: ['$course_info.metadata.end', []]
                }, '', {
                    $arrayElemAt: ['$course_info.metadata.end', 0]
                }]
            }, 0, 10]
        },
        organization: {
            $arrayElemAt: ['$course_info.metadata.display_organization', 0]
        },
        cur_studentmodule: {
            $filter: {
                input: '$studentmodule',
                as: 'item',
                cond: {
                    $eq: ['$$item.student_id', '$user_id']
                }

            }
        },
        portfolio_url: {
            $concat: ['/courses/', '$course_id', '/portfolio/about_me/', {
                $substr: ['$user_id', 0, -1]
            }]
        },
        course_time: {
            $sum: {
                $map: {
                    input: '$course_time',
                    as: 'item',
                    in : {
                        $cond: [{
                            $eq: ['$$item.course_id', '$course_id']
                        }, '$$item.time', 0]
                    }
                }
            }
        },
        external_time: {
            $sum: {
                $map: {
                    input: '$external_time',
                    as: 'item',
                    in : {
                        $cond: [{
                            $eq: ['$$item.course_id', '$course_id']
                        }, '$$item.r_time', 0]
                    }
                }
            }
        },
        discussion_time: {
            $sum: {
                $map: {
                    input: '$discussion_time',
                    as: 'item',
                    in : {
                        $cond: [{
                            $eq: ['$$item.course_id', '$course_id']
                        }, '$$item.time', 0]
                    }
                }
            }
        },
        portfolio_time: {
            $sum: '$portfolio_time.time'
        },
        pd_time: {
            $sum: '$pd_time.credit'
        },
        progress: {
            $sum: {
                $map: {
                    input: '$user_progress',
                    as: 'item',
                    in : {
                        $cond: [{
                            $eq: ['$$item.course_id', '$course_id']
                        }, '$$item.progress', 0]
                    }
                }
            }

        }
    }
}, {
    $project: {
        user_id: 1,
        course_id: 1,
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
        subscription_status: 1,
        course_number: 1,
        course_name: 1,
        course_run: 1,
        start_date: 1,
        end_date: 1,
        organization: 1,
        enrollment_date: 1,
        complete_date: {
            $substr: [{
                $arrayElemAt: ['$cur_studentmodule.state.complete_date', 0]
            }, 0, 10]
        },
        portfolio_url: 1,
        progress: 1,
        course_time: 1,
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
    db.UserCourseView.save(x);
})
