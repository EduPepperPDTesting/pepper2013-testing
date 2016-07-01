#!/bin/bash
echo -e "tahoe" | sudo -S netstat -tlnp
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
mongo3_path="/home/tahoe/mongo321/mongodb-linux-x86_64-ubuntu1204-3.2.1/bin"
cd "$DIR"
echo '-------------------------------------------'
echo 'User information conversion'
echo '-------------------------------------------'
sudo rm -f /tmp/user_info.csv;
mysql -upepper -plebbeb <<EOF
use pepper;
select auth_user.id,auth_userprofile.user_id,auth_user.email,TRIM(auth_user.username),TRIM(auth_user.first_name),TRIM(auth_user.last_name),TRIM(state.name) as state,TRIM(district.name) as district,TRIM(school.name) as school,state.id as state_id,district.code as district_id,school.id as school_id,date_format(auth_userprofile.activate_date,'%Y-%m-%d') as activate_date,TRIM(auth_userprofile.subscription_status),subject_area.name as major_subject_area from auth_user left join auth_userprofile on (auth_userprofile.user_id=auth_user.id) left join district on(district_id=district.id) left join state on(state_id=state.id) left join school on(school_id=school.id) left join subject_area on(major_subject_area_id=subject_area.id) into outfile '/tmp/user_info.csv' fields terminated by ',' optionally enclosed by '"' escaped by '' lines terminated by '\n';
EOF
$mongo3_path/mongo --port=27018 <<EOF
use reporting
db.user_info.drop()
EOF
# $mongo3_path/mongoimport -d "reporting" -c "user_info" --port 27018 -f "id,user_id,username,state,district,school,major_subject_area" --type=csv --file=/tmp/test123.csv
$mongo3_path/mongoimport -d "reporting" -c "user_info" --port 27018 -f "id,user_id,email,username,first_name,last_name,state,district,school,state_id,district_id,school_id,activate_date,subscription_status,major_subject_area" --type=csv --file=/tmp/user_info.csv
sudo rm -f /tmp/user_info.csv;
echo '-------------------------------------------'
echo 'user conversion is complete!'
echo '-------------------------------------------'
#exit 0;
echo '###########################################'

echo '-------------------------------------------'
echo 'Course information conversion'
echo '-------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

mongoexport -d xmodule -c modulestore -o /tmp/modulestore.json
$mongo3_path/mongo --port=27018 <<EOF
use reporting
db.modulestore.drop()
EOF
$mongo3_path/mongoimport -d reporting -c modulestore /tmp/modulestore.json --port 27018
sudo rm -f /tmp/modulestore.json;
$mongo3_path/mongo --port=27018 <<EOF
use reporting
db.modulestore.find({'_id.category':'course'}).forEach(function(x){
  x.course_id = [x._id.org, x._id.course, x._id.name].join('/');
  db.modulestore.save(x);
})
db.modulestore.remove({'_id.revision':'draft'})
EOF
echo '-------------------------------------------'
echo 'Course conversion is complete!'
echo '-------------------------------------------'
#exit 0;
echo '###########################################'

echo '-------------------------------------------'
echo 'Time report information conversion'
echo '-------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

sudo rm -f /tmp/pd_time.csv;
mysql -upepper -plebbeb <<EOF
use pepper;
select student_id as user_id,sum(student_credit)*3600 as credit from pepreg_student group by user_id into outfile '/tmp/pd_time.csv' fields terminated by ',' optionally enclosed by '"' escaped by '' lines terminated by '\n';
EOF

mongoexport -d assist -c page_time -o /tmp/page_time.json
mongoexport -d assist -c discussion_time -o /tmp/discussion_time.json
mongoexport -d assist -c portfolio_time -o /tmp/portfolio_time.json
mongoexport -d assist -c external_time -o /tmp/external_time.json
mongoexport -d assist -c adjustment_time -o /tmp/adjustment_time.json
$mongo3_path/mongo --port=27018 <<EOF
use reporting
db.page_time.drop()
db.discussion_time.drop()
db.portfolio_time.drop()
db.external_time.drop()
db.adjustment_time.drop()
db.t_external_time.drop()
db.course_time.drop()
db.pd_time.drop()
EOF
$mongo3_path/mongoimport -d reporting -c page_time /tmp/page_time.json --port 27018
$mongo3_path/mongoimport -d reporting -c discussion_time /tmp/discussion_time.json --port 27018
$mongo3_path/mongoimport -d reporting -c portfolio_time /tmp/portfolio_time.json --port 27018
$mongo3_path/mongoimport -d reporting -c t_external_time /tmp/external_time.json --port 27018
$mongo3_path/mongoimport -d reporting -c adjustment_time /tmp/adjustment_time.json --port 27018
sudo rm -f /tmp/page_time.json;
sudo rm -f /tmp/discussion_time.json;
sudo rm -f /tmp/portfolio_time.json;
sudo rm -f /tmp/external_time.json;
sudo rm -f /tmp/adjustment_time.json;

$mongo3_path/mongoimport -d "reporting" -c "pd_time" --port 27018 -f "user_id,credit" --type=csv --file=/tmp/pd_time.csv
sudo rm -f /tmp/pd_time.csv;

sudo $mongo3_path/mongo --port=27018 <<EOF
use reporting

db.adjustment_time.find().forEach(function(x){
  x.user_id =  parseInt(x.user_id);
  db.adjustment_time.save(x);
});

db.page_time.find().forEach(function(x){
  x.user_id =  parseInt(x.user_id);
  db.page_time.save(x);
});
db.page_time.aggregate({
    \$group: {
        _id: {'course_id':'\$course_id','user_id':'\$user_id'},
        user_id: {\$push:'\$user_id'} ,
        course_id:{\$push:'\$course_id'} ,
        time: {
            \$sum: '\$time'
        }
    }
  },{
    \$project: {
        _id: 1,
        user_id: {\$arrayElemAt: ['\$user_id', 0]},
        course_id: {\$arrayElemAt: ['\$course_id', 0]},
        time: 1
    }
},{\$out:'course_time'})

db.adjustment_time.find({'type':'courseware'}).forEach(function(ad){
  var cur_item = db.course_time.findOne({'course_id':ad.course_id,'user_id':ad.user_id})
  if(cur_item!=null){
    cur_item.time+=ad.time;
    db.course_time.save(cur_item);
  }
  else{
    db.course_time.save({'_id':{'course_id':ad.course_id,'user_id':ad.user_id},'user_id':ad.user_id,'course_id':ad.course_id,'time':ad.time})
  }

})
db.discussion_time.find().forEach(function(x){
  x.user_id =  parseInt(x.user_id);
  db.discussion_time.save(x);
});
db.adjustment_time.find({'type':'discussion'}).forEach(function(ad){
  var cur_item = db.discussion_time.findOne({'course_id':ad.course_id,'user_id':ad.user_id})
  if(cur_item!=null){
    cur_item.time+=ad.time;
    db.discussion_time.save(cur_item);
  }
  else{
    db.discussion_time.save({'user_id':ad.user_id,'course_id':ad.course_id,'time':ad.time})
  }

})
db.portfolio_time.find().forEach(function(x){
  x.user_id =  parseInt(x.user_id);
  db.portfolio_time.save(x);
});
db.adjustment_time.find({'type':'portfolio'}).forEach(function(ad){
  var cur_item = db.portfolio_time.findOne({'user_id':ad.user_id})
  if(cur_item!=null){
    cur_item.time+=ad.time;
    db.portfolio_time.save(cur_item);
  }
  else{
    db.portfolio_time.save({'user_id':ad.user_id,'time':ad.time})
  }

})
db.t_external_time.find().forEach(function(x){
  x.user_id =  parseInt(x.user_id);
  var course = x.course_id.split('/')[1];
  var time = db.modulestore.findOne({'_id.category':'course','_id.course':course}).metadata.external_course_time;
  if(time==null){time=1800;}
  x.r_time = parseInt(x.weight) * parseInt(time);
  db.t_external_time.save(x);
});

db.t_external_time.aggregate({
    \$group: {
        _id: {'course_id':'\$course_id','user_id':'\$user_id'},
        user_id: {\$push:'\$user_id'} ,
        course_id:{\$push:'\$course_id'} ,
        r_time: {
            \$sum: '\$r_time'
        }
    }
  },{
    \$project: {
        _id: 1,
        user_id: {\$arrayElemAt: ['\$user_id', 0]},
        course_id: {\$arrayElemAt: ['\$course_id', 0]},
        r_time: 1
    }
},{\$out:'external_time'})

db.adjustment_time.find({'type':'external'}).forEach(function(ad){
  var cur_item = db.external_time.findOne({'course_id':ad.course_id,'user_id':ad.user_id})
  if(cur_item!=null){
    cur_item.r_time+=ad.time;
    db.external_time.save(cur_item);
  }
  else{
    db.external_time.save({'_id':{'course_id':ad.course_id,'user_id':ad.user_id},'user_id':ad.user_id,'course_id':ad.course_id,'r_time':ad.time})
  }
})
EOF
echo '-------------------------------------------'
echo 'Time report conversion is complete!'
echo '-------------------------------------------'

echo '###########################################'

echo '-------------------------------------------'
echo 'Course enrollment conversion'
echo '-------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

mysql -upepper -plebbeb <<EOF
use pepper;
select user_id,course_id,created,is_active from student_courseenrollment into outfile '/tmp/student_courseenrollment.csv' fields terminated by ',' optionally enclosed by '"' escaped by '' lines terminated by '\n';
EOF

$mongo3_path/mongo --port=27018 <<EOF
use reporting
db.student_courseenrollment.drop()
EOF
# $mongo3_path/mongoimport -d "reporting" -c "student_courseenrollment" --port 27018 -f "user_id,course_id,created" --type=csv --file=/tmp/student_courseenrollment.csv
$mongo3_path/mongoimport -d "reporting" -c "student_courseenrollment" --port 27018 -f "user_id,course_id,created,is_active" --type=csv --file=/tmp/student_courseenrollment.csv
sudo rm -f /tmp/student_courseenrollment.csv;
$mongo3_path/mongo --port=27018 <<EOF
use reporting
var user_info = [];
db.student_courseenrollment.find().forEach(
  function(x){
    var key = x.user_id;
    if(user_info[key] == null){
      user_info[key] = db.user_info.findOne({'user_id':x.user_id})
    }
    if(user_info[key] != null){
      x.state_id = user_info[key].state_id;
      x.district_id = user_info[key].district_id;
      x.school_id = user_info[key].school_id;
      db.student_courseenrollment.save(x);
    }
    else{
      db.student_courseenrollment.remove(x);
    }
})
EOF
echo '-------------------------------------------'
echo 'Course enrollment conversion is complete!'
echo '-------------------------------------------'
#exit 0;

echo '###########################################'

echo '-------------------------------------------'
echo 'Student module conversion'
echo '-------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

sudo rm -f /tmp/courseware_studentmodule.csv;
mysql -upepper -plebbeb <<EOF
use pepper;
select module_type,module_id,student_id,replace(state,'"',"#@#") as state,grade,created,modified,max_grade,done,course_id from courseware_studentmodule where module_type='problem' or module_type='combinedopenended' or module_type='course' into outfile '/tmp/courseware_studentmodule.csv' fields terminated by ',' optionally enclosed by '"' escaped by '' lines terminated by '\n';
EOF
$mongo3_path/mongo --port=27018 <<EOF
use reporting
db.courseware_studentmodule.drop()
EOF
# $mongo3_path/mongoimport -d "reporting" -c "courseware_studentmodule" --port 27018 -f "module_type,module_id,student_id,state,grade,created,modified,max_grade,done,course_id" --type=csv --file=/tmp/courseware_studentmodule.csv
$mongo3_path/mongoimport -d "reporting" -c "courseware_studentmodule" --port 27018 -f "module_type,module_id,student_id,state,grade,created,modified,max_grade,done,course_id" --type=csv --file=/tmp/courseware_studentmodule.csv
sudo rm -f /tmp/courseware_studentmodule.csv;

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

$mongo3_path/mongo --port=27018 <<EOF
use reporting
db.courseware_studentmodule.find().forEach(
    function(x){
        x.state = JSON.parse(x.state.replace(new RegExp("#@#",'gm'),'"'));
        if(x.module_type == 'course'){
          x.c_course_id = x.course_id;
          x.c_student_id = x.student_id;
        }
        db.courseware_studentmodule.save(x);
    })
EOF
echo '-------------------------------------------'
echo 'Student module conversion is complete!'
echo '-------------------------------------------'

#exit 0;

echo '###########################################'

echo '-----------------------------------------------'
echo 'Create Indexes'
echo '-----------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

$mongo3_path/mongo --port=27018 <<EOF
use reporting

var courseArr = [];
db.modulestore.find({'_id.category':'course'}).forEach(function(x){
  courseArr.push(x.course_id);
})
db.student_courseenrollment.remove({'course_id':{'\$nin':courseArr}});
db.courseware_studentmodule.remove({'course_id':{'\$nin':courseArr}});
db.student_courseenrollment.createIndex({
    'user_id': 1
})
db.student_courseenrollment.createIndex({
    'course_id': 1
})
db.user_info.createIndex({
    'user_id': 1
})
db.modulestore.createIndex({
    'course_id': 1
})
db.modulestore.createIndex({
    'q_course_id': 1
})
db.course_time.createIndex({
    'user_id': 1
})
db.discussion_time.createIndex({
    'user_id': 1
})
db.portfolio_time.createIndex({
    'user_id': 1
})
db.external_time.createIndex({
    'user_id': 1
})
db.adjustment_time.createIndex({
    'user_id': 1
})
db.user_course_progress.createIndex({
    'user_id': 1
})
//db.courseware_studentmodule.dropIndexes();
db.courseware_studentmodule.createIndex({
    'c_student_id': 1
})
db.courseware_studentmodule.createIndex({
    'c_course_id': 1
})
db.courseware_studentmodule.createIndex({
    'module_id': 1
})
db.courseware_studentmodule.createIndex({
    'student_id': 1, 'module_id': 1, course_id:1
})

EOF
echo '------------------------------------------------'
echo 'Create Indexes complete!'
echo '------------------------------------------------'


echo '###########################################'

echo '-----------------------------------------------'
echo 'User Course Progress'
echo '-----------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

$mongo3_path/mongo --port=27018 <<EOF

load("$DIR/progress.js");

EOF
echo '------------------------------------------------'
echo 'User Course Progress is complete!'
echo '------------------------------------------------'

#exit 0;

echo '###########################################'

echo '-----------------------------------------------'
echo 'Clear cache collections'
echo '-----------------------------------------------'

$mongo3_path/mongo --port=27018 <<EOF
use reporting

db.getCollectionNames().forEach(function(x){
  if(x.indexOf('tmp_collection_') >= 0){
    db.getCollection(x).drop();
  }
})

EOF
echo '-----------------------------------------------'
echo 'Clear cache collections complete!'
echo '-----------------------------------------------'

#exit 0;

echo '###########################################'

echo '-----------------------------------------------'
echo 'Create superuser views'
echo '-----------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

$mongo3_path/mongo --port=27018 <<EOF

load("$DIR/create_superuser_views/user.js");
load("$DIR/create_superuser_views/course.js");
load("$DIR/create_superuser_views/user-course.js");
load("$DIR/create_superuser_views/course-assignments.js");
load("$DIR/create_superuser_views/aggregate-timer.js");
load("$DIR/create_superuser_views/aggregate-grades.js");

EOF
echo '-----------------------------------------------'
echo 'Create superuser views complete!'
echo '-----------------------------------------------'

sync
echo 3 | sudo tee /proc/sys/vm/drop_caches

exit 0;


