
function EmbedVideo() {}

EmbedVideo.prototype.embed_JS = function(element_name, js_src, width, height) {
    var embed_code = "<script src='" + js_src + "?width=" + width + "&height=" + height + "' type='text/javascript'><\/script>";
    var iObj = document.getElementById(element_name).contentWindow;
    iObj.document.open();
    iObj.document.writeln("<html><head>");
    iObj.document.writeln(embed_code);
    iObj.document.writeln("</head><body></body></html>");
    iObj.document.close();
}

function setIframeAutoSize(obj) {
    obj.height = obj.contentWindow.document.documentElement.scrollHeight
    obj.width = obj.contentWindow.document.documentElement.scrollWidth
}