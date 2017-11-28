$.fn.toggleSwitch = function() {
    var ret = this.each(function() {
        if(this.inited) return;
        this.inited = true;
        var self = this;
        var $switch = $("<div class='switch'></div>").appendTo(this);
        var drag = false;
        var x = 0;
        var y = 0;
        var current = 0;
        $switch.on("mousedown", function(e){
            e.preventDefault();
            x = e.clientX;
            y = e.clientY;
            drag = true;
            current = parseInt($(this).css("margin-left")) || 0;
        });
        $(document).on("mouseup", function(){
            if($(self).hasClass("left")){
                value = -1;
            }else if($(self).hasClass("right")){
                value = 1;
            }else{
                value = 0;
            }
            

            if(drag)self.val(value);
            // if(value != $(self).data("old")){
            //     $(self).trigger("change", [value]);
            // }
            // $switch.css("margin-left", '');

            // $(self).data("old", value);

            drag = false;

   
        });
        $(document).on("mousemove", function(e){
    
            function between(a, b, c){
                if(a < b) return b;
                if(a > c) return c;
                return a;
            }
            if(drag){
                $(self).removeClass("left");
                $(self).removeClass("right");
                var m = between(current + e.clientX - x, 2, 32)
                $switch.css("margin-left", m + "px");
                if(m < 9){
                    $(self).addClass("left");
                }else if(m > 24){
                    $(self).addClass("right");
                }
            }
        });

        this.val = function (v){
            var old = $(self).data("old");
            $(self).data("old", v);
            if(typeof(v) == "undefined"){
                var V;
                if($(self).hasClass("left")){
                    V = -1;
                }else if($(self).hasClass("right")){
                    V = 1;
                }else{
                    V = 0;
                }
                return V;
            }else{
                if(v != old){
                    ret.trigger("change", [v]);
                }
                $(self).removeClass("left");
                $(self).removeClass("right");
                if(v == -1){
                    $(self).addClass("left")
                }else if(v == 1){
                    $(self).addClass("right")
                }
                $switch.css("margin-left", '');
            }
        }
    });
    ret.val = function(v) {
        if(ret.length)
            return ret[0].val(v);
    }
    return ret;
}
