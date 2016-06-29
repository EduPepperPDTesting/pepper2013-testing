if Backbone?
  class @ResponseCommentShowView extends DiscussionContentView

    events:
      "click .discussion-flag-abuse": "toggleFlagAbuse"
      "click .action-edit": "edit"
      "click .action-delete": "_delete"
      "click .action-rating": "actionRating" #201606
      "click .see-results": "seeResults" #201606

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
      @renderRating() #201606
      @

    #201606
    renderRating: ->
      ratingTemp = "0"
      url = DiscussionUtil.urlFor('get_rating', @model.id)
      DiscussionUtil.safeAjax
          url: url
          type: "POST"
          dataType: 'json'
          async: true
          data:
              option_type: 'get_rating'

          #error: console.log("fail!")
          success: (response, textStatus) =>
            if textStatus == 'success'
              ratingTemp = response.rating
              @$el.find('.action-rating').raty({
                    starOn:'star-on-orange.png',
                    starHalf:'star-half-orange.png',
                    hints: ['Poor', 'Fair', 'Average', 'Good', 'Great'],
                    path:"/static/js/vendor/raty/lib/img",
                    click: (score, evt) ->
                      $(@).attr('data-rating',score)
                    score: ->
                      ratingTemp
                  })

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

    edit: (event) =>
      @createEditView()
      @renderEditView()
      @hideCommentForm()

    #201606
    actionRating: (event) =>
      rating = @$el.find('.action-rating').attr("data-rating")
      url = DiscussionUtil.urlFor('set_rating', @model.id)
      DiscussionUtil.safeAjax
          url: url
          type: "POST"
          dataType: 'json'
          async: true
          data:
              rating: rating
              option_type: 'update_rating'

          error: console.log("fail!")
          success: (response, textStatus) =>
            if textStatus == 'success'
              @model.set('rating', response.rating)
      
    #201606
    seeResults: (event) =>
      url = DiscussionUtil.urlFor('get_rating', @model.id)
      DiscussionUtil.safeAjax
          url: url
          type: "POST"
          dataType: 'json'
          async: true
          data:
              option_type: 'get_avg_rating'

          #error: console.log("fail!")
          success: (response, textStatus) =>
            if textStatus == 'success'
              avg_ratingTemp = response.avg_rating
              $("#rate_results").find('.avg-rating').raty({
                  starOn:'star-on-blue.png',
                  starHalf:'star-half-blue.png',
                  hints: ['Poor', 'Fair', 'Average', 'Good', 'Great'],
                  path:"/static/js/vendor/raty/lib/img",
                  click: (score, evt) ->
                      $(@).attr('data-rating',score)
                  readOnly: true
                  score: ->
                      avg_ratingTemp
              })
              $("#rate_results").find('#hq_rate_num').html(response.avg_rating_count)
              $("#rate_results").show();
              $("#lean_overlay").show();
              $(window).scrollTop(0);

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
      @createShowView()
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
              @render()
              @showCommentForm()