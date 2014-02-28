if Backbone?
  class @DiscussionThreadEditView extends Backbone.View

    events:
      "click .post-update": "update"
      "click .post-cancel": "cancel_edit"

    $: (selector) ->
      @$el.find(selector)

    initialize: ->
      super()

    render: ->
      @template = _.template($("#thread-edit-template").html())
      @$el.html(@template(@model.toJSON()))
      @delegateEvents()
      @$el.find('.edit-post-title').val(@model.get('title'))
      @$el.find('.edit-post-body').html(@model.get('body'))
      DiscussionUtil.makeWmdEditor @$el, $.proxy(@$, @), "edit-post-body"
      @$(".edit-post-tags").tagsInput DiscussionUtil.tagsInputOptions()
      @

    update: (event) ->
      @trigger "thread:update", event

    cancel_edit: (event) ->
      @trigger "thread:cancel_edit", event
