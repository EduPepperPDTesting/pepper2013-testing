// var db = connect("localhost:27018/reporting")

db.modulestore.aggregate({
    $match: {
        'q_course_id': {
            $exists: true
        }
    }
}, {
    $project: {
        course_id: '$q_course_id',
        course_number: 1,
        course_name: 1,
        course_run: '$_id.org',
        start: 1,
        end: 1,
        organization: 1,
        sequential_name: 1,
        vertical_num: 1,
        display_name: '$metadata.display_name',
        weight: {
            $ifNull: ['$metadata.weight', 1]
        }
    }
},{$out:'CourseAssignmentsView'})
