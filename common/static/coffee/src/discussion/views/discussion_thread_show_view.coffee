if Backbone?
  class @DiscussionThreadShowView extends DiscussionContentView

    events:
      "click .discussion-vote": "toggleVote"
      "click .discussion-flag-abuse": "toggleFlagAbuse"
      "click .admin-pin": "togglePin"
      "click .action-follow": "toggleFollowing"
      "click .action-edit": "edit"
      "click .action-delete": "_delete"
      "click .action-openclose": "toggleClosed"
      "click .action-rating": "actionRating" #201606
      "click .see-results": "seeResults" #201606

    $: (selector) ->
      @$el.find(selector)

    initialize: ->
      super()
      @model.on "change", @updateModelDetails

    renderTemplate: ->
      @template = _.template($("#thread-show-template").html())
      @template(@model.toJSON())

    render: ->
      @$el.html(@renderTemplate())
      @$(".discussion-post").find('h1').html(@model.get('title'))
      @$(".post-body").html(@model.get('body'))
      @$(".post-body").find('.file_url').remove()
      @delegateEvents()
      @renderDogear()
      @renderVoted()
      @renderFlagged()
      @renderPinned()
      @renderAttrs()
      @$("span.timeago").timeago()
      @convertMath()
      #@$(".post-body").html(@$(".post-body").text())
      @highlight @$(".post-body")
      @highlight @$("h1,h3")
      @$el.find('.username').attr('href','javascript:void(0);')
      @$el.find('.username').css('cursor','default')
      @$el.find('.username').css('color','#366094')
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
                      #$(@).attr('data-rating')
                      ratingTemp
                  })

    renderDogear: ->
      if window.user.following(@model)
        @$(".dogear").addClass("is-followed")

    renderVoted: =>
      if window.user.voted(@model)
        @$("[data-role=discussion-vote]").addClass("is-cast")
      else
        @$("[data-role=discussion-vote]").removeClass("is-cast")
        
    renderFlagged: =>
      if window.user.id in @model.get("abuse_flaggers") or (DiscussionUtil.isFlagModerator and @model.get("abuse_flaggers").length > 0)
        @$("[data-role=thread-flag]").addClass("flagged")  
        @$("[data-role=thread-flag]").removeClass("notflagged")
        @$(".discussion-flag-abuse .flag-label").html("Misuse Reported")
      else
        @$("[data-role=thread-flag]").removeClass("flagged")  
        @$("[data-role=thread-flag]").addClass("notflagged")      
        @$(".discussion-flag-abuse .flag-label").html("Report Misuse")

    renderPinned: =>
      if @model.get("pinned")
        @$("[data-role=thread-pin]").addClass("pinned")  
        @$("[data-role=thread-pin]").removeClass("notpinned")  
        @$(".discussion-pin .pin-label").html("Pinned")
      else
        @$("[data-role=thread-pin]").removeClass("pinned")  
        @$("[data-role=thread-pin]").addClass("notpinned")  
        @$(".discussion-pin .pin-label").html("Pin Thread")


    updateModelDetails: =>
      @renderVoted()
      @renderFlagged()
      @renderPinned()
      @$("[data-role=discussion-vote] .votes-count-number").html(@model.get("votes")["up_count"])

    convertMath: ->
      element = @$(".post-body")
      element.html(element.text())
      element.html DiscussionUtil.postMathJaxProcessor DiscussionUtil.markdownWithHighlight element.text()
      #MathJax.Hub.Queue ["Typeset", MathJax.Hub, element[0]]

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
            @model.set(response, {silent: true})


    unvote: ->
      window.user.unvote(@model)
      url = @model.urlFor("unvote")
      DiscussionUtil.safeAjax
        $elem: @$(".discussion-vote")
        url: url
        type: "POST"
        success: (response, textStatus) =>
          if textStatus == 'success'
            @model.set(response, {silent: true})


    edit: (event) ->
      @trigger "thread:edit", event

    #2016
    actionRating: (event) ->
      @trigger "thread:actionRating", event

    #2016
    seeResults: (event) ->
      @trigger "thread:seeResults", event

    _delete: (event) ->
      @trigger "thread:_delete", event

    togglePin: (event) ->
      event.preventDefault()
      if @model.get('pinned')
        @unPin()
      else
        @pin()
      
    pin: ->
      url = @model.urlFor("pinThread")
      DiscussionUtil.safeAjax
        $elem: @$(".discussion-pin")
        url: url
        type: "POST"
        success: (response, textStatus) =>
          if textStatus == 'success'
            @model.set('pinned', true)
        error: =>
          $('.admin-pin').text("Pinning not currently available")
       
    unPin: ->
      url = @model.urlFor("unPinThread")
      DiscussionUtil.safeAjax
        $elem: @$(".discussion-pin")
        url: url
        type: "POST"
        success: (response, textStatus) =>
          if textStatus == 'success'
            @model.set('pinned', false)


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

    toggleEndorse: (event) ->
      $elem = $(event.target)
      url = @model.urlFor('endorse')
      endorsed = @model.get('endorsed')
      data = { endorsed: not endorsed }
      DiscussionUtil.safeAjax
        $elem: $elem
        url: url
        data: data
        type: "POST"
        success: (response, textStatus) =>
          @model.set('endorsed', not endorsed)

    highlight: (el) ->
      if el.html()
        el.html(el.html().replace(/&lt;mark&gt;/g, "<mark>").replace(/&lt;\/mark&gt;/g, "</mark>"))

  class @DiscussionThreadInlineShowView extends DiscussionThreadShowView
    renderTemplate: ->
      @template = DiscussionUtil.getTemplate('_inline_thread_show')
      params = @model.toJSON()
      if @model.get('username')?
        params = $.extend(params, user:{username: @model.username, user_url: @model.user_url})
      Mustache.render(@template, params)

     
