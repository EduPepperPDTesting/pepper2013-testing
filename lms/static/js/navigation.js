(function ($) {
    $('.pepper-configuration').click(function (e) {
        e.preventDefault();
        $('.admin ul.pepper-dropdown-menu').toggle();
    });

    $(document).on('click', function(event) {
        if (!$(event.target).closest('.pepper-menu-holder').length) {
            $(".pepper-dropdown-menu").hide();
        }
    });

    var url_split_array = window.location.href.split('/');
    var split_array_1 = "";
    var split_keyword = "";
    var url_using = "#";
    var str1 = "https://studio";
    var str2 = ".pepperpd.com";

    if (url_split_array.length > 2){
        split_array_1 = url_split_array[2].split('.');
        split_keyword = split_array_1[0];
    }

    if (split_keyword === "www0"){
        url_using = str1 + "0" + str2;
    }
    else if(split_keyword === "www"){
        url_using = str1 + str2;
    }
    else{
        url_using = str1 + "-" + split_keyword + str2;
    }
    $("#org_tsm_studio_obj").attr("href", url_using);

    $(".control.global_task_panel").each(function(){
        new GlobalTaskPanelControl(this)
    });
})(jQuery);