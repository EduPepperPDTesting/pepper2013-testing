(function ($) {
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.admin-menu-holder').length) {
            $(".admin-dropdown-menu").hide();
        } else if ($(event.target).closest(".outside_menu").length) {
            $(".admin-dropdown-menu").hide();
        }
        if ($('#user-photo-arrow:hidden').length){
            $('#user-photo-arrow').css("visibility", "visible");
        }
    });

    $(document).ready(function(){
        var $dropdown = $('#pepper-dropdown');
        var $nav = $(".nav-option-ol li");
        var $user_arrow = $('#user-photo-arrow');
        var $dropdown_menu = $('ul.pepper-dropdown-menu');
        var $admin_dropdown = $(".admin-dropdown-menu");

        $(".pepper-configuration").click(function(event){
            var e = window.event || event;
            if (e.stopPropagation) {
                e.stopPropagation();
            } else {
                e.cancelBubble = true;
            }
            if ($dropdown.hasClass("active")){
                $dropdown_menu.removeClass("expanded");
                $dropdown.removeClass("active");
            }
            var $tmp_el = $("#admin-dropdown-menu-" + $(this).attr("mid"));
            if ($tmp_el.length > 0){
                if($tmp_el.is(":visible"))
                    $tmp_el.hide();
                else{
                    $admin_dropdown.hide();
                    $tmp_el.show();
                }
            }
        });

        $dropdown.click(function(event) {
            if ($(this).hasClass("active")){
                $dropdown_menu.removeClass("expanded");
                $(this).removeClass("active");
                $user_arrow.css("visibility", "visible");
            } else {
                $dropdown_menu.addClass("expanded");
                $dropdown.addClass("active");
                $admin_dropdown.hide();
                $(document).one("click", function(){
                    $dropdown_menu.removeClass("expanded");
                    $dropdown.removeClass("active");
                });
                $user_arrow.css("visibility", "hidden");
            }
            event.stopPropagation();
        });
        $('#me-dropdown').click(function(event){
            $user_arrow.css("visibility", "visible");
        });
        $dropdown.mouseover(function(){
            $(this).find(".nav-option-text-left").show();
        });
        $dropdown.mouseout(function(){
            $(this).find(".nav-option-text-left").hide();
        });
        $nav.mouseover(function(){
            $(this).find(".nav-option-text").show();
        });
        $nav.mouseout(function(){
            $(this).find(".nav-option-text").hide();
        });

        $(".control.global_task_panel").each(function(){
            new GlobalTaskPanelControl(this)
        });
    });
})(jQuery);