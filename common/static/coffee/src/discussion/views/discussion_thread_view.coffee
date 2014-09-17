if Backbone?
  class @DiscussionThreadView extends DiscussionContentView

    events:
      "click .discussion-submit-post": "submitComment"

      # TODO tags
      # Until we decide what to do w/ tags, removing them.
      #"click .thread-tag": "tagSelected"

    $: (selector) ->
      @$el.find(selector)

    initialize: ->
      super()
      @createShowView()

    renderTemplate: ->
      @template = _.template($("#thread-template").html())
      @template(@model.toJSON())

    render: ->
      @$el.html(@renderTemplate())
      @$el.find(".loading").hide()
      @delegateEvents()

      @renderShowView()
      @renderAttrs()

      # TODO tags
      # Until we decide what to do w/ tags, removing them.
      #@renderTags()

      @$("span.timeago").timeago()
      @makeWmdEditor "reply-body"
      @renderResponses()
      @

    cleanup: ->
      if @responsesRequest?
        @responsesRequest.abort()

    # TODO tags
    # Until we decide what to do w/ tags, removing them.
    #renderTags: ->
    #  # tags
    #  for tag in @model.get("tags")
    #    if !tags
    #      tags = $('<div class="thread-tags">')
    #    tags.append("<a href='#' class='thread-tag'>#{tag}</a>")
    #  @$(".post-body").after(tags)

    # TODO tags
    # Until we decide what to do w tags, removing them.
    #tagSelected: (e) ->
    #  @trigger "tag:selected", $(e.target).html()

    renderResponses: ->
      setTimeout(=>
        @$el.find(".loading").show()
      , 200)
      @responsesRequest = DiscussionUtil.safeAjax
        url: DiscussionUtil.urlFor('retrieve_single_thread', @model.get('commentable_id'), @model.id)
        success: (data, textStatus, xhr) =>
          @responsesRequest = null
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
        $(view.el).prepend('<a id="a'+response.get('id')+'"></a>')
        view.afterInsert()

    addComment: =>
      @model.comment()

    endorseThread: (endorsed) =>
      is_endorsed = @$el.find(".is-endorsed").length
      @model.set 'endorsed', is_endorsed

    submitComment: (event) ->
      event.preventDefault()
      url = @model.urlFor('reply')
      body = @getWmdContent("reply-body")
      return if not body.trim().length
      @setWmdContent("reply-body", "")
      comment = new Comment(body: body, created_at: (new Date()).toISOString(), username: window.user.get("username"), votes: { up_count: 0 }, abuse_flaggers:[], endorsed: false, user_id: window.user.get("id"))
      comment.set('thread', @model.get('thread'))
      @renderResponse(comment)
      @model.addComment()
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
          if This.model.get('thread').get('user_id')!=window.user.get("id") and This.interviewerIsEnable()
            if This.getCommentType()=='discussion'
              location = ('/courses/'+This.model.get('thread').get('course_id')+"/discussion/forum/"+This.model.get('thread').get('commentable_id')+"/threads/"+This.model.get('thread').get('id')).split("#")[0]+"#"+comment.get('id');
            else
              location = ('/courses/'+window.location.href.split('/courses/')[1]).split("#")[0]+"#"+comment.get('id');
            DiscussionUtil.safeAjax
                type: 'POST'
                url: '/interactive_update/save_info'
                data: {'info':JSON.stringify({'user_id':This.model.get('thread').get('user_id'),'interviewer_id':window.user.get("id"),'interviewer_name':window.user.get("username"),'type':This.getCommentType(),'location':location,'course_number':$('title').attr('course_number'),'date':data.content.created_at,'activate':'false'})}
                async:false

    edit: (event) =>
      @createEditView()
      @renderEditView()

    update: (event) =>

      newTitle = @editView.$(".edit-post-title").val()
      newBody  = @editView.$(".edit-post-body textarea").val()

      # TODO tags
      # Until we decide what to do w/ tags, removing them.
      #newTags  = @editView.$(".edit-post-tags").val()

      url = DiscussionUtil.urlFor('update_thread', @model.id)

      DiscussionUtil.safeAjax
          $elem: $(event.target)
          $loading: $(event.target) if event
          url: url
          type: "POST"
          dataType: 'json'
          async: false # TODO when the rest of the stuff below is made to work properly..
          data:
              title: newTitle
              body: newBody

              # TODO tags
              # Until we decide what to do w/ tags, removing them.
              #tags: newTags

          error: DiscussionUtil.formErrorHandler(@$(".edit-post-form-errors"))
          success: (response, textStatus) =>
              # TODO: Move this out of the callback, this makes it feel sluggish
              @editView.$(".edit-post-title").val("").attr("prev-text", "")
              @editView.$(".edit-post-body textarea").val("").attr("prev-text", "")
              @editView.$(".edit-post-tags").val("")
              @editView.$(".edit-post-tags").importTags("")
              @editView.$(".wmd-preview p").html("")
              @model.set
                title: newTitle
                body: newBody
                tags: response.content.tags
              @createShowView()
              @renderShowView()

              # TODO tags
              # Until we decide what to do w/ tags, removing them.
              #@renderTags()

    createEditView: () ->

      if @showView?
        @showView.undelegateEvents()
        @showView.$el.empty()
        @showView = null

      @editView = new DiscussionThreadEditView(model: @model)
      @editView.bind "thread:update", @update
      @editView.bind "thread:cancel_edit", @cancelEdit

    renderSubView: (view) ->
      view.setElement(@$('.thread-content-wrapper'))
      view.render()
      view.delegateEvents()

    renderEditView: () ->
      @renderSubView(@editView)

    createShowView: () ->

      if @editView?
        @editView.undelegateEvents()
        @editView.$el.empty()
        @editView = null

      @showView = new DiscussionThreadShowView(model: @model)
      @showView.bind "thread:_delete", @_delete
      @showView.bind "thread:edit", @edit

    renderShowView: () ->
      @renderSubView(@showView)

    cancelEdit: (event) =>
      event.preventDefault()
      @createShowView()
      @renderShowView()

    # If you use "delete" here, it will compile down into JS that includes the
    # use of DiscussionThreadView.prototype.delete, and that will break IE8
    # because "delete" is a keyword. So, using an underscore to prevent that.
    _delete: (event) =>
      deletet_thread = $(".list-item").find(".active")
      deletet_thread_id=deletet_thread.parent().attr('data-id')
      next_thread_id = deletet_thread.parent().next().find('a').attr('data-id')
      prev_thread_id = deletet_thread.parent().prev().find('a').attr('data-id')
      
      url = @model.urlFor('_delete')
      if not @model.can('can_delete')
        return
      if not confirm "Are you sure to delete thread \"#{@model.get('title')}\"?"
        return
      
      @model.remove()
      @showView.undelegateEvents()
      @undelegateEvents()
      @$el.empty()
      $elem = $(event.target)
      
      DiscussionUtil.safeAjax
        $elem: $elem
        url: url
        type: "POST"
        success: (response, textStatus) =>
          if next_thread_id!=undefined
            $(".post-list a[data-id='#{next_thread_id}']").click()
          else if prev_thread_id!=undefined
            $(".post-list a[data-id='#{prev_thread_id}']").click()
          else
            indexPage=window.location.href.split('forum/')
            url=indexPage[0]+"forum"
            @template = _.template($("#discussion-home").html())
            $(".discussion-column").html(@template)
            #top.window.location=url
            #$(".course-tabs").find(".active").get(0).click()

    getCommentType:()->
      if $('body').find('.my-course-work-content').length>0
        return 'portfolio'
      else
        return 'discussion'
    interviewerIsEnable:()->
      if $('body').find('.about-me-content').length<1
        return true
      else
        return false