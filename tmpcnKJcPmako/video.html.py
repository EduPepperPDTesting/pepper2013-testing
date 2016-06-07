# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465230993.659083
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/video.html'
_template_uri = 'video.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        data_dir = context.get('data_dir', UNDEFINED)
        sub = context.get('sub', UNDEFINED)
        start = context.get('start', UNDEFINED)
        track = context.get('track', UNDEFINED)
        sources = context.get('sources', UNDEFINED)
        show_captions = context.get('show_captions', UNDEFINED)
        yt_test_timeout = context.get('yt_test_timeout', UNDEFINED)
        yt_test_url = context.get('yt_test_url', UNDEFINED)
        caption_asset_path = context.get('caption_asset_path', UNDEFINED)
        end = context.get('end', UNDEFINED)
        autoplay = context.get('autoplay', UNDEFINED)
        id = context.get('id', UNDEFINED)
        youtube_streams = context.get('youtube_streams', UNDEFINED)
        display_name = context.get('display_name', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        if display_name is not UNDEFINED and display_name is not None:
            # SOURCE LINE 4
            __M_writer(u'    <h2>')
            __M_writer(filters.decode.utf8(display_name))
            __M_writer(u'</h2>\n')
        # SOURCE LINE 6
        __M_writer(u'\n<div\n    id="video_')
        # SOURCE LINE 8
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'"\n    class="video"\n\n    data-streams="')
        # SOURCE LINE 11
        __M_writer(filters.decode.utf8(youtube_streams))
        __M_writer(u'"\n\n    ')
        # SOURCE LINE 13
        __M_writer(filters.decode.utf8('data-sub="{}"'.format(sub) if sub else ''))
        __M_writer(u'\n    ')
        # SOURCE LINE 14
        __M_writer(filters.decode.utf8('data-autoplay="{}"'.format(autoplay) if autoplay else ''))
        __M_writer(u'\n\n    ')
        # SOURCE LINE 16
        __M_writer(filters.decode.utf8('data-mp4-source="{}"'.format(sources.get('mp4')) if sources.get('mp4') else ''))
        __M_writer(u'\n    ')
        # SOURCE LINE 17
        __M_writer(filters.decode.utf8('data-webm-source="{}"'.format(sources.get('webm')) if sources.get('webm') else ''))
        __M_writer(u'\n    ')
        # SOURCE LINE 18
        __M_writer(filters.decode.utf8('data-ogg-source="{}"'.format(sources.get('ogv')) if sources.get('ogv') else ''))
        __M_writer(u'\n\n    data-caption-data-dir="')
        # SOURCE LINE 20
        __M_writer(filters.decode.utf8(data_dir))
        __M_writer(u'"\n    data-show-captions="')
        # SOURCE LINE 21
        __M_writer(filters.decode.utf8(show_captions))
        __M_writer(u'"\n    data-start="')
        # SOURCE LINE 22
        __M_writer(filters.decode.utf8(start))
        __M_writer(u'"\n    data-end="')
        # SOURCE LINE 23
        __M_writer(filters.decode.utf8(end))
        __M_writer(u'"\n    data-caption-asset-path="')
        # SOURCE LINE 24
        __M_writer(filters.decode.utf8(caption_asset_path))
        __M_writer(u'"\n    data-autoplay="')
        # SOURCE LINE 25
        __M_writer(filters.decode.utf8(autoplay))
        __M_writer(u'"\n    data-yt-test-timeout="')
        # SOURCE LINE 26
        __M_writer(filters.decode.utf8(yt_test_timeout))
        __M_writer(u'"\n    data-yt-test-url="')
        # SOURCE LINE 27
        __M_writer(filters.decode.utf8(yt_test_url))
        __M_writer(u'"\n\n')
        # SOURCE LINE 40
        __M_writer(u'    data-autohide-html5="False"\n\n    tabindex="-1"\n>\n    <div class="focus_grabber first"></div>\n\n    <div class="tc-wrapper">\n        <article class="video-wrapper">\n            <div class="video-player-pre"></div>\n\n            <section class="video-player">\n                <div id="')
        # SOURCE LINE 51
        __M_writer(filters.decode.utf8(id))
        __M_writer(u'"></div>\n                <h3 class="hidden">')
        # SOURCE LINE 52
        __M_writer(filters.decode.utf8(_('ERROR: No playable video sources found!')))
        __M_writer(u'</h3>\n            </section>\n\n            <div class="video-player-post"></div>\n\n            <section class="video-controls">\n                <div class="slider" title="Video position"></div>\n\n                <div>\n                    <ul class="vcr">\n                        <li><a class="video_control" href="#" title="')
        # SOURCE LINE 62
        __M_writer(filters.decode.utf8(_('Play')))
        __M_writer(u'" role="button" aria-disabled="false"></a></li>\n                        <li><div class="vidtime">0:00 / 0:00</div></li>\n                    </ul>\n                    <div class="secondary-controls">\n                        <div class="speeds">\n                            <a href="#" title="')
        # SOURCE LINE 67
        __M_writer(filters.decode.utf8(_('Speeds')))
        __M_writer(u'" role="button" aria-disabled="false">\n                                <h3>')
        # SOURCE LINE 68
        __M_writer(filters.decode.utf8(_('Speed')))
        __M_writer(u'</h3>\n                                <p class="active"></p>\n                            </a>\n                            <ol class="video_speeds"></ol>\n                        </div>\n                        <div class="volume">\n                            <a href="#" title="')
        # SOURCE LINE 74
        __M_writer(filters.decode.utf8(_('Volume')))
        __M_writer(u'" role="button" aria-disabled="false"></a>\n                            <div class="volume-slider-container">\n                                <div class="volume-slider"></div>\n                            </div>\n                        </div>\n                        <a href="#" class="add-fullscreen" title="')
        # SOURCE LINE 79
        __M_writer(filters.decode.utf8(_('Fill browser')))
        __M_writer(u'" role="button" aria-disabled="false">')
        __M_writer(filters.decode.utf8(_('Fill browser')))
        __M_writer(u'</a>\n                        <a href="#" class="quality_control" title="')
        # SOURCE LINE 80
        __M_writer(filters.decode.utf8(_('HD')))
        __M_writer(u'" role="button" aria-disabled="false">')
        __M_writer(filters.decode.utf8(_('HD')))
        __M_writer(u'</a>\n\n                        <a href="#" class="hide-subtitles" title="')
        # SOURCE LINE 82
        __M_writer(filters.decode.utf8(_('Turn off captions')))
        __M_writer(u'" role="button" aria-disabled="false">')
        __M_writer(filters.decode.utf8(_('Turn off captions')))
        __M_writer(u'</a>\n                    </div>\n                </div>\n            </section>\n        </article>\n\n        <ol class="subtitles" tabindex="0" title="Captions"><li></li></ol>\n    </div>\n\n    <div class="focus_grabber last"></div>\n<ul class="wrapper-downloads">\n')
        # SOURCE LINE 93
        if sources.get('main'):
            # SOURCE LINE 94
            __M_writer(u'    <li class="video-sources">\n        ')
            # SOURCE LINE 95
            __M_writer(filters.decode.utf8(('<a href="%s">' + _('Download video') + '</a>') % sources.get('main')))
            __M_writer(u'\n    </li>\n')
        # SOURCE LINE 98
        __M_writer(u'\n')
        # SOURCE LINE 99
        if track:
            # SOURCE LINE 100
            __M_writer(u'    <li class="video-tracks">\n        ')
            # SOURCE LINE 101
            __M_writer(filters.decode.utf8(('<a  target="_blank" href="%s">' + _('Download timed transcript') + '</a>') % track))
            __M_writer(u'\n    </li>\n')
        # SOURCE LINE 104
        __M_writer(u'</ul>\n</div>\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


