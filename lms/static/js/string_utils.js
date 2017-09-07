String.prototype.escape = function(chars, slashed) {
    return this.replace(new RegExp((slashed ? "\\\\":"") + "([" + chars + "])", "g"), function(a, b) {
        return "&#" + b.charCodeAt(0) +";"
    });
}
String.prototype.fillData = function(data) {
    function v(s){
        var parts = s.split("."), d = data, r;
        for(var i=0;i<parts.length;i++){
            var p = parts[i];
            if(p){r = d[p]; d = r}
            if(!d) break;
        }
        return r;
    }
    var c = 1;
    var s = this.replace(/{([\s\S]+)}/g, function(a, b) {
        return "{" + b.escape("?:!", true) + "}";
    });
    while(c) {
        c = 0;
        s = s.replace(/\{([^\{\}]+?)\}/g, function(match, key) {
            var m = null, r;  
            if(m = key.match(/^([\s\S]+?)\!([\s\S]*?)(?:\:([\s\S]*))?$/)) {
                r = !v(m[1]) ? m[2] : (typeof(m[3]) !="undefined" ? m[3] : "");
            } else if(m = key.match(/^([\s\S]+?)\?([\s\S]*?)(?:\:([\s\S]*))?$/)) {
                r = v(m[1]) ? m[2] : (typeof(m[3]) !="undefined" ? m[3] : "");
            } else {
                var t = v(key);
                r = typeof(t) != "undefined" ? String(t).escape("?:!", false) : "";
            }
            c = 1;
            return r;
        });
    }
    return s;
}
String.prototype.htmlEncode = function(value) {
    return $('<div/>').text(this).html();
}
