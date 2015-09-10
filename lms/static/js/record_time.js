function RecordTime() {};

RecordTime.userID = '';
RecordTime.firstRun = true;
RecordTime.flag = null;
RecordTime.coursePosition = 1;

RecordTime.sessionInit = function() {
    RecordTime.userID = sessionStorage['user_id'];
    var vertical_id = RecordTime.userID + '_vertical_id';
    var time = RecordTime.userID + '_time';
    var course_time = RecordTime.userID + '_course_time';
    var course_id = RecordTime.userID + '_course_id';
    sessionStorage[vertical_id] = sessionStorage[vertical_id] || '';
    sessionStorage[time] = sessionStorage[time] || '';
    sessionStorage[course_time] = sessionStorage[course_time] || 0;
    sessionStorage[course_id] = sessionStorage[course_id] || '';
};

RecordTime.getSessionVerticalId = function() {
    return sessionStorage[RecordTime.userID + '_vertical_id'];
};

RecordTime.setSessionVerticalId = function(val) {
    sessionStorage[RecordTime.userID + '_vertical_id'] = val;
};

RecordTime.getSessionTime = function() {
    return sessionStorage[RecordTime.userID + '_time'];
};

RecordTime.setSessionTime = function(val) {
    sessionStorage[RecordTime.userID + '_time'] = val;
};

RecordTime.getSessionCourseID = function() {
    return sessionStorage[RecordTime.userID + '_course_id'];
};

RecordTime.setSessionCourseID = function(val) {
    sessionStorage[RecordTime.userID + '_course_id'] = val;
};

RecordTime.getSessionCourseTime = function(type) {
    return sessionStorage[RecordTime.userID + '_' + type];
};

RecordTime.setSessionCourseTime = function(type, val) {
    sessionStorage[RecordTime.userID + '_' + type] = val;
};

RecordTime.getSessionCourseType = function() {
    return sessionStorage[RecordTime.userID + '_type'];
};

RecordTime.setSessionCourseType = function(val) {
    if (val != '')
        sessionStorage[RecordTime.userID + '_type'] = val;
};

RecordTime.ajaxRecordTime = function(data, callback) {
    $.post("/record_time/", data, function(r) {
        callback();
    });
};

RecordTime.getCourseFullPath = function(path, position) {
    var pathArr = path.split('/courses/')[1].split('/');
    pathArr[6] = position;
    return pathArr.join('/');
};

//---------------------------------------------------------------------------------


function CourseTimer($container) {
    this.time = 0;
    this.hour = 0;
    this.minute = 0;
    this.second = 0;
    this.flag = null;
    this.element = null;
    this.btn = null;
    this.isrun = false;
    this.exeType = ['courseware', 'discussion', 'portfolio'];
    this.type = this.getType();
    this.create();
};

CourseTimer.prototype.create = function() {

    switch (this.type) {
        case 'courseware':
            this.courseInit();
            break;
        case 'discussion':
            this.discussionInit();
            break;
        case 'portfolio':
            this.portfolioInit();
            break;
        default:
            this.save();
    }
    //console.log("Type:" + this.type);
};

CourseTimer.prototype.init = function() {
    this.time = 0;
    this.hour = 0;
    this.minute = 0;
    this.second = 0;
    this.hide();
    this.stop();
    this.save();
    this.draw();
};

CourseTimer.prototype.start = function() {
    if (!this.isrun) {
        this.isrun = true;
        this.load();
    }
    this.show();
    RecordTime.setSessionCourseType(this.type);
};

CourseTimer.prototype.run = function() {
    var self = this;
    this.draw();
    this.time += 1;
    RecordTime.setSessionCourseTime(this.type, this.time);
    RecordTime.flag = setTimeout(function() {
        self.run();
    }, 1000);
    //console.log(RecordTime.flag);
};

CourseTimer.prototype.draw = function() {
    if (this.element != null) {
        this.hour = this.padding(Math.floor(this.time / 60 / 60));
        this.minute = this.padding(Math.floor(this.time / 60 % 60));
        this.second = this.padding(Math.floor(this.time % 60));
        this.hour_ele.html(this.hour);
        this.minute_ele.html(this.minute);
        this.second_ele.html(this.second);
        this.display_ele.html(this.format(this.time))
    }
};

CourseTimer.prototype.stop = function() {
    clearTimeout(RecordTime.flag);
    //this.isrun = false;
};

CourseTimer.prototype.show = function() {
    if (this.element != null) this.element.show();
};

CourseTimer.prototype.hide = function() {
    if (this.element != null) this.element.hide();
};

CourseTimer.prototype.load = function() {
    var self = this;
    $.post('/record_time/course_time_load', {
        'user_id': RecordTime.userID,
        'course_id': RecordTime.getSessionCourseID(),
        'type': this.type
    }, function(data) {

        if (data != null) {
            self.time = parseInt(data.time);
            RecordTime.setSessionCourseTime(this.type, self.time);
        } else {
            self.time = 0;
        }
        console.log("user_id:" + RecordTime.userID + "course_id:" + RecordTime.getSessionCourseID())
        if (RecordTime.getSessionCourseType() != 'courseware') {
            self.run();
        } else {
            self.draw();
        }
    });
};

CourseTimer.prototype.save = function() {
    var self = this;
    stime = parseInt(RecordTime.getSessionCourseTime(RecordTime.getSessionCourseType()));
    self.time = self.time != 0 ? self.time : stime;
    if (self.time > 0 && RecordTime.getSessionCourseID() != '' && RecordTime.getSessionCourseType() != '') {
        $.post('/record_time/course_time_save', {
            'user_id': RecordTime.userID,
            'course_id': RecordTime.getSessionCourseID(),
            'type': RecordTime.getSessionCourseType(),
            'time': self.time
        }, function(r) {
            RecordTime.setSessionCourseTime(RecordTime.getSessionCourseType(), 0);
        });
    }
};

CourseTimer.prototype.format = function(t) {
    var hour = Math.floor(t / 60 / 60);
    var minute = Math.floor(t / 60 % 60);
    var second = Math.floor(t % 60);
    var hour_unit = hour < 2 ? ' Hour, ' : ' Hours, ';
    var minute_unit = minute < 2 ? ' Minute ' : ' Minutes ';
    var hour_full = hour > 0 ? hour + hour_unit : '';
    return hour_full + minute + minute_unit;
};

CourseTimer.prototype.padding = function(v) {
    if (v.toString().length <= 1) return '0' + v;
    return v;
};

CourseTimer.prototype.getType = function() {
    var temp_url = document.URL.split('/courses/');
    var type = '';
    if (temp_url.length > 1) {
        type = temp_url[1].split('/')[3];
        if (this.exeType.indexOf(type) >= 0) {
            return type;
        } else {
            return '';
        }
    } else {
        console.log("Without this category.")
    }
    return type;
};

CourseTimer.prototype.createClock = function($container) {

    $container.empty();
    this.element = $("<div class='course_timer_div' style='float:right;'>Course Time: <span class='course_timer_display'></span> / <span class='course_timer_hour'>00</span>:<span class='course_timer_minute'>00</span>:<span class='course_timer_second'>00</span></div>");
    this.btn = $("<input type='button' onclick='location.href=\"/study_time\"' value='Time' style='margin-left:5px;float:right;padding:0px 5px 0px 5px;font-size:11px;height:25px;'/>");
    $container.prepend(this.element);
    this.element.append(this.btn);
    this.hour_ele = this.element.find('.course_timer_hour');
    this.minute_ele = this.element.find('.course_timer_minute');
    this.second_ele = this.element.find('.course_timer_second');
    this.display_ele = this.element.find('.course_timer_display');

}

CourseTimer.prototype.courseInit = function() {
    this.createClock($('.course_timer'));
    this.init();
};

CourseTimer.prototype.discussionInit = function() {
    this.init();
    this.start();
};

CourseTimer.prototype.portfolioInit = function() {
    var portfolio_info = document.URL.split('/portfolio/')[1].split('/');
    if (portfolio_info.length > 1) {
        if (RecordTime.userID != portfolio_info[1]) {
            this.init();
            this.start();

        }
    }
};