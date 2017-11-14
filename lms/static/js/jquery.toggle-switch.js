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
        var old = 0;
        $switch.on("mousedown", function(e){
            e.preventDefault();
            x = e.clientX;
            y = e.clientY;
            drag = true;
            current = parseInt($(this).css("margin-left")) || 0;
        });
        $(document).on("mouseup", function(){
            drag = false;
            if($(self).hasClass("left")){
                value = -1;
            }else if($(self).hasClass("right")){
                value = 1;
            }else{
                value = 0;
            }
            if(value != old){
                $(self).trigger("change", [value]);
            }
            $switch.css("margin-left", '');
            old = value;
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
    });
    var self = this;
    ret.val = function(v){
        if(typeof(v) == "undefined"){
            if(self.length){
                if(self.eq(0).hasClass("left")){
                    return -1;
                }else if(self.eq(0).hasClass("right")){
                    return 1;
                }else{
                    return 0;
                }
            }           
        }else{
            self.removeClass("left");
            self.removeClass("right");
            if(v == -1){
                self.addClass("left")
            }else if(v == 1){
                self.addClass("right")
            }
        }
    }
    return ret;
}
