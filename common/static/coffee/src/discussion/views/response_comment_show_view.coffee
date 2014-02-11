if Backbone?
  class @ResponseCommentShowView extends DiscussionContentView

    events:
      "click .discussion-flag-abuse": "toggleFlagAbuse"
      "click .action-edit": "edit"
      "click .action-delete": "_delete"

    tagName: "li"

    initialize: ->
        super()
        @model.on "change", @updateModelDetails

    render: ->
      @template = _.template($("#response-comment-show-template").html())
      params = @model.toJSON()

      @$el.html(@template(params))
      @initLocal()
      @delegateEvents()
      @renderAttrs()
      @renderFlagged()
      #@markAsStaff()
      @$el.find(".timeago").timeago()
      @$el.find('a.profile-link').attr('href','javascript:void(0);')
      @$el.find('a.profile-link').css('cursor','default')
      @$el.find('a.profile-link').css('color','#366094')
      @convertMath()
      @addReplyLink()
      @

    addReplyLink: () ->
      if @model.hasOwnProperty('parent')
        name = @model.parent.get('username') ? "anonymous"
        html = "<a href='#comment_#{@model.parent.id}'>@#{name}</a>:  "
        p = @$('.response-body p:first')
        p.prepend(html)

    convertMath: ->
      body = @$el.find(".response-body")
      body.html DiscussionUtil.postMathJaxProcessor DiscussionUtil.markdownWithHighlight body.text()
      MathJax.Hub.Queue ["Typeset", MathJax.Hub, body[0]]

    markAsStaff: ->
      if DiscussionUtil.isStaff(@model.get("user_id"))
        @$el.find("a.profile-link").after('<span class="staff-label">staff</span>')
      else if DiscussionUtil.isTA(@model.get("user_id"))
        @$el.find("a.profile-link").after('<span class="community-ta-label">Community&nbsp;&nbsp;TA</span>')


    renderFlagged: =>
      if window.user.id in @model.get("abuse_flaggers") or (DiscussionUtil.isFlagModerator and @model.get("abuse_flaggers").length > 0)
        @$("[data-role=thread-flag]").addClass("flagged")
        @$("[data-role=thread-flag]").removeClass("notflagged")
      else
        @$("[data-role=thread-flag]").removeClass("flagged")
        @$("[data-role=thread-flag]").addClass("notflagged")

    updateModelDetails: =>
      @renderFlagged()

    hideCommentForm: () ->
      @$('.comment-form').closest('li').hide()

    showCommentForm: () ->
      @$('.comment-form').closest('li').show()
      
    renderSubView: (view) ->
      view.setElement(@$('.discussion-response'+@model.id))
      view.render()
      view.delegateEvents()

    renderShowView: () ->
      @renderSubView(@showView)

    createShowView: () ->

      if @editView?
        @editView.undelegateEvents()
        @editView.$el.empty()
        @editView = null

      @showView = new ThreadResponseShowView(model: @model)
      @showView.bind "response:_delete", @_delete
      @showView.bind "response:edit", @edit

    edit: (event) =>
      @createEditView()
      @renderEditView()
      @hideCommentForm()

    _delete: (event) =>
      event.preventDefault()
      if not @model.can('can_delete')
        return
      if not confirm "Are you sure to delete this Comment? "
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

    renderEditView: () ->
      @renderSubView(@editView)

    cancelEdit: (event) =>
      event.preventDefault()
      @showCommentForm()

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
