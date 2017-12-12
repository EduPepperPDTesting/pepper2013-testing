<%!
    from django.core.urlresolvers import reverse
%>

function UrlResolver(signature, arguments) {
    var ResolvedUrl = '';

    $.ajax({
        async: false,
        url: "${reverse('pepper_utilities_js_url_lookup')}",
        data: {signature: signature, arguments: arguments},
        success: function (data) {
            ResolvedUrl = data.url;
        }
    });

    return ResolvedUrl;
}