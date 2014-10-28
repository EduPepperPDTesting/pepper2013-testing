(function (requirejs, require, define) {
define('PollCompareMain', ['logme'], function (logme) {

PollCompareMain.prototype = {

'postInit': function () {
        logme("PollCompareMain postInit");
        logme("jsonConfig:");
        logme(JSON.stringify(this.jsonConfig))

        table_dom = this.pollCompareEl.find('.poll_compare_table');
        logme("post_init_1");
        table_head_num=this.pollCompareEl.find('.poll_compare_table li').length-1;
        table_colWidth=Math.floor(520/table_head_num);
        var i = 0;
        $.each(this.jsonConfig, function(index,value){
            i++;
            /*
            table_row_html ='' +
            '<ul>' +
                '<li class="row_left left"><div>'+ i + '. Thanks!!!'+ value.display_name +'.</div></li>' +

                '<li>' +    
                    '<ul class="row_right from">&nbsp</ul>' +
                    '<ul class="row_right to">&nbsp</ul>' +
                '</li>' +

                '<li>' +
                    '<ul class="row_right from">&nbsp</ul>' +
                    '<ul class="row_right to">&nbsp</ul>' +
                '</li>' +

                '<li>' +
                    '<ul class="row_right from">&nbsp</ul>' +
                    '<ul class="row_right to">&nbsp</ul>' +
                '</li>' +

                '<li>' +
                    '<ul class="row_right from">&nbsp</ul>' +
                    '<ul class="row_right to">&nbsp</ul>' +
                '</li>' +

                '<li>' +
                    '<ul class="row_right from">&nbsp</ul>' +
                    '<ul class="row_right to">&nbsp</ul>' +
                '</li>' +
            '</ul>';
            */
            table_row_html ='<ul><li class="row_left left"><div>'+ i + '.</div></li>';
            for(var j=0;j<table_head_num;j++)
            {
                table_row_html+='<li>' +    
                    '<ul class="row_right from">&nbsp</ul>' +
                    '<ul class="row_right to">&nbsp</ul>' +'</li>';
            }
            table_row_html+='</ul>';
            table_dom.append(table_row_html);
        }); // end of each
        var colTitle = table_dom.find(".colTitle");
        colTitle.width(table_colWidth);
        var maxHeight=60;
        colTitle.each(function(index, el) {
            var h = parseFloat($(el).height())
            if(h>maxHeight)
            {
                maxHeight=h;
            }
        });
        table_dom.find(".title123").height(maxHeight);
        ul_rowObjS = table_dom.children();

        //set display name
        $.each(this.jsonConfig,function(index,value){
            var rowIndex = parseInt(index.substr(8));
            ul_rowObjS[rowIndex].children[0].innerHTML= value.display_name;
        });

        $.each(this.jsonConfig,function(index,value){
            var from_num = 0;
            var to_num = 0;
            var rowIndex = 0;
            var tmp = index.substr(8);
            rowIndex = parseInt(tmp);
            student_answers_from = value['student_answers']['from_loc'];
            student_answers_to   = value['student_answers']['to_loc'];
            $.each(student_answers_from, function(_index,value){
               from_num = parseInt(value.split("_")[1])+1;
                switch(value)
                {
                    case "choice_one":
                        from_num = 1;
                        break;
                    case "choice_zeroone":
                        from_num = 2;
                        break;
                    case "choice_zeromore":
                        from_num = 3;
                        break;
                    case "choice_onemore":
                        from_num = 4;
                        break;
                    case "choice_noone":
                        from_num = 5;
                        break;
                }
            });
            
            $.each(student_answers_to,function(_index,value){
                to_num = parseInt(value.split("_")[1])+1;
                switch(value)
                {
                    case "choice_one":
                        to_num = 1;
                        break;
                    case "choice_zeroone":
                        to_num = 2;
                        break;
                    case "choice_zeromore":
                        to_num = 3;
                        break;
                    case "choice_onemore":
                        to_num = 4;
                        break;
                    case "choice_noone":
                        to_num = 5;
                        break;
                }
            });

            ul_rowObj = ul_rowObjS[rowIndex];
            li_colObjS = ul_rowObj.children; //li s
            for(var col = 0;col<from_num;col++)
            {
                li_colObj = li_colObjS[col+1]; //li
                ul_fromObj = li_colObj.children[0];           
                ul_fromObj.className = ul_fromObj.className + " set_blue";
            }
            for(var col = 0;col<to_num;col++)
            {
                li_colObj = li_colObjS[col+1]; //li
                ul_toObj = li_colObj.children[1];
                ul_toObj.className = ul_toObj.className + " set_green";
            }
        });// end of each jsconfig
        var max_left_width = 0;
        var title_cell_width = 0;
        var max_row_height = 70;
        //get max left cell width
        for(var i = 1;i<ul_rowObjS.length;i++)
        {
            if (ul_rowObjS[i].offsetHeight > max_row_height)
            {
                max_row_height = ul_rowObjS[i].offsetHeight;
            }

            if (ul_rowObjS[i].children[0].offsetWidth > max_left_width)
            {
                max_left_width = ul_rowObjS[i].children[0].offsetWidth;
            }
        }

        //set all other rows's height to the same height with the most heightest row
        for(var i = 1;i<ul_rowObjS.length;i++)
        {
            for(var j =0;j<ul_rowObjS[i].children.length;j++)
            {
                ul_rowObjS[i].children[j].offsetHeight = max_row_height;
                ul_rowObjS[i].children[j].style.height = "" + max_row_height + "px";
            }
        }
        table_dom.offsetHeight = max_row_height * i;
        
        //set other cells's width the same with title cells's width
        for(var i=1;i<ul_rowObjS.length;i++)
        {
            for(var j=1;j<ul_rowObjS[i].children.length;j++)
            {
                ul_rowObjS[i].children[j].style.width = "" + ul_rowObjS[0].children[j].offsetWidth -1 + "px";
                ul_rowObjS[i].children[j].offsetWidth = ul_rowObjS[0].children[j].offsetWidth -1;
                ul_rowObjS[i].children[j].children[0].offsetWidth = ul_rowObjS[0].children[j].offsetWidth -1;
                ul_rowObjS[i].children[j].children[0].style.width = "" + ul_rowObjS[0].children[j].offsetWidth -1 + "px";
                ul_rowObjS[i].children[j].children[1].offsetWidth = ul_rowObjS[0].children[j].offsetWidth -1;
                ul_rowObjS[i].children[j].children[1].style.width = "" + ul_rowObjS[0].children[j].offsetWidth -1 + "px";
            }
        }
        
        //set other cells's height the same with left cells's height
        for(var i =1;i<ul_rowObjS.length;i++)
        {
            for(var j=1;j<ul_rowObjS[i].children.length;j++)
            {
                ul_rowObjS[i].children[j].children[0].offsetHeight = ul_rowObjS[i].children[j].offsetHeight/2;
                ul_rowObjS[i].children[j].children[0].style.height = "" + ul_rowObjS[i].children[j].offsetHeight/2 + "px";
                ul_rowObjS[i].children[j].children[1].offsetHeight = ul_rowObjS[i].children[j].offsetHeight/2;
                ul_rowObjS[i].children[j].children[1].style.height = "" + ul_rowObjS[i].children[j].offsetHeight/2 + "px";
            }
        }

        //set left title's width
        for(var i = 0;i<ul_rowObjS.length;i++)
        {
            ul_rowObjS[i].children[0].offsetWidth = max_left_width;
            ul_rowObjS[i].children[0].style.width = "" + max_left_width + "px";
        }
            return;
    } // End-of: 'postInit': function () {
}; // End-of: PollMain.prototype = {

return PollCompareMain;

function PollCompareMain(el) {
    var _this;
    this.pollCompareEl = $(el).find('.poll_compare');
    if (this.pollCompareEl.length !== 1) {
        // We require one question DOM element.
        logme('ERROR: PollMain constructor requires one poll_compare DOM element.');

        return;
    }

    // Just a safety precussion. If we run this code more than once, multiple 'click' callback handlers will be
    // attached to the same DOM elements. We don't want this to happen.
    if (this.pollCompareEl.attr('poll_main_processed') === 'true') {
        logme(
            'ERROR: PollCompareMain JS constructor was called on a DOM element that has already been processed once.'
        );

        return;
    }

    // This element was not processed earlier.
    // Make sure that next time we will not process this element a second time.
    this.pollCompareEl.attr('poll_main_processed', 'true');

    // Access this object inside inner functions.
    _this = this;

    // DOM element which contains the current poll along with any conditionals. By default we assume that such
    // element is not present. We will try to find it.
    this.wrapperSectionEl = null;

    (function (tempEl, c1) {
        while (tempEl.tagName.toLowerCase() !== 'body') {
            tempEl = $(tempEl).parent()[0];
            c1 += 1;

            if (
                (tempEl.tagName.toLowerCase() === 'section') &&
                ($(tempEl).hasClass('xmodule_WrapperModule') === true)
            ) {
                _this.wrapperSectionEl = tempEl;

                break;
            } else if (c1 > 50) {
                // In case something breaks, and we enter an endless loop, a sane
                // limit for loop iterations.

                break;
            }
        }
    }($(el)[0], 0));



    try {
        this.jsonConfig = JSON.parse(this.pollCompareEl.children('.poll_compare_div').html());
        logme("this.jsonConfig:")
        logme(JSON.stringify(this.jsonConfig))

        this.student_answers = new Array();
        $.postWithPrefix(
            ''+ this.pollCompareEl.data('ajax-url') + '/' + "get_state", 
            {'data': JSON.stringify(this.jsonConfig)},
            function(response){
                console.log('success!');
                // console.log(JSON.stringify(response));
                $.each(response,function(index,value){
                    _this.jsonConfig[index] = value;
                })
                // _this.jsonConfig = response;
                logme("response:" + JSON.stringify(response));
                _this.postInit();
            }
        );

        return;
    } catch (err) {
        logme(
            'ERROR: Invalid JSON config for poll ID "' + this.id + '".',
            'Error messsage: "' + err.message + '".'
        );

        return;
    }
} // End-of: function PollMain(el) {

}); // End-of: define('PollMain', ['logme'], function (logme) {

// End-of: (function (requirejs, require, define) {
}(RequireJS.requirejs, RequireJS.require, RequireJS.define));
