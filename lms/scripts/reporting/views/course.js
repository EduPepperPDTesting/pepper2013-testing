var db = connect("localhost:37017/reporting")

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
        state_id: '$user_info.state_id',
        distric_id: '$user_info.distric_id',
        school_id: '$user_info.school_id',
    }
}, {
    $match: {
        'school_id': 14
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
        localField: 'user_id',
        foreignField: 'c_student_id',
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
    $project: {
        course_id: 1,
        complete_course: {
            $sum: {
                $map: {
                    input: '$studentmodule',
                    as: 'item',
                    in : {
                        $cond: [{
                            $and: [{
                                $eq: ['$$item.course_id', '$course_id']
                            }, {
                                $eq: ['$$item.state.complete_course', true]
                            }]
                        }, 1, 0]
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
        course_number: '$course_info.metadata.display_coursenumber',
        course_name: '$course_info.metadata.display_name',
        course_run: '$course_info._id.org',
        start_date: '$course_info.metadata.start',
        end_date: '$course_info.metadata.end',
        organization: '$course_info.metadata.display_organization'
    }
}, {
    $project: {
        course_id: 1,
        course_number: 1,
        course_name: 1,
        course_run: 1,
        start_date: 1,
        end_date: 1,
        organization: 1,
        complete_course: 1,
        course_time: 1,
        external_time: 1,
        discussion_time: 1,
        portfolio_time: 1,
        collaboration_time: {
            $add: ['$discussion_time', '$portfolio_time']
        },
        total_time: {
            $add: ['$course_time', '$external_time', '$discussion_time', '$portfolio_time']
        }
    }
}, {
    $group: {
        '_id': '$course_id',

        course_number: {
            $push: {
                $arrayElemAt: ['$course_number', 0]
            }
        },
        course_name: {
            $push: {
                $arrayElemAt: ['$course_name', 0]
            }
        },
        enrolled_course_num: {
            $sum: 1
        },
        course_run: {
            $push: {
                $arrayElemAt: ['$course_run', 0]
            }
        },
        start_date: {
            $push: {
                $arrayElemAt: ['$start_date', 0]
            }
        },
        end_date: {
            $push: {
                $arrayElemAt: ['$end_date', 0]
            }
        },
        organization: {
            $push: {
                $arrayElemAt: ['$organization', 0]
            }
        },
        complete_course: {
            $sum: '$complete_course'
        },
        course_time: {
            $sum: '$course_time'

        },
        external_time: {
            $sum: '$external_time'
        },
        discussion_time: {
            $sum: '$discussion_time'
        },
        portfolio_time: {
            $sum: '$portfolio_time'
        },
        collaboration_time: {
            $sum: '$collaboration_time'
        },
        total_time: {
            $sum: '$total_time'
        },
    }
}, {
    $project: {
        complete_course: 1,
        enrolled_course_num: 1,
        course_time: 1,
        external_time: 1,
        discussion_time: 1,
        portfolio_time: 1,
        collaboration_time: 1,
        total_time: 1,
        course_number: {
            $arrayElemAt: ['$course_number', 0]
        },
        course_name: {
            $arrayElemAt: ['$course_name', 0]
        },
        course_run: {
            $arrayElemAt: ['$course_run', 0]
        },
        start_date: {
            $substr: [{
                $arrayElemAt: ['$start_date', 0]
            }, 0, 10]
        },
        end_date: {
            $substr: [{
                $cond: [{
                    $eq: ['$end_date', []]
                }, '', {
                    $arrayElemAt: ['$end_date', 0]
                }]
            }, 0, 10]
        },
        organization: {
            $arrayElemAt: ['$organization', 0]
        },
        avg_course_time: {
            $ceil: {
                $divide: ['$course_time', '$enrolled_course_num']
            }
        }
    }
}, {
    $skip: 0
}, {
    $limit: 20
}).forEach(function(collec) {
    printjson(collec);
})