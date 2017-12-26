<%!
    from django.core.urlresolvers import reverse
%>

function UrlResolver(signature, arguments) {

    var key_string = signature;
    $.each(arguments, function (key, value) {
        key_string += key + value;
    });

    var resolved_url = sessionStorage.getItem(key_string);
    if (resolved_url) {
        return resolved_url;
    }

    $.ajax({
        async: false,
        url: "${reverse('pepper_utilities_js_url_lookup')}",
        data: {signature: signature, arguments: arguments},
        success: function (data) {
            resolved_url = data.url;
            sessionStorage.setItem(key_string, resolved_url);
        }
    });
    return resolved_url;
}