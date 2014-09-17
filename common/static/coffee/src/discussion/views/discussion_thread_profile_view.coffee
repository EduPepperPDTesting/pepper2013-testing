if Backbone?
  class @DiscussionThreadProfileView extends DiscussionContentView
    expanded = false
    events:
      "click .discussion-vote": "toggleVote"
      "click .action-follow": "toggleFollowing"
      "click .expand-post": "expandPost"
      "click .collapse-post": "collapsePost"
      "click .discussion-submit-comment": "submitComment"
      "click .discussion-submit-post": "submitThread"
      "click .action-edit": "edit"
      "click .action-delete": "_delete"
      "click .action-openclose": "toggleClosed"

    initLocal: ->
      @$local = @$el.children(".discussion-article").children(".local")
      @$delegateElement = @$local

    initialize: ->
      super()
      @model.on "change", @updateModelDetails

    render: ->
      @template = DiscussionUtil.getTemplate("_profile_thread")
      if not @model.has('abbreviatedBody')
        @abbreviateBody()
      params = $.extend(@model.toJSON(),{expanded: @expanded, permalink: @model.urlFor('retrieve')})
      if not @model.get('anonymous')
        params = $.extend(params, user:{username: @model.username, user_url: @model.user_url})
      @$el.html(Mustache.render(@template, params))
      @initLocal()
      @delegateEvents()
      @renderDogear()
      @renderVoted()
      @renderAttrs()
      if @model.get('courseware_url')
        if $('#btn-logged-user').length>0
          course_url="<span style='padding-left:20px;'>(this topic is about <a href='"+@model.get('courseware_url')+"'>"+@model.get('courseware_title')+" Welcome to Pepper</a>)</span>"
        else
          course_url="<span style='padding-left:20px;'>(this topic is about <span style='color:#366094;'>"+@model.get('courseware_title')+" Welcome to Pepper</span>)</span>"
        @$el.find('.post-context').html(course_url)
      @$("span.timeago").timeago()
      if $(".my-discussion-content").length>0
        @$el.find('.username').attr('href','javascript:void(0);')
        @$el.find('.username').css('cursor','default')
        @$el.find('.username').css('color','#366094')
      @$el.find('.action-edit').hide()
      @$el.find('.action-delete').hide()
      @$el.find('.action-openclose').hide()
      @convertMath()
      #@$(".post-body").html(@$(".post-body").text())
      if @expanded
        @makeWmdEditor "reply-body"
        @renderResponses()
      if window.location.hash!=""
        @expandPost(null)
      @

    renderDogear: ->
      if window.user.following(@model)
        @$(".dogear").addClass("is-followed")

    renderVoted: =>
      if window.user.voted(@model)
        @$("[data-role=discussion-vote]").addClass("is-cast")
      else
        @$("[data-role=discussion-vote]").removeClass("is-cast")

    updateModelDetails: =>
      @renderVoted()
      @$("[data-role=discussion-vote] .votes-count-number").html(@model.get("votes")["up_count"])

    convertMath: ->
      element = @$(".post-body")
      element.html(element.text())
      element.html DiscussionUtil.postMathJaxProcessor DiscussionUtil.markdownWithHighlight element.text()
      #MathJax.Hub.Queue ["Typeset", MathJax.Hub, element[0]]

    renderResponses: ->
      DiscussionUtil.safeAjax
        url: "/courses/#{$$course_id}/discussion/forum/#{@model.get('commentable_id')}/threads/#{@model.id}"
        #$loading: @$el
        success: (data, textStatus, xhr) =>
          @$el.find(".loading").remove()
          Content.loadContentInfos(data['annotated_content_info'])
          comments = new Comments(data['content']['children'])
          comments.each @renderResponse
          @trigger "thread:responses:rendered"
          if window.location.hash!=""
            hash = window.location.hash.replace("#","")
            id="#a"+hash
            if $(id).length>0
              $(window).scrollTop($(id).offset().top-70)

    renderResponse: (response) =>
      response.set('thread', @model)
      view = new ThreadResponseView(model: response)
      view.on "comment:add", @addComment
      view.on "comment:endorse", @endorseThread
      view.render()
      @$el.find(".responses").append(view.el)
      view.afterInsert()

    addComment: =>
      @model.comment()

    toggleVote: (event) ->
      event.preventDefault()
      if window.user.voted(@model)
        @unvote()
      else
        @vote()

    toggleFollowing: (event) ->
      $elem = $(event.target)
      url = null
      if not @model.get('subscribed')
        @model.follow()
        url = @model.urlFor("follow")
      else
        @model.unfollow()
        url = @model.urlFor("unfollow")
      DiscussionUtil.safeAjax
        $elem: $elem
        url: url
        type: "POST"

    vote: ->
      window.user.vote(@model)
      url = @model.urlFor("upvote")
      DiscussionUtil.safeAjax
        $elem: @$(".discussion-vote")
        url: url
        type: "POST"
        success: (response, textStatus) =>
          if textStatus == 'success'
            @model.set(response)

    unvote: ->
      window.user.unvote(@model)
      url = @model.urlFor("unvote")
      DiscussionUtil.safeAjax
        $elem: @$(".discussion-vote")
        url: url
        type: "POST"
        success: (response, textStatus) =>
          if textStatus == 'success'
            @model.set(response)

    edit: ->

    abbreviateBody: ->
      abbreviated = DiscussionUtil.abbreviateString @model.get('body'), 140
      @model.set('abbreviatedBody', abbreviated)

    expandPost: (event) ->
      @expanded = true
      @$el.addClass('expanded')
      @$el.find('.post-body').html(@model.get('body'))
      @convertMath()
      @$el.find('.expand-post').css('display', 'none')
      @$el.find('.collapse-post').css('display', 'block')
      @$el.find('.post-extended-content').show()
      @$el.find('.action-edit').hide()
      @$el.find('.action-delete').hide()
      @$el.find('.action-openclose').hide()
      @makeWmdEditor "reply-body"
      @renderAttrs()
      if @$el.find('.loading').length
        @renderResponses()

    collapsePost: (event) ->
      @expanded = false
      @$el.removeClass('expanded')
      @$el.find('.post-body').html(@model.get('abbreviatedBody'))
      @convertMath()
      @$el.find('.collapse-post').css('display', 'none')
      @$el.find('.post-extended-content').hide()
      @$el.find('.action-edit').hide()
      @$el.find('.action-delete').hide()
      @$el.find('.action-openclose').hide()
      @$el.find('.expand-post').css('display', 'block')

    submitComment: (event) ->
      event.preventDefault()
      url = @model.urlFor('reply')
      body = @getWmdContent("comment-body")
      return if not body.trim().length
      @setWmdContent("comment-body", "")
      comment = new Comment(body: body, created_at: (new Date()).toISOString(), username: window.user.get("username"), abuse_flaggers:[], user_id: window.user.get("id"), id:"unsaved")
      view = @renderComment(comment)
      @hideEditorChrome()
      @trigger "comment:add", comment

      DiscussionUtil.safeAjax
        $elem: $(event.target)
        url: url
        type: "POST"
        dataType: 'json'
        data:
          body: body
        success: (response, textStatus) ->
          comment.set(response.content)
          view.render() # This is just to update the id for the most part, but might be useful in general

    submitThread: (event) ->
      event.preventDefault()
      url = @model.urlFor('reply')
      body = @getWmdContent("reply-body")
      return if not body.trim().length
      @setWmdContent("reply-body", "")
      comment = new Comment(body: body, created_at: (new Date()).toISOString(), username: window.user.get("username"), votes: { up_count: 0 }, abuse_flaggers:[], endorsed: false, user_id: window.user.get("id"))
      comment.set('thread', @model.get('thread'))
      @renderResponse(comment)
      @model.addComment()
      @.$el.find(".responses").empty()
      @.renderResponses()
      This = @
      DiscussionUtil.safeAjax
        $elem: $(event.target)
        url: url
        type: "POST"
        dataType: 'json'
        data:
          body: body
        success: (data, textStatus) =>
          comment.updateInfo(data.annotated_content_info)
          comment.set(data.content)
          user_id=data.content.user_id
          user_name=data.content.username
          if This.model.get('thread').get('user_id')!=user_id
            if This.getCommentType()=='discussion'
              location = ('/courses/'+This.model.get('thread').get('course_id')+"/discussion/forum/"+This.model.get('thread').get('commentable_id')+"/threads/"+This.model.get('thread').get('id')).split("#")[0]+"#"+comment.get('id');
            else
              location = ('/courses/'+window.location.href.split('/courses/')[1]).split("#")[0]+"#"+comment.get('id');
            DiscussionUtil.safeAjax
                type: 'POST'
                url: '/interactive_update/save_info'
                data: {'info':JSON.stringify({'user_id':This.model.get('thread').get('user_id'),'interviewer_id':user_id,'interviewer_name':user_name,'type':This.getCommentType(),'location':location,'course_number':$('title').attr('course_number'),'date':(new Date()).toISOString(),'activate':'false','portfolio_username':$(".user_name").text()})}
                async:false
        
    toggleClosed: (event) ->
      $elem = $(event.target)
      url = @model.urlFor('close')
      closed = @model.get('closed')
      data = { closed: not closed }
      DiscussionUtil.safeAjax
        $elem: $elem
        url: url
        data: data
        type: "POST"
        success: (response, textStatus) =>
          @model.set('closed', not closed)
          @model.set('ability', response.ability)

    edit: (event) ->
      @trigger "thread:edit", event

    _delete: (event) ->
      @trigger "thread:_delete", event

    getCommentType:()->
      if $('body').find('.my-course-work-content').length>0
        return 'portfolio'
      else
        return 'discussion'
