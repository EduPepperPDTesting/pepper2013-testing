var db = connect("localhost:37017/reporting")

db.user_info.aggregate({
    $project: {
        user_id: 1,
        state_id: 1,
        district_id: 1,
        school_id: 1
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
        user_id: 1,
        course_time: {
            $sum: '$course_time.time'
        },
        external_time: {
            $sum: '$external_time.r_time'
        },
        discussion_time: {
            $sum: '$discussion_time.time'
        },
        portfolio_time: {
            $sum: '$portfolio_time.time'
        }
    }
}, {
    $project: {
        user_id: 1,
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
        _id: null,
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
        }
    }
}).forEach(function(collec) {
    printjson(collec);
})