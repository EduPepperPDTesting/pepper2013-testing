function spExternalLink(callback, argument) {
    var link_create_url = UrlResolver('sp_link_create');
    $.ajax({
        url: link_create_url,
        dataType: 'html',
        success: function (data) {
            // Add the HTML to the page.
            $('body').append(data);

            // Handle the submission of the form.
            $('.sp-link-create').submit(function (e) {
                e.preventDefault();
                // The selected SP.
                var sp = $("select[name='sp']").val();
                // The link to the external page.
                var link = $("input[name='link']").val();
                // The SAML link to go to the external link.
                var saml_link = UrlResolver('sso_idp_acs_send') + '?sp=' + sp + '&RelayState=' + encodeURIComponent(link);
                // Remove the popup.
                $('.sp-link-backdrop').remove();
                // Call the callback function with the generated/encoded link if it exists.
                if (window[callback] instanceof Function) {
                    window[callback](saml_link, argument);
                } else {
                    alert("There was an error when adding this link.");
                }
            });

            // Add the close button handler.
            $('.sp-link-header a').click(function (e) {
                e.preventDefault();
                // Remove the popup.
                $('.sp-link-backdrop').remove();
            });
        }
    });
}
