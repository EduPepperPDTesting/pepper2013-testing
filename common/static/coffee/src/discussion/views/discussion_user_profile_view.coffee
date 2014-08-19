if Backbone?
  class @DiscussionUserProfileView extends Backbone.View
#    events:
#      "":""
    currPageNum = 0
    threadNum = 0
    initialize: (options) ->
      @renderThreads @$el, @collection
      @pageControlInit()
    renderThreads: ($elem, threads) =>
      #Content.loadContentInfos(response.annotated_content_info)
      @discussion = new Discussion()
      @discussion.reset(threads, {silent: false})
      $discussion = $(Mustache.render $("script#_user_profile").html(), {'threads':threads})
      $elem.append($discussion)
      pageval = @getURLParam("page")
      if pageval!=null
        currPageNum = parseInt(pageval.split("#")[0])-1
      else
        currPageNum = 0
      start = currPageNum*5
      end = start+5
      paging = @discussion.slice(start,end)
      threadNum = @discussion.length
      @threadviews = paging.map (thread) ->
        new DiscussionThreadProfileView el: @$("article#thread_#{thread.id}"), model: thread
      _.each @threadviews, (dtv) -> dtv.render()

    addThread: (thread, collection, options) =>
      # TODO: When doing pagination, this will need to repaginate. Perhaps just reload page 1?
      article = $("<article class='discussion-thread' id='thread_#{thread.id}'></article>")
      @$('section.discussion > .threads').prepend(article)
      threadView = new DiscussionThreadInlineView el: article, model: thread
      threadView.render()
      @threadviews.unshift threadView

    getURLParam:(name) ->
      reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i")
      r = window.location.search.substr(1).match(reg)
      if r != null
        return unescape(r[2])
      else
        return null
    pageControlInit:()->
      num = currPageNum+1
      container = $(".page");
      pageTotal = Math.ceil(threadNum/5)
      param = "?chapter=1&page="+num
      up_page = $('<a class="up_page" title="Pre"></a>')
      next_page = $('<a class="next_page" title="Next"></a>')
      if num==1
        up_page.attr("href","javascript:void(0);")
      else
        up_page.attr("href","?chapter=1&page="+(num-1))
      if num>=pageTotal
        next_page.attr("href","javascript:void(0);")
      else
        next_page.attr("href","?chapter=1&page="+(num+1))
      container.append(up_page)
      for i in [1..pageTotal]
        if num== i
          aele = $('<a>'+i+'</a>')
        else
          aele = $('<a class="page_active" href="?chapter=1&page='+i+'">'+i+'</a>')
        container.append(aele)
      container.append(next_page)
