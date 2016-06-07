# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1465230993.696418
_enable_loop = True
_template_filename = u'/usr/local/pcg/pepper/edx-platform/lms/templates/discussion/_underscore_templates.html'
_template_uri = u'discussion/_underscore_templates.html'
_source_encoding = 'utf-8'
_exports = []


# SOURCE LINE 1
from django.utils.translation import ugettext as _ 

# SOURCE LINE 2
from django_comment_client.permissions import has_permission 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        course = context.get('course', UNDEFINED)
        user = context.get('user', UNDEFINED)
        settings = context.get('settings', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n<script type="text/template" id="thread-template">\n    <article class="discussion-article" data-id="')
        # SOURCE LINE 5
        __M_writer(filters.decode.utf8('<%- id %>'))
        __M_writer(u'">\n        <div class="thread-content-wrapper"></div>\n        \n        <ol class="responses">\n            <li class="loading"><div class="loading-animation"></div></li>\n        </ol>\n        <div class="post-status-closed bottom-post-status" style="display: none">\n          ')
        # SOURCE LINE 12
        __M_writer(filters.decode.utf8(_("This thread is closed.")))
        __M_writer(u'\n        </div>\n        <!--\n')
        # SOURCE LINE 15
        if course is UNDEFINED or has_permission(user, 'create_comment', course.id):
            # SOURCE LINE 16
            __M_writer(u'        <form class="discussion-reply-new" data-id="')
            __M_writer(filters.decode.utf8('<%- id %>'))
            __M_writer(u'">\n            <h4>')
            # SOURCE LINE 17
            __M_writer(filters.decode.utf8(_("Start a new discussion:")))
            __M_writer(u'</h4>\n            <ul class="discussion-errors"></ul>\n            <div class="reply-body" data-id="')
            # SOURCE LINE 19
            __M_writer(filters.decode.utf8('<%- id %>'))
            __M_writer(u'"></div>\n            <div class="reply-post-control">\n                <a class="discussion-submit-post control-button" href="#">')
            # SOURCE LINE 21
            __M_writer(filters.decode.utf8(_("Submit")))
            __M_writer(u'</a>\n            </div>\n        </form>\n')
        # SOURCE LINE 25
        __M_writer(u'        -->\n    </article>\n</script>\n\n<script type="text/template" id="thread-show-template">\n  <div class="discussion-post">\n      <div><a href="javascript:void(0)" class="dogear action-follow" data-tooltip="follow"></a></div>\n      <header>\n      ')
        # SOURCE LINE 33
        __M_writer(filters.decode.utf8("<% if (obj.group_id) { %>"))
        __M_writer(u'\n      <div class="group-visibility-label">')
        # SOURCE LINE 34
        __M_writer(filters.decode.utf8("<%- obj.group_string%>"))
        __M_writer(u'</div>\n              ')
        # SOURCE LINE 35
        __M_writer(filters.decode.utf8("<% }  %>"))
        __M_writer(u'      \n      \n          <a href="#" class="vote-btn discussion-vote discussion-vote-up" data-role="discussion-vote" data-tooltip="vote">\n          <span class="plus-icon">+</span> <span class=\'votes-count-number\'>')
        # SOURCE LINE 38
        __M_writer(filters.decode.utf8('<%- votes["up_count"] %>'))
        __M_writer(u'</span></a>\n          <h1>')
        # SOURCE LINE 39
        __M_writer(filters.decode.utf8('<%- title %>'))
        __M_writer(u'</h1>\n          <p class="posted-details">\n              ')
        # SOURCE LINE 41
        __M_writer(filters.decode.utf8("<% if (obj.username) { %>"))
        __M_writer(u'\n              <a href="')
        # SOURCE LINE 42
        __M_writer(filters.decode.utf8('<%- user_url %>'))
        __M_writer(u'" class="username">')
        __M_writer(filters.decode.utf8('<%- username %>'))
        __M_writer(u'</a>\n              ')
        # SOURCE LINE 43
        __M_writer(filters.decode.utf8("<% } else {print('anonymous');} %>"))
        __M_writer(u'\n              <span class="timeago" title="')
        # SOURCE LINE 44
        __M_writer(filters.decode.utf8('<%- created_at %>'))
        __M_writer(u'">')
        __M_writer(filters.decode.utf8('<%- created_at %>'))
        __M_writer(u'</span>\n\n              <span class="post-status-closed top-post-status" style="display: none">\n                ')
        # SOURCE LINE 47
        __M_writer(filters.decode.utf8(_("&bull; This thread is closed.")))
        __M_writer(u'\n              </span>\n          </p>\n      </header>\n\n      <div class="post-body">')
        # SOURCE LINE 52
        __M_writer(filters.decode.utf8('<%- body %>'))
        __M_writer(u'</div>\n      <div class="discussion-flag-abuse notflagged" data-role="thread-flag" data-tooltip="Report Misuse">\n      <i class="icon icon-flag"></i><span class="flag-label">')
        # SOURCE LINE 54
        __M_writer(filters.decode.utf8(_("Report Misuse")))
        __M_writer(u'</span></div>\n        \n        \n')
        # SOURCE LINE 57
        if course and has_permission(user, 'openclose_thread', course.id):
            # SOURCE LINE 58
            __M_writer(u'      <div class="admin-pin discussion-pin notpinned" data-role="thread-pin" data-tooltip="pin this thread">\n      <i class="icon icon-pushpin"></i><span class="pin-label">')
            # SOURCE LINE 59
            __M_writer(filters.decode.utf8(_("Pin Thread")))
            __M_writer(u'</span></div>\n\n')
            # SOURCE LINE 61
        else:
            # SOURCE LINE 62
            __M_writer(u'      ')
            __M_writer(filters.decode.utf8("<% if (pinned) { %>"))
            __M_writer(u'\n      <div class="discussion-pin notpinned" data-role="thread-pin" data-tooltip="pin this thread">\n      <i class="icon icon-pushpin"></i><span class="pin-label">')
            # SOURCE LINE 64
            __M_writer(filters.decode.utf8(_("Pin Thread")))
            __M_writer(u'</span></div>\n      ')
            # SOURCE LINE 65
            __M_writer(filters.decode.utf8("<% }  %>"))
            __M_writer(u'  \n')
        # SOURCE LINE 67
        __M_writer(u'      \n      \n      ')
        # SOURCE LINE 69
        __M_writer(filters.decode.utf8('<% if (obj.courseware_url) { %>'))
        __M_writer(u'\n      <div class="post-context">\n          (this topic is about <a href="')
        # SOURCE LINE 71
        __M_writer(filters.decode.utf8('<%- courseware_url%>'))
        __M_writer(u'">')
        __M_writer(filters.decode.utf8('<%- courseware_title %>'))
        __M_writer(u' Welcome to Pepper</a>)\n      </div>\n      ')
        # SOURCE LINE 73
        __M_writer(filters.decode.utf8('<% } %>'))
        __M_writer(u'\n\n      <ul class="moderator-actions">\n          <li style="display: none"><a class="action-edit" href="javascript:void(0)"><span class="edit-icon"></span> ')
        # SOURCE LINE 76
        __M_writer(filters.decode.utf8(_("Edit")))
        __M_writer(u'</a></li>\n          <li style="display: none"><a class="action-delete" href="javascript:void(0)"><span class="delete-icon"></span> ')
        # SOURCE LINE 77
        __M_writer(filters.decode.utf8(_("Delete")))
        __M_writer(u'</a></li>\n          <li style="display: none"><a class="action-openclose" href="javascript:void(0)"><span class="edit-icon"></span> ')
        # SOURCE LINE 78
        __M_writer(filters.decode.utf8(_("Close")))
        __M_writer(u'</a></li>\n      </ul>\n  </div>\n</script>\n\n<script type="text/template" id="thread-edit-template">\n  <div class="discussion-post edit-post-form">\n    <h1>')
        # SOURCE LINE 85
        __M_writer(filters.decode.utf8(_("Editing topic")))
        __M_writer(u'</h1>\n    <ul class="edit-post-form-errors"></ul>\n    <div class="form-row">\n      <input type="text" class="edit-post-title" name="title" value="')
        # SOURCE LINE 88
        __M_writer(filters.decode.utf8("<%-title %>"))
        __M_writer(u'" placeholder="Title">\n    </div>\n    <div class="form-row">\n      <div class="edit-post-body" name="body">')
        # SOURCE LINE 91
        __M_writer(filters.decode.utf8("<%- body %>"))
        __M_writer(u'</div>\n    </div>\n')
        # SOURCE LINE 98
        __M_writer(u'    <input type="submit" class="post-update" value="')
        __M_writer(filters.decode.utf8(_("Update topic")))
        __M_writer(u'">\n    <a href="#" class="post-cancel">')
        # SOURCE LINE 99
        __M_writer(filters.decode.utf8(_("Cancel")))
        __M_writer(u'</a>\n  </div>\n</script>\n\n<script type="text/template" id="thread-response-template">\n    <div class="discussion-response"></div>\n    <ol class="comments">\n        <li class="new-comment response-local">\n            <form class="comment-form" data-id="')
        # SOURCE LINE 107
        __M_writer(filters.decode.utf8('<%- wmdId %>'))
        __M_writer(u'">\n                <ul class="discussion-errors"></ul>\n                <div class="comment-body" data-id="')
        # SOURCE LINE 109
        __M_writer(filters.decode.utf8('<%- wmdId %>'))
        __M_writer(u'"\n                data-placeholder="Add a comment..."></div>\n                <div class="comment-post-control">\n                    <a class="discussion-submit-comment control-button" href="#">')
        # SOURCE LINE 112
        __M_writer(filters.decode.utf8(_("Submit")))
        __M_writer(u'</a>\n                </div>\n            </form>\n        \n        </li>\n    </ol>\n</script>\n\n<script type="text/template" id="thread-response-show-template">\n    <header class="response-local">\n        <a href="javascript:void(0)" class="vote-btn" data-tooltip="vote"><span class="plus-icon"></span><span class="votes-count-number">')
        # SOURCE LINE 122
        __M_writer(filters.decode.utf8("<%- votes['up_count'] %>"))
        __M_writer(u'</span></a>\n        <a href="javascript:void(0)" class="endorse-btn')
        # SOURCE LINE 123
        __M_writer(filters.decode.utf8('<% if (endorsed) { %> is-endorsed<% } %>'))
        __M_writer(u' action-endorse" style="cursor: default; display: none;" data-tooltip="endorse"><span class="check-icon" style="pointer-events: none; "></span></a>\n        ')
        # SOURCE LINE 124
        __M_writer(filters.decode.utf8("<% if (obj.username) { %>"))
        __M_writer(u'\n        <a href="')
        # SOURCE LINE 125
        __M_writer(filters.decode.utf8('<%- user_url %>'))
        __M_writer(u'" class="posted-by" posted_by_id="')
        __M_writer(filters.decode.utf8('<%- user_id %>'))
        __M_writer(u'">')
        __M_writer(filters.decode.utf8('<%- username %>'))
        __M_writer(u'</a>\n        ')
        # SOURCE LINE 126
        __M_writer(filters.decode.utf8("<% } else {print('<span class=\"anonymous\"><em>anonymous</em></span>');} %>"))
        __M_writer(u'\n        <p class="posted-details" title="')
        # SOURCE LINE 127
        __M_writer(filters.decode.utf8('<%- created_at %>'))
        __M_writer(u'">')
        __M_writer(filters.decode.utf8('<%- created_at %>'))
        __M_writer(u'</p>\n    </header>\n    <div class="response-local"><div class="response-body">')
        # SOURCE LINE 129
        __M_writer(filters.decode.utf8("<%- body %>"))
        __M_writer(u'</div>\n    <div class="discussion-flag-abuse notflagged" data-role="thread-flag" data-tooltip="report misuse">                \n      <i class="icon icon-flag"></i><span class="flag-label">Report Misuse</span></div>\n    </div>\n    <ul class="moderator-actions response-local">\n        <li style="display: none"><a class="action-edit" href="javascript:void(0)"><span class="edit-icon"></span> ')
        # SOURCE LINE 134
        __M_writer(filters.decode.utf8(_("Edit")))
        __M_writer(u'</a></li>\n        <li style="display: none"><a class="action-delete" href="javascript:void(0)"><span class="delete-icon"></span> ')
        # SOURCE LINE 135
        __M_writer(filters.decode.utf8(_("Delete")))
        __M_writer(u'</a></li>\n        <li style="display: none"><a class="action-openclose" href="javascript:void(0)"><span class="edit-icon"></span> ')
        # SOURCE LINE 136
        __M_writer(filters.decode.utf8(_("Close")))
        __M_writer(u'</a></li>\n    </ul>\n</script>\n\n<script type="text/template" id="thread-response-edit-template">\n  <div class="edit-post-form">\n    <h1>')
        # SOURCE LINE 142
        __M_writer(filters.decode.utf8(_("Editing response")))
        __M_writer(u'</h1>\n    <ul class="edit-post-form-errors"></ul>\n    <div class="form-row">\n      <div class="edit-post-body" name="body">')
        # SOURCE LINE 145
        __M_writer(filters.decode.utf8("<%- body %>"))
        __M_writer(u'</div>\n    </div>\n    <input type="submit" class="post-update" value="')
        # SOURCE LINE 147
        __M_writer(filters.decode.utf8(_("Update response")))
        __M_writer(u'">\n    <a href="#" class="post-cancel">')
        # SOURCE LINE 148
        __M_writer(filters.decode.utf8(_("Cancel")))
        __M_writer(u'</a>\n  </div>\n</script>\n\n<script type="text/template" id="response-comment-show-template">\n  <a id="a')
        # SOURCE LINE 153
        __M_writer(filters.decode.utf8('<%- id %>'))
        __M_writer(u'"></a>\n  <div id="comment_')
        # SOURCE LINE 154
        __M_writer(filters.decode.utf8('<%- id %>'))
        __M_writer(u'">\n    <div class="response-body">')
        # SOURCE LINE 155
        __M_writer(filters.decode.utf8('<%- body %>'))
        __M_writer(u'</div>\n    <div class="discussion-flag-abuse notflagged" data-role="thread-flag" data-tooltip="Report Misuse">                \n      <i class="icon icon-flag"></i><span class="flag-label"></span></div> \n    <p class="posted-details">&ndash;posted <span class="timeago" title="')
        # SOURCE LINE 158
        __M_writer(filters.decode.utf8('<%- created_at %>'))
        __M_writer(u'">')
        __M_writer(filters.decode.utf8('<%- created_at %>'))
        __M_writer(u'</span> by\n        ')
        # SOURCE LINE 159
        __M_writer(filters.decode.utf8("<% if (obj.username) { %>"))
        __M_writer(u'\n        <a href="')
        # SOURCE LINE 160
        __M_writer(filters.decode.utf8('<%- user_url %>'))
        __M_writer(u'" class="profile-link">')
        __M_writer(filters.decode.utf8('<%- username %>'))
        __M_writer(u'</a>\n        ')
        # SOURCE LINE 161
        __M_writer(filters.decode.utf8("<% } else {print('anonymous');} %>"))
        __M_writer(u'\n    </p>\n    <div class="discussion-response')
        # SOURCE LINE 163
        __M_writer(filters.decode.utf8('<%- id %>'))
        __M_writer(u'"></div>\n    <div style="padding-left:20px;">\n     <ul class="moderator-actions response-local">\n          <li style="display: none"><a class="action-edit" href="javascript:void(0)"><span class="edit-icon"></span> ')
        # SOURCE LINE 166
        __M_writer(filters.decode.utf8(_("Edit")))
        __M_writer(u'</a></li>\n          <li style="display: none"><a class="action-delete" href="javascript:void(0)"><span class="delete-icon"></span> ')
        # SOURCE LINE 167
        __M_writer(filters.decode.utf8(_("Delete")))
        __M_writer(u'</a></li>\n          <!--<li style="display: none"><a class="action-openclose" href="javascript:void(0)"><span class="edit-icon"></span> ')
        # SOURCE LINE 168
        __M_writer(filters.decode.utf8(_("Close")))
        __M_writer(u'</a></li>\n          -->\n      </ul>\n     </div>\n  </div>\n</script>\n\n<script type="text/template" id="thread-list-item-template">\n    <a href="')
        # SOURCE LINE 176
        __M_writer(filters.decode.utf8('<%- id %>'))
        __M_writer(u'" data-id="')
        __M_writer(filters.decode.utf8('<%- id %>'))
        __M_writer(u'">\n        <span class="title">')
        # SOURCE LINE 177
        __M_writer(filters.decode.utf8("<%- title %>"))
        __M_writer(u'</span>\n        ')
        # SOURCE LINE 178
        __M_writer(filters.decode.utf8("<% if (unread_comments_count > 0) { %>"))
        __M_writer(u'\n            <span class="comments-count unread" data-tooltip="')
        # SOURCE LINE 179
        __M_writer(filters.decode.utf8("<%- unread_comments_count %>"))
        __M_writer(u' new comment')
        __M_writer(filters.decode.utf8("<%- unread_comments_count > 1 ? 's' : '' %>"))
        __M_writer(u'">')
        __M_writer(filters.decode.utf8("<%- comments_count %>"))
        __M_writer(u'</span>\n        ')
        # SOURCE LINE 180
        __M_writer(filters.decode.utf8("<% } else { %>"))
        __M_writer(u'\n            <span class="comments-count">')
        # SOURCE LINE 181
        __M_writer(filters.decode.utf8("<%- comments_count %>"))
        __M_writer(u'</span>\n        ')
        # SOURCE LINE 182
        __M_writer(filters.decode.utf8("<% } %>"))
        __M_writer(u'\n        <span class="votes-count">+')
        # SOURCE LINE 183
        __M_writer(filters.decode.utf8("<%- votes['up_count'] %>"))
        __M_writer(u'</span>\n    </a>\n</script>\n<script type="text/template" id="discussion-home">\n  <style>\n    [class^="icon-"], [class*=" icon-"] {font-family: "FontAwesome" !important;}\n  </style>\n  <div class="discussion-article blank-slate">\n  <section class="home-header">\n  <span class="label">DISCUSSION HOME:</span>\n')
        # SOURCE LINE 193
        if course and course.display_name_with_default:
            # SOURCE LINE 194
            __M_writer(u'  <h1 class="home-title">')
            __M_writer(filters.decode.utf8(course.display_name_with_default))
            __M_writer(u'</h1>\n  </section>\n  \n')
            # SOURCE LINE 197
            if settings.MITX_FEATURES.get('ENABLE_DISCUSSION_HOME_PANEL'):
                # SOURCE LINE 198
                __M_writer(u'  <span class="label label-settings">HOW TO USE PEPPER DISCUSSIONS</span>\n  <table class="home-helpgrid">\n  <tr class="helpgrid-row helpgrid-row-navigation">\n  <td class="row-title">Find discussions</td>\n  <td class="row-item">\n  <i class="icon icon-reorder"></i>\n  <span class="row-description">Focus in on specific topics</span>\n  </td>\n  <td class="row-item">\n  <i class="icon icon-search"></i>\n  <span class="row-description">Search for specific topics </span>\n  </td>\n  <td class="row-item">\n  <i class="icon icon-sort"></i>\n  <span class="row-description">Sort by date, vote, or comments </span>\n  </td>\n  </tr>\n  <tr class="helpgrid-row helpgrid-row-participation">\n  <td class="row-title">Engage with topics</td>\n  <td class="row-item">\n  <i class="icon icon-plus"></i>\n  <span class="row-description">Upvote topics and good responses</span>\n  </td>\n  <td class="row-item">\n  <i class="icon icon-flag"></i>\n  <span class="row-description">Report Forum Misuse</span>\n  </td>\n  <td class="row-item">\n  <i class="icon icon-star"></i>\n  <span class="row-description">Follow topics for updates</span>\n  </td>\n  </tr>\n  <!--\n  <tr class="helpgrid-row helpgrid-row-notification">\n  <td class="row-title">Receive updates</td>\n  <td class="row-item-full" colspan="3">\n  <input type="checkbox" class="email-setting" name="email-notification"></input>\n  <i class="icon icon-envelope"></i>\n  <span class="row-description"> If enabled, you will receive an email digest once a day notifying you about new, unread activity from posts you are following. </span>\n  </td>\n  </tr>\n  -->\n  </table>\n  <!--20151124 add new information-->\n  <!--begin-->\n  </br>\n  <table class="home-helpgrid">\n  <tr>\n  <td style="background-color:#b0e0e6;">\n    <p style="padding:8px;">Let\'s use the discussion forum to coach and collaborate with your fellow Pepper</br>educators. <b>If you have a support issue, please contact us at </b><a href="mailto:peppersupport@pcgus.com" style="font-color:#1ea9dc;">PepperSupport@pcgus.com</a>. Support-related items will be removed from the board.</p>\n  </td>\n  </tr>\n  </table>\n  <!--end-->\n')
        # SOURCE LINE 254
        __M_writer(u'\n  </div>    \n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


