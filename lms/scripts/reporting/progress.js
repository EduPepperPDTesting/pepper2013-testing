// var db = connect("localhost:27018/reporting")
db.user_course_progress.remove({})
db.problem_point.remove({})
var modulestore = [];

function x_children(item, subsectionInfo) {
    var subsection_name = '';
    var unit_number = 0;
    if (item._id.category == 'sequential') {
        var score = 0;
        var weight = 0;
        print(item._id.category, item._id.name)
        subsectionInfo.subsection_name = item.metadata.display_name;
        if (item.metadata.graded != true && item.metadata.graded != 'true') {
            return
        }
    }
    if (item.definition.children != undefined && item.definition.children.length > 0) {
        for (var i = 0; i < item.definition.children.length; i++) {
            try {
                var arr = item.definition.children[i].split('/');
                if (modulestore[item.definition.children[i]] != undefined) {
                    var c = modulestore[item.definition.children[i]];
                } else {
                    var c = db.modulestore.findOne({
                        '_id.course': arr[3],
                        '_id.category': arr[4],
                        '_id.name': arr[5]
                    });
                }
                if (arr[4] == 'vertical') {
                    subsectionInfo.unit_number = i + 1;
                }
                if (c != null) {
                    x_children(c, subsectionInfo);
                }
            } catch (e) {}
        }
    } else {
        if (item._id.category == 'problem') {
            print('^^^^^^^^^', subsectionInfo.subsection_name, subsectionInfo.unit_number);

            print(item._id.category, item._id.name)
            var _id = item._id;
            var module_id = _id.tag + '://' + _id.org + '/' + _id.course + '/' + _id.category + '/' + _id.name;
            if (modulestore[module_id] == undefined) {
                item.q_course_id = subsectionInfo.course_id;
                item.sequential_name = subsectionInfo.subsection_name;
                item.vertical_num = subsectionInfo.unit_number;
                item.course_number = subsectionInfo.course_number;
                item.course_name = subsectionInfo.course_name;
                item.start_date = subsectionInfo.start_date;
                item.end_date = subsectionInfo.end_date;
                item.organization = subsectionInfo.organization;
                item.module_id = module_id;
                db.modulestore.save(item);
                modulestore[module_id] = item;
            }

        } else if (item._id.category == 'combinedopenended') {
            print('^^^^^^^^^', subsectionInfo.subsection_name, subsectionInfo.unit_number);
            print(item._id.category, item._id.name)
            var _id = item._id;
            var module_id = _id.tag + '://' + _id.org + '/' + _id.course + '/' + _id.category + '/' + _id.name;
            if (modulestore[module_id] == undefined) {
                item.q_course_id = subsectionInfo.course_id;
                item.sequential_name = subsectionInfo.subsection_name;
                item.vertical_num = subsectionInfo.unit_number;
                item.course_number = subsectionInfo.course_number;
                item.course_name = subsectionInfo.course_name;
                item.start_date = subsectionInfo.start_date;
                item.end_date = subsectionInfo.end_date;
                item.organization = subsectionInfo.organization;
                item.module_id = module_id;
                db.modulestore.save(item);
                modulestore[module_id] = item;
            }
        }
    }
}
var chapterScore = [];
var module_problem = [];
var subsectionInfo = {};
var course_num = 0;

db.modulestore.find({
    '_id.category': 'course',
    '_id.revision': null
}).forEach(function(x) {
    subsectionInfo.course_id = x.course_id;
    subsectionInfo.course_number = x.metadata.display_coursenumber;
    subsectionInfo.course_name = x.metadata.display_name;
    subsectionInfo.start_date = x.metadata.start != undefined ? x.metadata.start.substr(0, 10) : '';
    subsectionInfo.end_date = x.metadata.end != undefined ? x.metadata.end.substr(0, 10) : '';
    subsectionInfo.organization = x.metadata.display_organization;
    x_children(x, subsectionInfo);
    course_num++;
    print('--------------------------------------------------------------------', course_num);
})


var student_course_num = 1;
//db.student_courseenrollment.find({'is_active':1,'user_id':125,'course_id':'MPY/DC102/S2016'}).noCursorTimeout().forEach(function(sc){
db.student_courseenrollment.find({
    'is_active': 1
}).noCursorTimeout().forEach(function(sc) {
    print('--------------------------------------------------------------------', student_course_num);
    chapterScore = []
    if (module_problem[sc.course_id] == undefined) {
        module_problem[sc.course_id] = db.modulestore.aggregate([{
            $match: {
                q_course_id: {
                    $exists: true
                },
                q_course_id: sc.course_id
            }
        }, {
            $group: {
                _id: {
                    'course_id': '$q_course_id',
                    's_n': '$sequential_name'
                },
                module_id: {
                    $push: '$module_id'
                },
                module_weight: {
                    $push: {
                        $ifNull: ['$metadata.weight', 1]
                    }
                },
                weight: {
                    $sum: {
                        $ifNull: ['$metadata.weight', 1]
                    }
                }
            }
            //},{'$sort':{'_id.s_n':1}}
        }]);
    }
    module_problem[sc.course_id]._batch.forEach(function(item) {
        var i = 0;
        chapterScore.push({
            weight: item.weight,
            score: 0
        });
        item.module_id.forEach(function(id) {
            var score = 0;
            try {
                var module = db.courseware_studentmodule.findOne({
                    'student_id': sc.user_id,
                    'module_id': id,
                    'course_id': sc.course_id
                });
                if (module.module_type == 'problem') {
                    //var temp_id = id.split('/')
                    //correct_map_id ='i4x'+temp_id[1]+'-'+temp_id[2]+'-'+temp_id[3]+'-'+temp_id[4]+'-'+temp_id[5]+'_2_1';          
                    if (module.grade != 'NULL') {
                        print(module.module_id + "+++++")
                        if (item.module_weight[i] > 0) {
                            //score = item.module_weight[i];
                            score = module.grade;
                        } else {
                            print(module.module_id + "-----")
                            score = 0;
                        }
                        chapterScore[chapterScore.length - 1].score += score;
                    } else {
                        print(module.module_id + "-----")
                        score = 0;
                    }
                    //module.point = score;
                    // db.courseware_studentmodule.save(module);
                    set_problem_point(module.module_id, module.student_id, module.course_id, score);
                    //printjson(item.module_weight[i])

                } else if (module.module_type == 'combinedopenended') {
                    var task_states = JSON.parse(module.state.task_states[0]);
                    if (task_states.child_history.length > 0) {
                        score = item.module_weight[i];
                        chapterScore[chapterScore.length - 1].score += score;
                    } else {
                        score = 0;
                    }
                    //module.point = score;
                    //db.courseware_studentmodule.save(module);
                    set_problem_point(module.module_id, module.student_id, module.course_id, score);
                }
                i++;
            } catch (e) {
                if (module != null) {
                    //module.point = score;
                    //db.courseware_studentmodule.save(module);
                    set_problem_point(module.module_id, module.student_id, module.course_id, score);
                }
            }
        })
    })
    var total_number = 0;
    var sum_progress = 0;
    for (var i = 0; i < chapterScore.length; i++) {
        print(chapterScore[i].weight, chapterScore[i].score);
        var sequential_progress = chapterScore[i].weight > 0 ? Math.round(chapterScore[i].score / chapterScore[i].weight * 100) : 0;
        sum_progress += sequential_progress;
        print('sequential_progress', sequential_progress)
        if (chapterScore[i].weight > 0) {
            total_number++;
        }
    }
    if (total_number > 0) {
        var progress = Math.round(sum_progress / total_number);
        print('sum_progress', sum_progress);
        print('course_progress', Math.round(sum_progress / total_number));
        db.user_course_progress.insert({
            'user_id': sc.user_id,
            'course_id': sc.course_id,
            'progress': progress
        })
    }
    student_course_num++;
})
db.problem_point.createIndex({
    'module_id': 1
})

function set_problem_point(module_id, user_id, course_id, point) {
    db.problem_point.save({
        'module_id': module_id,
        'user_id': user_id,
        'course_id': course_id,
        'point': point
    });
}
