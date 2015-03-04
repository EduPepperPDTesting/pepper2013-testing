if Backbone?
  class @ThreadResponseView extends DiscussionContentView
    commentList=[]
    tagName: "li"
    
    events:
        "click .discussion-submit-comment": "submitComment"
        "focus .wmd-input": "showEditorChrome"

    $: (selector) ->
      @$el.find(selector)

    initialize: ->
      @commentList=[]
      @createShowView()

    renderTemplate: ->
      @template = _.template($("#thread-response-template").html())

      templateData = @model.toJSON()
      templateData.wmdId = @model.id ? (new Date()).getTime()
      @template(templateData)

    render: ->
      @$el.html(@renderTemplate())
      @delegateEvents()

      @renderShowView()
      @renderAttrs()

      @renderComments()
      @

    afterInsert: ->
      @makeWmdEditor "comment-body"
      @hideEditorChrome()

    hideEditorChrome: ->
      @$('.wmd-button-row').hide()
      @$('.wmd-preview').hide()
      @$('.wmd-input').css({
        height: '35px',
        padding: '5px'
      })
      @$('.comment-post-control').hide()

    showEditorChrome: ->
      @$('.wmd-button-row').show()
      @$('.wmd-preview').show()
      @$('.comment-post-control').show()
      @$('.wmd-input').css({
        height: '125px',
        padding: '10px'
      })

    renderComments: ->
      comments = new Comments()
      comments.comparator = (comment) ->
        comment.get('created_at')
      collectComments = (comment) ->
        comments.add(comment)
        children = new Comments(comment.get('children'))
        children.each (child) ->
          child.parent = comment
          collectComments(child)
      @model.get('comments').each collectComments
      comments.each (comment) => @renderComment(comment, false, null)

    renderComment: (comment) =>
      @addCommentList(comment.get("user_id"))
      comment.set('thread', @model.get('thread'))
      view = new ResponseCommentView(model: comment)
      view.render()
      @$el.find(".comments .new-comment").before(view.el)
      if window.location.hash!=""
        hash = window.location.hash.replace("#","")
        id="#a"+hash
        if $(id).length>0
          $(window).scrollTop($(id).offset().top-70)
      view

    submitComment: (event) ->
      event.preventDefault()
      url = @model.urlFor('reply')
      body = @getWmdContent("comment-body")
      return if not body.trim().length
      @setWmdContent("comment-body", "")
      comment = new Comment(body: body,created_at: (new Date()).toISOString(), username: window.user.get("username"), abuse_flaggers:[], user_id: window.user.get("id"), id:"unsaved")
      view = @renderComment(comment)
      @hideEditorChrome()
      @trigger "comment:add", comment
      This = @
      DiscussionUtil.safeAjax
        $elem: $(event.target)
        url: url
        type: "POST"
        dataType: 'json'
        data:
          body: body
        success: (response, textStatus) ->
          comment.set(response.content)
          comment.set(response.annotated_content_info)
          view.render() # This is just to update the id for the most part, but might be useful in general
          #This.abilityRenderer(response.annotated_scontent_info.ability)
          user_id=This.$el.find('.posted-by').attr('posted_by_id')
          if This.getDiscussionType()=='course_discussion'
            interviewer_id=window.user.get("id")
            interviewer_name=window.user.get("username")
          else
            interviewer_id = response.content.user_id
            interviewer_name = response.content.username
          This.addCommentList(user_id)
          for v,i in This.commentList
            if (user_id==interviewer_id and user_id==v) or v==interviewer_id
              This.commentList.splice(i,1)
          if This.commentList.length>0 and This.interviewerIsEnable()
            if This.getCommentType()=='discussion'
              location = ('/courses/'+This.model.get('thread').get('course_id')+"/discussion/forum/"+This.model.get('thread').get('commentable_id')+"/threads/"+This.model.get('thread').get('id')).split("#")[0]+"#"+comment.get('id');
            else
              location = ('/courses/'+window.location.href.split('/courses/')[1]).split("#")[0]+"#"+comment.get('id');
            if This.commentList.length>1  
              dataInfo={'info':JSON.stringify({'user_id':This.commentList.toString(),'interviewer_id':interviewer_id,'interviewer_name':interviewer_name,'type':This.getCommentType(),'location':location,'course_number':$('title').attr('course_number'),'date':(new Date()).toISOString(),'activate':'false','multiple':'true','portfolio_username':$(".user_name").text()})}
            else
              dataInfo={'info':JSON.stringify({'user_id':This.commentList.toString(),'interviewer_id':interviewer_id,'interviewer_name':interviewer_name,'type':This.getCommentType(),'location':location,'course_number':$('title').attr('course_number'),'date':(new Date()).toISOString(),'activate':'false','portfolio_username':$(".user_name").text()})}
            DiscussionUtil.safeAjax
                type: 'POST'
                url: '/interactive_update/save_info'
                data: dataInfo
                async:false
    _delete: (event) =>
      event.preventDefault()
      if not @model.can('can_delete')
        return
      if not confirm "Are you sure to delete this response? "
        return
      url = @model.urlFor('_delete')
      @model.remove()
      @$el.remove()
      $elem = $(event.target)
      DiscussionUtil.safeAjax
        $elem: $elem
        url: url
        type: "POST"
        success: (response, textStatus) =>

    createEditView: () ->
      if @showView?
        @showView.undelegateEvents()
        @showView.$el.empty()
        @showView = null

      @editView = new ThreadResponseEditView(model: @model)
      @editView.bind "response:update", @update
      @editView.bind "response:cancel_edit", @cancelEdit

    renderSubView: (view) ->
      view.setElement(@$('.discussion-response'))
      view.render()
      view.delegateEvents()

    renderEditView: () ->
      @renderSubView(@editView)

    hideCommentForm: () ->
      @$('.comment-form').closest('li').hide()

    showCommentForm: () ->
      @$('.comment-form').closest('li').show()

    createShowView: () ->

      if @editView?
        @editView.undelegateEvents()
        @editView.$el.empty()
        @editView = null

      @showView = new ThreadResponseShowView(model: @model)
      @showView.bind "response:_delete", @_delete
      @showView.bind "response:edit", @edit

    renderShowView: () ->
      @renderSubView(@showView)

    cancelEdit: (event) =>
      event.preventDefault()
      @createShowView()
      @renderShowView()
      @showCommentForm()

    edit: (event) =>
      @createEditView()
      @renderEditView()
      @hideCommentForm()

    update: (event) =>

      newBody  = @editView.$(".edit-post-body textarea").val()

      url = DiscussionUtil.urlFor('update_comment', @model.id)

      DiscussionUtil.safeAjax
          $elem: $(event.target)
          $loading: $(event.target) if event
          url: url
          type: "POST"
          dataType: 'json'
          async: false # TODO when the rest of the stuff below is made to work properly..
          data:
              body: newBody
          error: DiscussionUtil.formErrorHandler(@$(".edit-post-form-errors"))
          success: (response, textStatus) =>
              # TODO: Move this out of the callback, this makes it feel sluggish
              @editView.$(".edit-post-body textarea").val("").attr("prev-text", "")
              @editView.$(".wmd-preview p").html("")

              @model.set
                body: newBody

              @createShowView()
              @renderShowView()
              @showCommentForm()

    abilityRenderer:(obj) ->
      if obj.can_delete
        @$(".action-delete").closest("li").show()
      else
        @$(".action-delete").closest("li").hide()

    getCommentType:()->
      if $('body').find('.my-course-work-content').length>0
        return 'portfolio'
      else
        return 'discussion'

    getDiscussionType:()->
      if $('body').find('.my-discussion-content').length>0
        return 'my_discussion'
      else
        return 'course_discussion'

    interviewerIsEnable:()->
      if $('body').find('.about-me-content').length<1
        return true
      else
        return false

    addCommentList:(cid)->
      if $.inArray(cid,@commentList)==-1
        @commentList.push(cid)