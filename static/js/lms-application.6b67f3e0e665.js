(function($, undefined) {
  var form_ext;
  $.form_ext  = form_ext = {
    ajax: function(options) {
      return $.ajax(options);
    },
    handleRemote: function(element) {
      var method = element.attr('method');
      var url = element.attr('action');
      var data = element.serializeArray();
      var options = {
        type: method || 'GET',
        data: data,
        dataType: 'text json',
        success: function(data, status, xhr) {
          element.trigger("ajax:success", [data, status, xhr]);
        },
        complete: function(xhr, status) {
          element.trigger("ajax:complete", [xhr, status]);
        },
        error: function(xhr, status, error) {
          element.trigger("ajax:error", [xhr, status, error]);
        }
      }
      if(url) { options.url = url; }
      return form_ext.ajax(options)
    },
    CSRFProtection: function(xhr) {
      var token = $.cookie('csrftoken');
      if (token) xhr.setRequestHeader('X-CSRFToken', token);
    }
  }
  $.ajaxPrefilter(function(options, originalOptions, xhr){ if ( !options.crossDomain ) { form_ext.CSRFProtection(xhr); }});
  $(document).delegate('form', 'submit', function(e) {
    var form = $(this),
    remote = form.data("remote") !== undefined;

    if(remote) {
      form_ext.handleRemote(form);
      return false;
    }

  });
})(jQuery);

$(document).ready(function () {
  $('a.dropdown').toggle(function() {
    $('ul.dropdown-menu').addClass("expanded");
    $('a.dropdown').addClass("active");
  }, function() {
    $('ul.dropdown-menu').removeClass("expanded");
    $('a.dropdown').removeClass("active");
  });
});

(function($){
  $.fn.extend({
    leanModal: function(options) {
      var defaults = {
        top: 100,
        overlay: 0.5,
        closeButton: null,
        position: 'fixed'
      }
      
      if ($("#lean_overlay").length == 0) {
        var overlay = $("<div id='lean_overlay'></div>");
        $("body").append(overlay);
      }

      options =  $.extend(defaults, options);

      return this.each(function() {
        var o = options;

        $(this).click(function(e) {

          $(".modal").hide();

          var modal_id = $(this).attr("href");
          
          if ($(modal_id).hasClass("video-modal")) {
            //Video modals need to be cloned before being presented as a modal
            //This is because actions on the video get recorded in the history.
            //Deleting the video (clone) prevents the odd back button behavior.
            var modal_clone = $(modal_id).clone(true, true);
            modal_clone.attr('id', 'modal_clone');
            $(modal_id).after(modal_clone);
            modal_id = '#modal_clone';
          }


          $("#lean_overlay").click(function() {
             close_modal(modal_id);
          });

          $(o.closeButton).click(function() {
             close_modal(modal_id);
          });

          var modal_height = $(modal_id).outerHeight();
          var modal_width = $(modal_id).outerWidth();

          $('#lean_overlay').css({ 'display' : 'block', opacity : 0 });
          $('#lean_overlay').fadeTo(200,o.overlay);

          $('iframe', modal_id).attr('src', $('iframe', modal_id).data('src'));
          $(modal_id).css({
            'display' : 'block',
            'position' : o.position,
            'opacity' : 0,
            'z-index': 11000,
            'left' : 50 + '%',
            'margin-left' : -(modal_width/2) + "px",
            'top' : o.top + "px"
          })

          $(modal_id).fadeTo(200,1);
          $(modal_id).find(".notice").hide().html("");
          var notice = $(this).data('notice')
          if(notice !== undefined) {
            $notice = $(modal_id).find(".notice");
            $notice.show().html(notice);
            // This is for activating leanModal links that were in the notice. We should have a cleaner way of
            // allowing all dynamically added leanmodal links to work.
            $notice.find("a[rel*=leanModal]").leanModal({ top : 120, overlay: 1, closeButton: ".close-modal", position: 'absolute' });
          }
          window.scrollTo(0, 0);
          e.preventDefault();

        });
      });

      function close_modal(modal_id){
        $("#lean_overlay").fadeOut(200);
        $('iframe', modal_id).attr('src', '');
        $(modal_id).css({ 'display' : 'none' });
        if (modal_id == '#modal_clone') {
          $(modal_id).remove();
        }
      }
    }
  });

  $("a[rel*=leanModal]").each(function(){
    $(this).leanModal({ top : 120, overlay: 1, closeButton: ".close-modal", position: 'absolute' });
    embed = $($(this).attr('href')).find('iframe')
    if(embed.length > 0) {
      if(embed.attr('src').indexOf("?") > 0) {
          embed.data('src', embed.attr('src') + '&autoplay=1&rel=0');
          embed.attr('src', '');
      } else {
          embed.data('src', embed.attr('src') + '?autoplay=1&rel=0');
          embed.attr('src', '');
      }
    }
  });
})(jQuery);

$(function() {
  if ($('.filter nav').length > 0) {
    var offset = $('.filter nav').offset().top;

    $(window).scroll(function() {
      if (offset <= window.pageYOffset) {
        return $('.filter nav').addClass('fixed-top');
      }
      else if (offset >= window.pageYOffset) {
        return $('.filter nav').removeClass('fixed-top');
      }
    });
  }
});

// http://james.padolsey.com/javascript/bujs-1-getparameterbyname/
function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)')
                    .exec(window.location.search);

    return match ?
        decodeURIComponent(match[1].replace(/\+/g, ' '))
        : null;
}

// checks whether or not the url is external to the local site.
// generously provided by StackOverflow: http://stackoverflow.com/questions/6238351/fastest-way-to-detect-external-urls
window.isExternal = function (url) {
    // parse the url into protocol, host, path, query, and fragment. More information can be found here: http://tools.ietf.org/html/rfc3986#appendix-B
    var match = url.match(/^([^:\/?#]+:)?(?:\/\/([^\/?#]*))?([^?#]+)?(\?[^#]*)?(#.*)?/);
    // match[1] matches a protocol if one exists in the url
    // if the protocol in the url does not match the protocol in the window's location, this url is considered external
    if (typeof match[1] === "string" &&
            match[1].length > 0 &&
            match[1].toLowerCase() !== location.protocol)
        return true;
    // match[2] matches the host if one exists in the url
    // if the host in the url does not match the host of the window location, this url is considered external
    if (typeof match[2] === "string" &&
            match[2].length > 0 &&
            // this regex removes the port number if it patches the current location's protocol
            match[2].replace(new RegExp(":("+{"http:":80,"https:":443}[location.protocol]+")?$"), "") !== location.host)
        return true;
    return false;
};

// Utility method for replacing a portion of a string.
window.rewriteStaticLinks = function(content, from, to) {
    if (from === null || to === null) {
        return content
    }

    var regex = new RegExp(from, 'g');
    return content.replace(regex, to)
};
