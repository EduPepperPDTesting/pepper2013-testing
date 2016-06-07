# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465223109.959421
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/common/templates/mathjax_include.html'
_template_uri = u'/mathjax_include.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        mathjax_mode = context.get('mathjax_mode', UNDEFINED)
        Undefined = context.get('Undefined', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer(u'\n\n')
        # SOURCE LINE 9
        if mathjax_mode is not Undefined and mathjax_mode == 'wiki':
            # SOURCE LINE 10
            __M_writer(u'<script type="text/x-mathjax-config">\n  MathJax.Hub.Config({\n    tex2jax: {inlineMath: [ [\'$\',\'$\'], ["\\\\(","\\\\)"]],\n              displayMath: [ [\'$$\',\'$$\'], ["\\\\[","\\\\]"]]}\n  });\n</script>\n')
            # SOURCE LINE 16
        else:
            # SOURCE LINE 17
            __M_writer(u'<script type="text/x-mathjax-config">\n  MathJax.Hub.Config({\n    tex2jax: {\n      inlineMath: [\n        ["\\\\(","\\\\)"],\n        [\'[mathjaxinline]\',\'[/mathjaxinline]\']\n      ],\n      displayMath: [\n        ["\\\\[","\\\\]"],\n        [\'[mathjax]\',\'[/mathjax]\']\n      ]\n    }\n  });\n</script>\n')
        # SOURCE LINE 32
        __M_writer(u'\n<!-- This must appear after all mathjax-config blocks, so it is after the imports from the other templates.\n     It can\'t be run through static.url because MathJax uses crazy url introspection to do lazy loading of\n     MathJax extension libraries -->\n<script type="text/javascript" src="/static/js/vendor/mathjax-MathJax-c9db6ac/MathJax.js?config=TeX-AMS-MML_SVG-full"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


