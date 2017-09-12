(function($) {
    function hasAttr(node, name) {
        var attr = $(node).attr(name);
        return (typeof attr !== typeof undefined && attr !== false);
    }
    function show_selection(c) {
        c.$selection.html("");
        var $tr;
        $.each($(c).get_selection(true), function(j, v) {
            $tr = $("<tr/>").appendTo(c.$selection);
            var $td = $("<td class='item'>" + $.trim(v.text) + "</td> ").appendTo($tr),
                $input = $("<input class='remove' type='checkbox' checked/>").prependTo($td);
            $td.click(function(e) {
                if (e.target == this)
                    $(this).find("input").click();
            });
            $input.change(function(){
                $(this).parent().parent().remove();
                c.$table.find("input").eq(v.pos).prop("checked", false);
                $(c).trigger("change");
                if(!c.$selection.find("input").length){
                    c.$menu_selection.hide();
                }
            });
        });        
        if($(c).get_selection().length) c.$menu_selection.show(); else c.$menu_selection.hide();
    }
    function load_items(c){
        c.$table.html("");
        c.$selection.html("");
        c.$menu_selection.hide();
        var $tr;
        $(c).find("option").each(function(i, option){
            $tr = $("<tr/>").appendTo(c.$table);
            var value = $.trim(hasAttr(option, "value") ? $(option).attr("value") : $(option).text());
            var check_able = true; //$(option).hasAttr("checkbox");
            var $td = $("<td class='item'/>").appendTo($tr);
            $td.html($.trim($(option).text()));
            if(check_able){
                var $input = $("<input type='checkbox'/>").prependTo($td);
                $input.attr("value", value);
            }
            $td.click(function(e){
                if(e.target == this){
                    $(this).find("input").prop('checked', !$(this).find("input").prop('checked')).change();
                }
            }).find("input").change(function(e) {
                e.stopPropagation();
            });
        });
    }
    function init(c){
        var $box = c.$box = $("<div class='mul-drop-button-box'/>").insertBefore(c);
        var $button = c.$button = $("<div class='mul-drop-button'/>").appendTo($box);
        var $menu = c.$menu = $("<div class='mul-drop-menu'/>").appendTo($box).hide();
        var $menu_selection = c.$menu_selection = $("<div class='mul-drop-menu-selection'/>").appendTo($box).hide();
        var $filter = c.$filter = $("<div class='filter'></div>").appendTo($menu);
        var $filter_input = c.$filter_input = $("<input type='text'/>").appendTo($filter);
        var $check_all = $("<input type='checkbox'>").prependTo($("<label class='check-all-label'>All</label>").appendTo($filter));
        $check_all.click(function(){
            if(this.checked)
                $(c).check_all();
            else
                $(c).clear_all();
        });
        var $selection = c.$selection = $("<table class='selection'/>").appendTo($menu_selection);
        var $table = c.$table = $("<table class='list'/>").appendTo($("<div class='list-scroll'/>").appendTo($menu));
        $(document).click(function(e){
            if(!($box[0].contains(e.target)) && $menu.is(":visible")){
                $menu.hide();
                show_selection(c);
                $(c).trigger("change");
            }
        });
        c.$button.click(function(){
            if($menu.is(":visible"))
                show_selection(c);
            else{
                $menu_selection.hide();
                $(c).trigger("change");
            }
            $menu.toggle();
        });
        c.$button.append("<div class='label'>" + $(c).attr("label") + "</div>");
        $filter_input.on("keyup", function(e) {
            var value = $.trim($(this).val()).toLowerCase();
            var $table = c.$table;
            var values = [];
            $table.find("tr").each(function(i, input) {
                var text = $.trim($(this).text()).toLowerCase();
                if(value.length){
                    if(text.indexOf(value)==0 && $(this).find("input").length)
                        $(this).show();
                    else
                        $(this).hide();
                }else{
                    $(this).show();
                }
            });
        });
        load_items(c);
    }
    $.fn.check_all = function() {
        this.each(function(i, c){
            var $table = c.$table;
            $table.find("tr:visible td input").prop("checked", true);
        });
    }
    $.fn.clear_all = function() {
        this.each(function(i, c){
            var $table = c.$table;
            $table.find("tr td input").prop("checked", false);
            show_selection(c);
        });
    }     
    $.fn.get_selection = function(verbose) {
        if(!this.length) return null;
        var $table = this[0].$table;
        var values = [];
        $table.find("td input").each(function(i, input){
            if($(input).is(":checked")){
                if(verbose)
                    values.push({pos: i, value: $(input).attr("value"), text: $(input).parent().text()});
                else
                    values.push($(input).attr("value"));
            }
        });
        return values;
    }
    $.fn.reload = function() {
        this.each(function(i, v){
            load_items(this);
        });
    }
    $.fn.multi_sele_dropdown = function() {
        this.hide();
        this.each(function(i, v){
            init(v);
        });
        return this;
    };
})(jQuery);
