// var db = connect("localhost:27018/reporting")

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
        email: {
            $arrayElemAt: ['$user_info.email', 0]
        },
        user_name: {
            $arrayElemAt: ['$user_info.username', 0]
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
        state_id: '$user_info.state_id',
        district_id: '$user_info.district_id',
        school_id: '$user_info.school_id'
    }
}, {
    $lookup: {
        from: 'modulestore',
        localField: 'course_id',
        foreignField: 'q_course_id',
        as: 'question_info'
    }
}, {
    $unwind: '$question_info'
}, {
    $project: {
        _id: 0,
        user_id: 1,
        email: 1,
        user_name: 1,
        state: 1,
        district: 1,
        school: 1,
        course_id: '$question_info.q_course_id',
        course_number: '$question_info.course_number',
        course_name: '$question_info.course_name',
        course_run: '$question_info._id.org',
        start: '$question_info.start_date',
        end: '$question_info.end_date',
        organization: '$question_info.organization',
        sequential_name: '$question_info.sequential_name',
        vertical_num: '$question_info.vertical_num',
        display_name: '$question_info.metadata.display_name',
        module_id: '$question_info.module_id'
    }
}, {
    $lookup: {
        from: 'problem_point',
        localField: 'module_id',
        foreignField: 'module_id',
        as: 'problem_point'
    }
}, {
    $project: {
        email: 1,
        user_name: 1,
        state: 1,
        district: 1,
        school: 1,
        course_number: 1,
        course_name: 1,
        course_run: 1,
        start: 1,
        end: 1,
        organization: 1,
        sequential_name: 1,
        vertical_num: 1,
        display_name: 1,
        point: {
            $sum: {
                $map: {
                    input: '$problem_point',
                    as: 'item',
                    in : {
                        $cond: [{
                            $eq: ['$$item.user_id', '$user_id']
                        }, '$$item.point', 0]
                    }
                }
            }
        }
    }
},{$out:'AggregateGradesView'})
