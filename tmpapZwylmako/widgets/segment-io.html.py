# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223499.438134
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/widgets/segment-io.html'
_template_uri = u'widgets/segment-io.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        user = context.get('user', UNDEFINED)
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        if settings.MITX_FEATURES.get('SEGMENT_IO_LMS'):
            # SOURCE LINE 2
            __M_writer(u'<!-- begin Segment.io -->\n<script type="text/javascript">\n  var analytics=analytics||[];analytics.load=function(e){var t=document.createElement("script");t.type="text/javascript",t.async=!0,t.src=("https:"===document.location.protocol?"https://":"http://")+"d2dq2ahtl5zl1z.cloudfront.net/analytics.js/v1/"+e+"/analytics.min.js";var n=document.getElementsByTagName("script")[0];n.parentNode.insertBefore(t,n);var r=function(e){return function(){analytics.push([e].concat(Array.prototype.slice.call(arguments,0)))}},i=["identify","track","trackLink","trackForm","trackClick","trackSubmit","pageview","ab","alias","ready"];for(var s=0;s<i.length;s++)analytics[i[s]]=r(i[s])};\n  analytics.load("')
            # SOURCE LINE 5
            __M_writer(filters.decode.utf8( settings.SEGMENT_IO_LMS_KEY ))
            __M_writer(u'");\n\n')
            # SOURCE LINE 7
            if user.is_authenticated():
                # SOURCE LINE 8
                __M_writer(u'  analytics.identify("')
                __M_writer(filters.decode.utf8( user.id ))
                __M_writer(u'", {\n      email     : "')
                # SOURCE LINE 9
                __M_writer(filters.decode.utf8( user.email ))
                __M_writer(u'",\n      username  : "')
                # SOURCE LINE 10
                __M_writer(filters.decode.utf8( user.username ))
                __M_writer(u'"\n  });\n\n')
            # SOURCE LINE 14
            __M_writer(u'</script>\n<!-- end Segment.io -->\n')
            # SOURCE LINE 16
        else:
            # SOURCE LINE 17
            __M_writer(u'<!-- dummy segment.io -->\n<script type="text/javascript">\n  var analytics = {\n    track: function() { return; },\n    pageview: function() { return; }\n  };\n</script>\n<!-- end dummy segment.io -->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


