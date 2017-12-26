function CoursePermission(sys){
    this.user_selection={};
    this.initUI();
    this.sys = sys;
}
CoursePermission.prototype.downloadExcel = function(url){
    var user_state_ids = $("#lst-user-filter-state").get_selection();
    var user_district_ids = $("#lst-user-filter-district").get_selection();
    var user_school_ids = $("#lst-user-filter-school").get_selection();
    var user_cohort_ids = ($("#lst-user-filter-cohort").length ? $("#lst-user-filter-cohort").get_selection().join(",") : []);
    var course_subject = ($("#filters-subject-submenu li.active").attr("data-value") || '');
    var course_author = ($("#filters-author-submenu li.active").attr("data-value") || '');
    var course_grade_level = ($("#filters-grade-submenu li.active").attr("data-value") || '');
    var url = this.sys.url.download_excel;
    url += "&states=" + user_state_ids.join(",");
    url += "&districts=" + user_district_ids.join(",");
    url += "&schools=" + user_school_ids.join(",");
    url += "&cohorts=" + user_cohort_ids.join(",");
    url += "&subject=" + course_subject;
    url += "&author=" + course_author;
    url += "&grade_level=" + course_grade_level;
    window.open(url, "_blank");
}
CoursePermission.prototype.checkTaskProgress = function(taskId){
    var self = this;
    function check(r){
        if(r && r.title == 'all done'){
            new Dialog($('#dialog')).show("Course Save Success ", "Course permissions have been saved.").onClose(function(){
                self.loadUserTable(true);  
            });
        }else if(r && r.title == 'all done with errors'){
            new Dialog($('#dialog')).show("Course Save Failure", "Course permissions have been saved with errors, please check your email for error log.").onClose(function(){
                self.loadUserTable(true);  
            });
        }else{
            setTimeout(function(){
                $.get(self.sys.url.get_async_task, {id: taskId}, function(r){
                    check(r);
                });
            }, 1000);
        }
    }
    check();
}
CoursePermission.prototype.save = function(send_notification){
    var self = this;
    // make filter
    var users = [], courses = [], access = [], enroll = [];
    var global_all_user = $('#course_permission_user .tablesorter-blue .check-all').is(":checked");
    var select_user_manual = $('#course_permission_user .tablesorter-blue .check-manual').is(":checked");
    var select_user_current_page = $('#course_permission_user .tablesorter-blue .check-current-page').is(":checked");
    $('#course_permission_user .tablesorter-blue').find("tbody tr td:nth-child(1) input").each(function(){
        if(select_user_manual){
            if($(this).is(":checked"))users.push(this.value);
        }else if(select_user_current_page){
            users.push(this.value);
        }
    });
    if(!users.length && !global_all_user){
        new Dialog($('#dialog')).show("Warn", "No user selected");
        return;
    }
    var $filter_row = $('#course_permission_course .tablesorter-blue .tablesorter-filter-row');
    var global_course_access = $filter_row.find(".toggle.access").toggleSwitch().val();
    var global_course_enroll = $filter_row.find(".toggle.enroll").toggleSwitch().val();
    var global_all_course = global_course_access != 0 || global_course_enroll != 0;
    $('#course_permission_course .tablesorter-blue tbody tr').each(function(){
        var a = $(this).find("td:nth-child(7) .toggle").toggleSwitch().val();
        var e = $(this).find("td:nth-child(8) .toggle").toggleSwitch().val();
        if(a != 0 || e != 0){
            if(!global_all_course)
                courses.push($(this).find("td:nth-child(5)").text())
            access.push(a);
            enroll.push(e);
        }
    });
    if(!courses.length && !global_all_course){
        new Dialog($('#dialog')).show("Warn", "No course assigned");
        return;
    }
    var $user_table = $('#course_permission_user .tablesorter-blue');
    var $course_table = $('#course_permission_course .tablesorter-blue');
    var course_filter  = $course_table[0].config.pager.data;
    var user_filter  = $user_table[0].config.pager.data;
    var filter = {
        global_all_user: global_all_user,
        global_all_course: global_all_course,
        global_course_access: global_course_access,
        global_course_enroll: global_course_enroll,
        send_notification: send_notification,
        users: users.join(","),
        courses: courses.join(","),
        access: access.join(","),
        enroll: enroll.join(",")
    }
    filter = $.extend(filter, user_filter);
    filter = $.extend(filter, course_filter);
    // submit
    $.post(self.sys.url.update_course_permission, filter, function(r){
        if(r.success){
            self.checkTaskProgress(r.taskId);
        }else{
            new Dialog($('#dialog')).show("Course Permission", "Error occured " + r.error); 
        }
    });
}
CoursePermission.prototype.addTimeStamp = function(url){
    var r = url.replace(/&timestamp=\d*/, "") + "&timestamp=" + new Date().getTime();
    return r;
}
CoursePermission.prototype.loadCourseTable = function(){
    var self = this;
    var url = this.sys.url.get_course_permission_course_rows + "?page={page}&size={size}&{filterList:fcol}&{sortList:col}";
    var data = {
        course_filter_subjects: $("#lst-course-filter-subject").get_selection().join(",") || "",
        course_filter_authors: $("#lst-course-filter-author").get_selection().join(",") || "",
        course_filter_grade_levels: $("#lst-course-filter-grade-level").get_selection().join(",") || "",
        course_filter_states: $("#lst-course-filter-state").get_selection().join(",") || "",
        course_filter_districts: $("#lst-course-filter-district").get_selection().join(",") || ""
    };
    var pagerOptions = {
        container: '',
        output: '{startRow} - {endRow} / {filteredRows} ({totalRows})',
        fixedHeight: false,
        removeRows: false,
        cssGoto: '.gotoPage',
        ajaxUrl: url,
        ajaxProcessing: function(data){
            return data;
        },
        processAjaxOnInit: true,
        page: 0,
        size: 10,
        method: 'POST',
        data: data,
        savePages: false
    };
    var tablesorterOptions = {
        theme: 'blue',
        widthFixed: true,
        widgets: ["zebra", "filter", "output"],
        widgetOptions: {
            filter_external: '',
            filter_columnFilters: true,
            filter_placeholder: {search: 'Search...'},
            filter_saveFilters: false,
            filter_reset: '.reset',
            filter_serversideFiltering: true
        }
    };
    pagerOptions.container = $("#course_permission_course .pager");
    var $table = $('#course_permission_course table.tablesorter-blue');
    if($table[0].config){
        var c = $table[0].config;
        var p = c.pager;
        p = $.extend(p, p.last);
        p.ajaxUrl = url + "&timestamp=" + new Date();
        p.data = data;
        p.reload();
        return;
    }
    $table.tablesorter(tablesorterOptions).tablesorterPager(pagerOptions);
    var loadwin;
    $table.bind("movingPage", function(a){
        loadwin = new LoadingWin();
        loadwin.show();  
    });
    $table.bind('filterStart', function(e, f) {
        this.config.pager.data.course_filter_subject_fuzzy = f[0];
        this.config.pager.data.course_filter_author_fuzzy = f[1];
        this.config.pager.data.course_filter_grade_level_fuzzy = f[2];
        this.config.pager.data.course_filter_course_name_fuzzy = f[3];
    });
    $table.bind("pagerComplete", function (a) {
        if(loadwin)loadwin.hide();
        var this_table=this;
        // $(this).find(".check-current-page").click(function(){
        //     $(this_table).find("tbody tr td:nth-child(6) input").prop("checked", this.checked);
        // });
        // clean contents inside cells
        $(this).find("thead tr td:eq(4)").html("").css("text-align", "left");
        $(this).find("thead tr td:eq(5)").html("").css("text-align", "left");
        // place toggles into cells
         var g_toggle1 = $("<div class='toggle access'/>").appendTo( $(this).find("thead tr td:eq(4)")).toggleSwitch();
         var g_toggle2 = $("<div class='toggle enroll'/>").appendTo( $(this).find("thead tr td:eq(5)")).toggleSwitch();
        g_toggle2.change(function(){
            var v = this.val();
            if(v == 1) g_toggle1.val(1, true)
            $(this_table).find("tbody tr td:nth-child(8) .toggle").toggleSwitch().val(v, false);
        });
        g_toggle1.change(function(){
            var v = this.val();
            if(v == -1) g_toggle2.val(-1, true)
            $(this_table).find("tbody tr td:nth-child(7) .toggle").toggleSwitch().val(v, false);
        });
        $(this).find("tbody tr").each(function(){
            var id = $(this).find("td:nth-child(5)").text();
            var displaynumber = $(this).find("td:nth-child(6)").text();
            $(this).find("td:nth-child(5)").hide();
            $(this).find("td:nth-child(6)").hide();
            $(this).find("td:nth-child(4)").prop("title", displaynumber);
            var toggle1 = $("<div class='toggle'/>").appendTo($(this).find("td").eq(6)).toggleSwitch();
            var toggle2 = $("<div class='toggle'/>").appendTo($(this).find("td").eq(7)).toggleSwitch();
            toggle2.change(function(){
                g_toggle2.val(0, false);
                var v = this.val();
                if(v == 1) toggle1.val(1)
            });
            toggle1.change(function(){
                g_toggle1.val(0, false);
                var v = this.val();
                if(v == -1) toggle2.val(-1)
            });
        });
    });
}
CoursePermission.prototype.loadUserTable = function(use_old_filter){
    var self = this;
    var $table = $('#course_permission_user .tablesorter-blue');
    var hidden = {}
    $("#course_permission_user .filters input[type=hidden]").each(function(){
        hidden[this.name] = this.value;
    });
    if(hidden['csv_users']){
        var data = {
            user_course_filter_subject: ($("#filters-subject-submenu li.active").attr("data-value")) || "",
            user_course_filter_author: ($("#filters-author-submenu li.active").attr("data-value")) || "",
            user_course_filter_grade_level: ($("#filters-grade-submenu li.active").attr("data-value")) || "",
            user_filter_csv_users: hidden['csv_users']
        };
    }else{
        var data = {
            user_course_filter_subject: ($("#filters-subject-submenu li.active").attr("data-value")) || "",
            user_course_filter_author: ($("#filters-author-submenu li.active").attr("data-value"))  || "",
            user_course_filter_grade_level: ($("#filters-grade-submenu li.active").attr("data-value"))  || "",
            user_filter_states: hidden["state_id"] || $("#lst-user-filter-state").get_selection().join(",")  || "",
            user_filter_districts: hidden["district_id"] || $("#lst-user-filter-district").get_selection().join(",")  || "",
            user_filter_schools: $("#lst-user-filter-school").get_selection().join(",") || "",
            user_filter_cohorts: ($("#lst-user-filter-cohort").length? $("#lst-user-filter-cohort").get_selection().join(",") : null)  || ""
        };
    }
    var url = this.sys.url.get_course_permission_user_rows + "?page={page}&size={size}&{sortList:col}";
    /** reload with new filters or not */
    if($table[0].config){
        var c = $table[0].config;
        var p = c.pager;
        p = $.extend(p, p.last);
        p.data = $.extend(p.data, data);
        if(use_old_filter){
            p.ajaxUrl = this.addTimeStamp(p.ajaxUrl.replace(/page=\d+/, 'page={page}'));
        }else{
            p.ajaxUrl = this.addTimeStamp(url);
        }
        // $table.find("td:nth-child(1) input").each(function(){
        //     self.user_selection[this.value] = (this.checked);
        // });
        p.reload();
        return;
    }
    /** init */
    var courses;
    var all_user_on = false;
    var pagerOptions = {
        container: $("#course_permission_user .pager"),
        output: '{startRow} - {endRow} / {filteredRows} ({totalRows})',
        fixedHeight: false,
        removeRows: false,
        cssGoto: '.gotoPage',
        ajaxUrl: url,
        ajaxProcessing: function(data){
            all_user_on = $("input[name=user-select].check-all").is(":checked");
            if(data && data.length)courses = data[2];
            return data;
        },
        processAjaxOnInit: true,
        page: 0,
        size: 10,
        method: 'POST',
        data: data
    };
    var tablesorterOptions = {
        theme: 'blue',
        widthFixed: true,
        widgets: ["zebra", "filter", "output"],
        widgetOptions: {
            filter_external: '',
            filter_columnFilters: true,
            filter_placeholder: {search: 'Search...'},
            filter_saveFilters: false,
            filter_reset: '.reset',
            filter_serversideFiltering: true,
            output_saveFileName: 'data.csv'
        }
    };
    $table.tablesorter(tablesorterOptions).tablesorterPager(pagerOptions);
    $table.bind('filterStart', function(e, f) {
        this.config.pager.data.user_filter_first_name_fuzzy=f[1];
        this.config.pager.data.user_filter_last_name_fuzzy=f[2];
        this.config.pager.data.user_filter_email_fuzzy=f[3];
    });
    var loadwin;
    $table.bind("movingPage", function(a){
        loadwin = new LoadingWin();
        loadwin.show();  
    });
    $table.bind("pagerComplete", function (a) {
        $('#course_permission_user table.tablesorter-blue thead').off("click");
        if(loadwin)loadwin.hide();
        // $(this).trigger('refreshColumnSelector', [[0, 1, 2]]);
        // $(this).find("th:nth-child(1)").width(160)
        var this_table=this;
        // var $check_all = $(this).find(".check-current-page");
        // $check_all.click(function(){
        //     $(this_table).find("tbody tr td:nth-child(1) input").prop("checked", this.checked);
        //     $(this_table).find("tbody tr td:nth-child(1) input").trigger("change");
        // });
        var user_selection = self.user_selection;
        $(this).find("td:nth-child(1):gt(0)").each(function(i){
            var v = $(this).text();
            $(this).html("");
            var $check = $("<input type='checkbox'>").appendTo(this).val(v);
            if(user_selection[v]){
                $check.prop('checked', true);
            }
            $check.change(function(){
                self.user_selection[this.value] = (this.checked);
                //console.log(self.user_selection)
                // var all_checked = $(this_table).find("tbody tr td:nth-child(1) input:checked").length == $(this_table).find("tbody tr td:nth-child(1) input").length;
                // //console.log(all_checked)
                // $check_all.attr("checked", all_checked);
            })
            $check.click(function(){
            });
            $check.trigger("change");
        });
        // self.user_selection = {};
        /** hide headers only for filter  */
        $(this).find("th:nth-child(5)").hide();
        $(this).find("td:nth-child(5)").hide();
        $(this).find("th:nth-child(6)").hide();
        $(this).find("td:nth-child(6)").hide();
        $(this).find("th:nth-child(7)").hide();
        $(this).find("td:nth-child(7)").hide();
        var $tr0 = $(this).find("thead tr").eq(0);
        var $tr1 = $(this).find("thead tr").eq(1);
        /** headers of filtered courses */
        $tr0.find("th:gt(6)").remove();
        $tr1.find("td:gt(6)").remove();
        $tr1.find("td:eq(0)").html("");
        $.each(courses, function(i, c){
            $("<th title=" + c.display_coursenumber + ">" + c.display_name + "</th>").appendTo($tr0).hover(function(){
            });
            $("<td></td>").appendTo($tr1);
        });
        /** float user window */
        var $thead = $(this).find("thead");
        $("#float-users-win").html("");
        $(this).find("tbody tr td:nth-child(4)").each(function(){ // each email.
            var $tr = $(this).parent();
            // courses assigned
            var course_assign = "";
            $tr.find("td:gt(6)").each(function(i){
                var assign = $(this).html();
                if(assign == "P" || assign == "E"){
                    var c = $thead.find("tr th:nth-child(" + (i+5) + ")").html();
                    course_assign += "<div>" + c + " <b>" + assign + "</b></div>"
                }
            });
            var $item = $("<div class='email'><input type='checkbox'> <label>" + $(this).html() + "</label></div>").appendTo($("#float-users-win"));
            $item.find("input").prop("checked", $tr.find("td:eq(0) input").prop("checked"));
            var $detail = $("<div class='courses'>" + course_assign + "</div>").insertAfter($item);
            $detail.hide();
            /** change checked eath other */
            $item.find("input").on("change", function(){
                $tr.find("td:eq(0) input").prop("checked", $(this).prop("checked"))
            });
            $tr.find("td:eq(0) input").on("change", function(){
                $item.find("input").prop("checked", $(this).prop("checked"))
            });
            $item.find("label").click(function(){
                if($detail.is(":visible"))
                    $detail.hide();
                else
                    $detail.show();
            });
        });
        // begin ------- end checks control
        var $checks = $(this).find("tbody tr td:nth-child(1) input");
        $("input[name=user-select]").change(function(e){
            var v = $(this).val(); 
            if(v == "manual"){
                $checks.prop("checked", false);
            }else if(v == "current-page"){
                $checks.prop("checked", true);
            }else if(v == "all"){
                $checks.prop("checked", true);
            }
        });
        if(all_user_on){
            $checks.prop("checked", true);
        }else{
            $("input[name=user-select].check-manual").prop("checked", true);
        }
        // end ------- checks control
        $checks.change(function(){
            $("input[name=user-select].check-manual").prop("checked", true);
        });
    });
}
CoursePermission.prototype.dropDistrictMu = function(select, state_ids){
    $(select).find("option").remove();
    $(select).reload();
    if(!state_ids.length)
        return;
    $.get('/pepper-utilities/drop/districts',{access_level: 'System', state: state_ids.join(",")}, function(r){
        $.each(r, function(i, d){
            $(select).append("<option value='" + d.id + "'>" + d.name + "</option>");
        });
        $(select).reload();
    });
}
CoursePermission.prototype.dropSchoolMu = function(select, district_ids){
    $(select).find("option").remove();
    $(select).reload();
    if(!district_ids.length)
        return;
    $.get('/pepper-utilities/drop/schools',{access_level: 'System', district: district_ids.join(",")}, function(r){
        $.each(r, function(i, d){
            $(select).append("<option value='" + d.id + "'>" + d.name + "</option>");
        });
        $(select).reload();
    });
}
CoursePermission.prototype.dropCohortMu = function(select, district_ids){
    $(select).find("option").remove();
    $(select).reload();
    if(!district_ids.length)
        return;
    $.get('/pepper-utilities/drop/cohorts',{access_level: 'System', district: district_ids.join(",")}, function(r){
        $.each(r, function(i, d){
            $(select).append("<option value='" + d.id + "'>" + d.code + "</option>");
        });
        $(select).reload();
    });
}
CoursePermission.prototype.loadCsv=function(){
    var self = this;
    var $file =  $("#btnCoursePermCsvLoad").next("input");
    $file.click();
    $file.change(function(){
        if(this.value){
            var fd = new FormData();
            fd.append('attachment', this.files[0]);
            $(this).val("");
            $.ajax({
                url: self.sys.url.course_permission_load_csv,
                data: fd,
                processData: false,
                contentType: false,
                type: 'post',
                beforeSend: function (x) {
                    if (x && x.overrideMimeType) {
                        x.overrideMimeType("multipart/form-data");
                    }
                },
                enctype: 'multipart/form-data',
                mimeType: 'multipart/form-data',
                error: function(xhr, status){},
                success: function(data){
                    if(data.success){
                        self.checkTaskProgress(data.taskId);
                    }else{
                        new Dialog($('#dialog')).show("Course Permission", "Error occured " + r.error); 
                    }
                }
            });            
        }
    });
}
CoursePermission.prototype.initUI = function(){
    var self = this;
    /** filter subject/author/grade menu */
    $(".filters-submenu").each(function(){
        $(this).find("li").each(function(i){
            var colors=["#2196F3", "#E93578", "#C238EB", "#629C44", "#006E8C"];
            $(this).css("background", colors[i % colors.length])
            $(this).click(function(){
                var on = $(this).hasClass("active");
                $(this).parent().find("li").removeClass("active");
                if(!on)
                    $(this).addClass("active");
                $("#filters-menu-selection").html("");
                $(".filters-submenu li.active").each(function(){
                    var self = this;
                    var a = $("<span>" + $(this).html() + "<b class='close'>x</b></span>").appendTo($("#filters-menu-selection"));
                    a.find("b").click(function(){
                        $(this).closest("ul").find("li").removeClass("active");
                        $(self).removeClass("active");
                        a.remove();
                    });
                });
            });
        });
    });
    $(".filters-menu li").click(function(){
        $(this).parent().find("li").removeClass("active");
        $(this).addClass("active");
        $(".filters-submenu").hide();
        $("#" + this.id + "-submenu").show();
    });
    $(".filters-menu li").eq(0).click(); /** show subject at 1st */
    /** filter dropdowns */
    $(".mu").multi_sele_dropdown().change(function(e){
        if(this.id == "lst-user-filter-state"){
            var sele = ("#lst-user-filter-district");
            self.dropDistrictMu(sele, $(this).get_selection());
        }else if(this.id == "lst-user-filter-district"){
            var sele = ("#lst-user-filter-school");
            self.dropSchoolMu(sele, $(this).get_selection());
            
            var sele = ("#lst-user-filter-cohort");
            self.dropCohortMu(sele, $(this).get_selection());
        }else if(this.id == "lst-course-filter-state"){
            var sele = ("#lst-course-filter-district");
            self.dropDistrictMu(sele, $(this).get_selection());
        }
    });
    $(document).click(function(e){
        if(!$(e.target).parent().hasClass("filters-menu") &&
           !$(e.target).parent().hasClass("filters-submenu")) {
            $(".filters-menu li").removeClass("active");
            $(".filters-submenu").hide();
        }
    })
    /** btns load table */
    $("#btnUserLoad").click(function(){
        $("input[name=csv_users]").val("");
        self.loadUserTable();
    });
    $("#btnCourseLoad").click(function(){
        self.loadCourseTable();
    });
    /** btn save */
    $("#btnSave").click(function(){
        self.save(false);
    });
    $("#btnSaveSend").click(function(){
        self.save(true);
    });
    $("#btnCoursePermCsvLoad").click(function(){
        self.loadCsv();      
    });
    $("#btnCoursePermDownloadExcel").click(function(){
        self.downloadExcel();
        return false;
    });
    $(".course-perm-sub-title").click(function(){
        var $div = $(this).next("div");
        if($div.is(":visible")){
            $div.slideUp();
            $(this).removeClass("shown");
        }else{
            $div.slideDown();
            $(this).addClass("shown");
        }
    });
    $("#btnClearUserFilter, #btnClearCourseFilter").click(function(){
        $("#course_permission_user, #course_permission_course").find("div.filters").find("select").each(function(){
            $(this).clear_all();
            $(".filters-submenu li").removeClass("active");
        });
    });
    /** set size of floating user win */
    var isInView = false;
    setInterval(function(){
        if(isInView)
            return $("#float-users-win").hide();
        if($("#float-users-win").find("input:checked").length < 1)
            return $("#float-users-win").hide();
        var offset = $("#course_permission_user").offset();
        var width = offset.left - $(window).scrollLeft() - 20;
        if($("#float-users-win").html()){
            if(width < 0)
                $("#float-users-win").hide();
            else
                $("#float-users-win").show();
            $("#float-users-win").width(width);
        }else{
            $("#float-users-win").hide();
        }
    }, 100);
    $('#course_permission_user table').on('inview', function(event, v) {
        isInView = v;
    });
}
