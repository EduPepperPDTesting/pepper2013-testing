if (!CMS.Views['Settings']) CMS.Views.Settings = {};

CMS.Views.Settings.Details = CMS.Views.ValidatingView.extend({
    // Model class is CMS.Models.Settings.CourseDetails
    events : {
        "input input" : "updateModel",
        "input textarea" : "updateModel",
        // Leaving change in as fallback for older browsers
        "change input" : "updateModel",
        "change textarea" : "updateModel",
        'click .remove-course-introduction-video' : "removeVideo",
        'focus #course-overview' : "codeMirrorize",
        'mouseover #timezone' : "updateTime",
        // would love to move to a general superclass, but event hashes don't inherit in backbone :-(
        'focus :input' : "inputFocus",
        'blur :input' : "inputUnfocus",
        "change .input_overview" : "updateModel_overview",
        'click .action-upload-image': "uploadImage",
        'click .course-author-btn': "addCourseAuthor",
        'click :radio': "overview_switch"
    },
    overview_mode:'general',
    load_overview_init:false,
    initialize : function() {
        this.fileAnchorTemplate = _.template('<a href="<%= fullpath %>"> <i class="icon-file"></i><%= filename %></a>');
        // fill in fields
        this.$el.find("#course-name").val(this.model.get('location').get('name'));
        this.$el.find("#course-organization").val(this.model.get('location').get('org'));
        this.$el.find("#course-number").val(this.model.get('location').get('course'));
        this.$el.find('.set-date').datepicker({ 'dateFormat': 'm/d/yy' });

        // Avoid showing broken image on mistyped/nonexistent image
        this.$el.find('img.course-image').error(function() {
            $(this).hide();
        });
        this.$el.find('img.course-image').load(function() {
            $(this).show();
        });

        var dateIntrospect = new Date();
        this.$el.find('#timezone').html("(" + dateIntrospect.getTimezone() + ")");

        this.listenTo(this.model, 'invalid', this.handleValidationError);
        this.listenTo(this.model, 'change', this.showNotificationBar);
        this.selectorToField = _.invert(this.fieldToSelectorMap);
    },

    render: function() {
        this.setupDatePicker('start_date');
        this.setupDatePicker('end_date');
        this.setupDatePicker('enrollment_start');
        this.setupDatePicker('enrollment_end');

        this.$el.find('#' + this.fieldToSelectorMap['overview']).val(this.model.get('overview'));
        this.codeMirrorize(null, $('#course-overview')[0]);

        this.$el.find('.current-course-introduction-video iframe').attr('src', this.model.videosourceSample());
        this.$el.find('#' + this.fieldToSelectorMap['intro_video']).val(this.model.get('intro_video') || '');
        if (this.model.has('intro_video')) {
            this.$el.find('.remove-course-introduction-video').show();
        }
        else this.$el.find('.remove-course-introduction-video').hide();

        this.$el.find('#' + this.fieldToSelectorMap['effort']).val(this.model.get('effort'));

        var imageURL = this.model.get('course_image_asset_path');
        this.$el.find('#course-image-url').val(imageURL)
        this.$el.find('#course-image').attr('src', imageURL);
        this.load_overview();
        return this;
    },
    fieldToSelectorMap : {
        'start_date' : "course-start",
        'end_date' : 'course-end',
        'enrollment_start' : 'enrollment-start',
        'enrollment_end' : 'enrollment-end',
        'overview' : 'course-overview',
        'intro_video' : 'course-introduction-video',
        'effort' : "course-effort",
        'course_image_asset_path': 'course-image-url'
    },

    updateTime : function(e) {
        var now = new Date();
        var hours = now.getHours();
        var minutes = now.getMinutes();
        $(e.currentTarget).attr('title', (hours % 12 === 0 ? 12 : hours % 12) + ":" + (minutes < 10 ? "0" : "")  +
                now.getMinutes() + (hours < 12 ? "am" : "pm") + " (current local time)");
    },

    setupDatePicker: function (fieldName) {
        var cacheModel = this.model;
        var div = this.$el.find('#' + this.fieldToSelectorMap[fieldName]);
        var datefield = $(div).find("input:.date");
        var timefield = $(div).find("input:.time");
        var cachethis = this;
        var setfield = function () {
            var date = datefield.datepicker('getDate');
            if (date) {
                var time = timefield.timepicker("getSecondsFromMidnight");
                if (!time) {
                    time = 0;
                }
                var newVal = new Date(date.getTime() + time * 1000);
                if (!cacheModel.has(fieldName) || cacheModel.get(fieldName).getTime() !== newVal.getTime()) {
                    cachethis.clearValidationErrors();
                    cachethis.setAndValidate(fieldName, newVal);
                }
            }
            else {
                // Clear date (note that this clears the time as well, as date and time are linked).
                // Note also that the validation logic prevents us from clearing the start date
                // (start date is required by the back end).
                cachethis.clearValidationErrors();
                cachethis.setAndValidate(fieldName, null);
            }
        };

        // instrument as date and time pickers
        timefield.timepicker({'timeFormat' : 'H:i'});
        datefield.datepicker();

        // Using the change event causes setfield to be triggered twice, but it is necessary
        // to pick up when the date is typed directly in the field.
        datefield.change(setfield);
        timefield.on('changeTime', setfield);
        timefield.on('input', setfield);

        datefield.datepicker('setDate', this.model.get(fieldName));
        // timepicker doesn't let us set null, so check that we have a time
        if (this.model.has(fieldName)) {
            timefield.timepicker('setTime', this.model.get(fieldName));
        } // but reset the field either way
        else {
            timefield.val('');
        }
    },

    updateModel: function(event) {
        switch (event.currentTarget.id) {
        case 'course-image-url':
            this.setField(event);
            var url = $(event.currentTarget).val();
            var image_name = _.last(url.split('/'));
            this.model.set('course_image_name', image_name);
            // Wait to set the image src until the user stops typing
            clearTimeout(this.imageTimer);
            this.imageTimer = setTimeout(function() {
                $('#course-image').attr('src', $(event.currentTarget).val());
            }, 1000);
            break;
        case 'course-effort':
            this.setField(event);
            break;
        // Don't make the user reload the page to check the Youtube ID.
        // Wait for a second to load the video, avoiding egregious AJAX calls.
        case 'course-introduction-video':
            this.clearValidationErrors();
            var previewsource = this.model.set_videosource($(event.currentTarget).val());
            clearTimeout(this.videoTimer);
            this.videoTimer = setTimeout(_.bind(function() {
                this.$el.find(".current-course-introduction-video iframe").attr("src", previewsource);
                if (this.model.has('intro_video')) {
                    this.$el.find('.remove-course-introduction-video').show();
                }
                else {
                    this.$el.find('.remove-course-introduction-video').hide();
                }
            }, this), 1000);
            break;
        default: // Everything else is handled by datepickers and CodeMirror.
            break;
        }
    },

    removeVideo: function(event) {
        event.preventDefault();
        if (this.model.has('intro_video')) {
            this.model.set_videosource(null);
            this.$el.find(".current-course-introduction-video iframe").attr("src", "");
            this.$el.find('#' + this.fieldToSelectorMap['intro_video']).val("");
            this.$el.find('.remove-course-introduction-video').hide();
        }
    },
    codeMirrors : {},
    codeMirrorize: function (e, forcedTarget) {
        var thisTarget;
        if (forcedTarget) {
            thisTarget = forcedTarget;
            thisTarget.id = $(thisTarget).attr('id');
        } else if (e !== null) {
            thisTarget = e.currentTarget;
        } else
        {
            // e and forcedTarget can be null so don't deference it
            // This is because in cases where we have a marketing site
            // we don't display the codeMirrors for editing the marketing
            // materials, except we do need to show the 'set course image'
            // workflow. So in this case e = forcedTarget = null.
            return;
        }

        if (!this.codeMirrors[thisTarget.id]) {
            var cachethis = this;
            var field = this.selectorToField[thisTarget.id];
            this.codeMirrors[thisTarget.id] = CodeMirror.fromTextArea(thisTarget, {
                mode: "text/html", lineNumbers: true, lineWrapping: true,
                onChange: function (mirror) {
                    mirror.save();
                    cachethis.clearValidationErrors();
                    var newVal = mirror.getValue();
                    if (cachethis.model.get(field) != newVal) {
                        cachethis.setAndValidate(field, newVal);
                    }
                }
            });
        }
    },

    revertView: function() {
        // Make sure that the CodeMirror instance has the correct
        // data from its corresponding textarea
        var self = this;
        this.model.fetch({
            success: function() {
                self.render();
                _.each(self.codeMirrors,
                       function(mirror) {
                           var ele = mirror.getTextArea();
                           var field = self.selectorToField[ele.id];
                           mirror.setValue(self.model.get(field));
                       });
            },
            reset: true,
            silent: true});
    },
    setAndValidate: function(attr, value) {
        // If we call model.set() with {validate: true}, model fields
        // will not be set if validation fails. This puts the UI and
        // the model in an inconsistent state, and causes us to not
        // see the right validation errors the next time validate() is
        // called on the model. So we set *without* validating, then
        // call validate ourselves.
        this.model.set(attr, value);
        this.model.isValid();
    },

    showNotificationBar: function() {
        // We always call showNotificationBar with the same args, just
        // delegate to superclass
        CMS.Views.ValidatingView.prototype.showNotificationBar.call(this,
                                                                    this.save_message,
                                                                    _.bind(this.saveView, this),
                                                                    _.bind(this.revertView, this));
    },
    uploadImage: function(event) {
        event.preventDefault();
        var upload = new CMS.Models.FileUpload({
            title: gettext("Upload your course image."),
            message: gettext("Files must be in JPEG or PNG format."),
            mimeTypes: ['image/jpeg', 'image/png']
        });
        var self = this;
        var modal = new CMS.Views.UploadDialog({
            model: upload,
            onSuccess: function(response) {
                var options = {
                    'course_image_name': response.displayname,
                    'course_image_asset_path': response.url
                }
                self.model.set(options);
                self.render();
                $('#course-image').attr('src', self.model.get('course_image_asset_path'))
            }
        });
        $('.wrapper-view').after(modal.show().el);
    },
    updateModel_overview: function(event) {
        this.set_overview();
    },
    codeMirrors_overview : {},
    codeMirrors_author : {},
    codeMirrorize_overview: function (e, forcedTarget) {
        var thisTarget;
        if (forcedTarget) {
            thisTarget = forcedTarget;
            thisTarget.id = $(thisTarget).attr('id');
        } else if (e !== null) {
            thisTarget = e.currentTarget;
        } else
        {
            // e and forcedTarget can be null so don't deference it
            // This is because in cases where we have a marketing site
            // we don't display the codeMirrors for editing the marketing
            // materials, except we do need to show the 'set course image'
            // workflow. So in this case e = forcedTarget = null.
            return;
        }
        if (!this.codeMirrors_overview[thisTarget.id]) {
            var cachethis = this;
            var field = this.selectorToField[thisTarget.id];
            this.codeMirrors_overview[thisTarget.id] = CodeMirror.fromTextArea(thisTarget, {
                mode: "text/html", lineNumbers: true, lineWrapping: true,
                onChange: function (mirror) {
                    mirror.save();
                    cachethis.clearValidationErrors();
                    var newVal = mirror.getValue();
                    var course_overview=$('<section>'+cachethis.model.get('overview')+'</section>');
                    if (course_overview.find('.'+thisTarget.id).html() != newVal) {
                        cachethis.set_overview();
                    }
                   
                }
            });
        }
    },
    load_overview: function() {
        try{
           var course_overview=$('<section>'+this.model.get('overview')+'</section>');
           //var course_name=course_overview.find('.title h2').text();
           var course_org=course_overview.find('.course_org img').attr('src');
           
           var short_description=course_overview.find('.short_description').html();
           var about=course_overview.find('.about').html();
           var course_prerequisites=course_overview.find('.prerequisites').html();
           var flip_content=course_overview.find('.flip-content').html();
           var flip_content_faq=course_overview.find('.flip-content-faq').html();
           var pdf=course_overview.find('#pdf').attr('href');
           //this.codeMirrorize_overview(null, $('#flip-content')[0]);
           //this.codeMirrorize_overview(null, $('#flip-content-faq')[0]);
           //this.$el.find('#overview-course-name').val(course_name);
           this.$el.find('#overview-course-org-image').val(course_org);
           this.$el.find('#overview-outline-pdf').val(pdf);
           //this.codeMirrors_overview['flip-content'].setValue(flip_content);
           //this.codeMirrors_overview['flip-content-faq'].setValue(flip_content_faq);
           }
           catch(err)
           {
                alert('Course overview default configuration error!');
           }
           this.read_tinyMCE_value('short_description',short_description);
           this.read_tinyMCE_value('about',about);
           this.read_tinyMCE_value('prerequisites',course_prerequisites);
           this.read_tinyMCE_value('flip-content',flip_content);
           this.read_tinyMCE_value('flip-content-faq',flip_content_faq);
           this.load_course_author(course_overview);
           this.field_exist_init(course_overview);
           $('input:radio[value=general]').attr('checked',true);
           this.$el.find('.overview_advanced').css('display','none');
           this.load_overview_init=true;
        
       
    },
    set_overview: function() {
        if(this.load_overview_init)
        {
            var overview_model=$('<section>'+this.model.get('overview')+'</section>');
            var course_overview=$('<section>'+this.model.get('overview')+'</section>');
            this.default_information_init(course_overview);
            //course_overview.find('.title h2').html(this.$el.find('#overview-course-name').val());
            this.author_org_image_init(course_overview);
            this.course_outline_data_init(course_overview);
            this.course_faq_data_init(course_overview);
            //course_overview.find('.flip-content').html(this.codeMirrors_overview['flip-content'].getValue());
            //course_overview.find('.flip-content-faq').html(this.codeMirrors_overview['flip-content-faq'].getValue());
            course_overview.find('.short_description').html(tinyMCE.getInstanceById('short_description').getBody().innerHTML);
            course_overview.find('.about').html(tinyMCE.getInstanceById('about').getBody().innerHTML);
            course_overview.find('.prerequisites').html(tinyMCE.getInstanceById('prerequisites').getBody().innerHTML);
            course_overview.find('.flip-content').html(tinyMCE.getInstanceById('flip-content').getBody().innerHTML);
            course_overview.find('.flip-content-faq').html(tinyMCE.getInstanceById('flip-content-faq').getBody().innerHTML);
            course_overview.find('#pdf').attr('href',this.$el.find('#overview-outline-pdf').val());
            course_author=$('.authors_content').find('.author_item');
            this.author_data_init(course_overview,course_author);
            This=this;
            course_author.each(function(){
                This.author_item_init(course_overview,$(this).find('.course_author_name').val(),$(this).find('.course_author_image').val(),tinyMCE.getInstanceById($(this).attr('id')+'_textarea').getBody().innerHTML);
            });
            var compare_overview_model=overview_model.clone();
            var compare_course_overview=course_overview.clone();
            compare_overview_model.htmlClean();
            compare_course_overview.htmlClean();
            if(compare_overview_model.html()!=compare_course_overview.html())
            {
                this.model.set('overview',course_overview.html());
                this.model.isValid();
            }
        }
    },
    create_author_item:function(name,image_path,bio){
        var _name=name||"";
        var _image_path=image_path||"";
        var _bio=bio||"";
        var item=$('<div class="author_item"><br/><hr/><div><label for="course-overview">Course Author Name (First Name Last Name):</label><input type="text" autocomplete="off" placeholder="" value="" class="course_author_name input_overview long new-course-image-url"></div><div><label for="course-overview">Course Author Image(URL from Files & Uploads):</label><input type="text" autocomplete="off" placeholder="" value="" class="course_author_image input_overview long new-course-image-url"></div><div><label for="course-overview">Course Author Bio:</label><textarea class="tinymce text-editor course_author_bio mceEditor" mce_editable="true" style="height:200px;"></textarea></div><div><a class="remove-item" href="javascript:void(0);" style="display: block;"><span class="delete-icon"></span>Delete Author</a></div></div>');
        item.attr('id',"author_item_"+new Date().getTime()+Math.floor(Math.random()*999));
        item.find('.course_author_name').val(_name);
        item.find('.course_author_image').val(_image_path);
        var thisTarget = item.find('.course_author_bio')[0];
        var cachethis = this;
        thisTarget.id=item[0].id+"_textarea";
        $(thisTarget).addClass(thisTarget.id);
        
        item.find('.course_author_name').change(function(event) {
            cachethis.set_overview();
        });
        item.find('.course_author_image').change(function(event) {
            cachethis.set_overview();
        });
        item.find('.remove-item').click(function(event) {
            $(this).parent().parent().remove();
            cachethis.set_overview();
        });
        $('.authors_content').append(item);
        tinyMCE_cms_init(this,thisTarget.id,_bio);
        return item;
    },
    load_course_author:function(course_overview){
        course_author=course_overview.find('.teacher').children('div');
        $('.authors_content').empty();
        This=this;
        course_author.each(function(){
            var bio_p=$(this).children('div').eq(1).children('p');
            var bio_con=bio_p.length!=1?$(this).children('div').eq(1).children('span').eq(0).html():bio_p.eq(0).html();
            var author_item=This.create_author_item($(this).children('div').eq(1).find('h3 b').text(),$(this).find('.teacher-image img').attr('src'),bio_con);
        });
    },
    author_data_init:function(course_overview,author_item){ 
        if(course_overview.find('.teacher').length<1&&author_item.length>0)
        {
            course_overview.append($('<section class="course-staff"><h2><b>Course Staff</b></h2><article class="teacher"></article></section>'));
        }
        course_overview.find('.teacher').html('')
    },
    author_item_init:function(course_overview,name,image_path,bio){
        var _name=name||"";
        var _image_path=image_path||"";
        var _bio=bio||"";
        course_overview.find('.teacher').append($('\n<div style="float:left;padding-bottom:20px;">\n<div class="teacher-image" style="width:120px;float:left;">\n<img src="'+_image_path+'" style="margin:0 20 px 0" align="left">\n</div>\n<div style="float:left;width:460px;">\n<h3><b>'+_name+'</b></h3>\n<br>\n<span>'+_bio+'</span></div>\n</div>'));
    },
    addCourseAuthor:function(){
        var course_overview=$('<section>'+this.model.get('overview')+'</section>');
        if(course_overview.find('.teacher').length<1)
        {
            course_overview.append($('<section class="course-staff"><h2><b>Course Staff</b></h2><article class="teacher"></article></section>'));
        }
        this.create_author_item();
    },
    course_outline_data_init:function(course_overview){
        var co_flip_content=course_overview.find('.flip-content');
        var co_about=course_overview.find('.about');
        if(co_flip_content.length<1)
        {
            co_about.after($('<br/>\n<div class="flip-title" style="display:none;">\n<span class="flip-title-left">VIEW DETAILED COURSE OUTLINE</span><span class="flip-title-right">+ Expand</span>\n</div>\n<span>\n<div class="flip-content" style="display: none;">\n</div>\n</span>\n<div style="height:16px;"></div>'));
        }
        var co_pdf=course_overview.find('#pdf');
        var co_flip_title=course_overview.find('.flip-title');
        if(co_pdf.length<1)
        {
            var pdf_div=$('\n<p style="padding-left:20px;"><img alt="" src="/static/PepperIcon_Download.jpg">&nbsp;<a id="pdf" style="font-family: Arial; font-size: 14pt; line-height: 1.6em;" href="" target="_blank"><b><i>Download Detailed Course Outline</i></b></a></p>\n');
            if(co_flip_title.length>0)
            {
                co_flip_title.next().next().after(pdf_div);
            }
            else
            {
                co_about.after(pdf_div);
            }
        }
    },
    course_faq_data_init:function(course_overview){
        var co_flip_content=course_overview.find('.flip-content-faq');
        var co_about=course_overview.find('.about');
        var co_pdf=course_overview.find('#pdf');
        var co_flip_title_faq=course_overview.find('.flip-title-faq');
        var co_flip_title_outline=course_overview.find('.flip-title');
        var div=$('<br/>\n<div class="flip-title-faq" style="display:none;">\n<span class="flip-title-left-faq">FAQ</span><span class="flip-title-right-faq">+ Expand</span>\n</div>\n<span>\n<div class="flip-content-faq" style="display: none;">\n</div>\n</span>\n<div style="height:16px;"></div>');
        if(co_flip_content.length<1)
        {
            if(co_pdf.length>0)
            {
                co_pdf.parent().after(div);
            }
            else if(co_flip_title_outline.length>0&&co_pdf.length<1)
            {
                co_flip_title_outline.next().next().after(div);
            }
            else if(co_flip_title_outline.length<1&&co_pdf.length<1)
            {
                co_about.after(div);
            }
        }
    },
    field_exist_init:function(course_overview){
        var co_ways=course_overview.find('.ways');
        var co_flip_title=course_overview.find('.flip-title');
        var co_pdf=course_overview.find('#pdf').parent();
        var co_flip_title_faq=course_overview.find('.flip-title-faq');
        var el_ways=this.$el.find('#way_cbox');
        var el_outline=this.$el.find('#outline_cbox');
        var el_pdf=this.$el.find('#pdf_cbox');
        var el_faq=this.$el.find('#faq_cbox');
        if(co_ways.css('display')=='block')
        {
            el_ways.attr("checked", true);
        }
        else
        {
            el_ways.attr("checked", false);
        }
        if(co_flip_title.css('display')=='block')
        {
            el_outline.attr("checked", true);
        }
        else
        {
            el_outline.attr("checked", false);
        }
        if(co_pdf.css('display')=='block')
        {
            el_pdf.attr("checked", true);
        }
        else
        {
            el_pdf.attr("checked", false);
        }
        if(co_flip_title_faq.css('display')=='block')
        {
            el_faq.attr("checked", true);
        }
        else
        {
            el_faq.attr("checked", false);
        }
        var This=this;
        $(".field-exist").click(function(){
            if ($(this).attr('checked')==undefined) {
                if(this.id=='outline_cbox')
                {
                    co_flip_title.css('display','none');
                }
                else if(this.id=='way_cbox')
                {
                    co_ways.css('display','none');
                }
                else if(this.id=='pdf_cbox')
                {
                    co_pdf.css('display','none');
                }
                else if(this.id=='faq_cbox')
                {
                    co_flip_title_faq.css('display','none');
                }
            }
            else
            {
                if(this.id=='outline_cbox')
                {
                    co_flip_title.css('display','block');
                }
                else if(this.id=='way_cbox')
                {
                    co_ways.css('display','block');
                }
                else if(this.id=='pdf_cbox')
                {
                    co_pdf.css('display','block');
                }
                else if(this.id=='faq_cbox')
                {
                    co_flip_title_faq.css('display','block');
                }
            }
            This.model.set('overview',course_overview.html());
            This.set_overview();
        })
    },
    overview_switch:function(event){
        this.overview_mode=event.target.value;
        this.set_overview_mode();
    },
    set_overview_mode:function(){
        if(this.overview_mode=='general')
        {
            this.$el.find('.overview_general').css('display','block');
            this.$el.find('.overview_advanced').css('display','none');
            this.load_overview();
        }
        else
        {
            this.$el.find('.overview_general').css('display','none');
            this.$el.find('.overview_advanced').css('display','block');
            this.codeMirrors['course-overview'].setValue(this.model.get('overview'));
        }
    },
    author_org_image_init:function(course_overview){
        if(this.$el.find('#overview-course-org-image').val()!="")
        {
            if(course_overview.find('.course_org').length<1)
            {
                course_overview.append('<section class="course_org"><img src="" width="320" height="211"></section>');
            }
            course_overview.find('.course_org img').attr('src',this.$el.find('#overview-course-org-image').val());
        }
        else
        {
            course_overview.find('.course_org').remove();
        }
    },
    read_tinyMCE_value:function(name,details)
    {   
        try
        {
            tinyMCE.getInstanceById(name).getBody().innerHTML=details;
        }
        catch(err){
            tinyMCE_cms_init(this,name,details)
        };
    },
    default_information_init:function(course_overview)
    {
        if(course_overview.find('.title').length<1)
        {
            course_overview.prepend('<section class="title"><h2></h2></section>\n');
        }
        if(course_overview.find('.short_description').length<1)
        {
          course_overview.find('.title').after('<section class="short_description"></section>\n');
        }
        if(course_overview.find('.about').length<1)
        {
          course_overview.find('.short_description').after('<section class="about"></section>\n');
        }
        
    }
});

jQuery.fn.htmlClean = function() {
this.contents().filter(function() {
if (this.nodeType != 3) {
$(this).htmlClean();
return false;
}
else {
//this.textContent = $.trim(this.textContent);
return !/\S/.test(this.nodeValue);
}
}).remove();
return this;
}
function tinyMCE_cms_init(CMS_Details,name,details)
{   
    tinyMCE.init({
      // General options
      mode : "textareas",
      editor_selector : name,
      theme : "advanced",
      forced_root_block:'',
      // Theme options
      theme_advanced_buttons1 : "bold,italic,underline,|,link,unlink,|,bullist,outdent,indent,|,justifyleft,justifycenter,justifyright,justifyfull",
      theme_advanced_resizing : false,
      content_css : "/static/css/tiny-mce.css",
      setup : function(ed) {
        ed.onInit.add(function(ed, evt) {
            ed.getBody().innerHTML=details;
        }),
        ed.onChange.add(function(ed, evt) {
            CMS_Details.set_overview();
        })
     }
    });
}