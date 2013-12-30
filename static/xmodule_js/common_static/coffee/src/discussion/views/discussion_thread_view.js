// Generated by CoffeeScript 1.6.3
(function() {
  var _ref,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  if (typeof Backbone !== "undefined" && Backbone !== null) {
    this.DiscussionThreadView = (function(_super) {
      __extends(DiscussionThreadView, _super);

      function DiscussionThreadView() {
        this._delete = __bind(this._delete, this);
        this.cancelEdit = __bind(this.cancelEdit, this);
        this.update = __bind(this.update, this);
        this.edit = __bind(this.edit, this);
        this.endorseThread = __bind(this.endorseThread, this);
        this.addComment = __bind(this.addComment, this);
        this.renderResponse = __bind(this.renderResponse, this);
        _ref = DiscussionThreadView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      DiscussionThreadView.prototype.events = {
        "click .discussion-submit-post": "submitComment"
      };

      DiscussionThreadView.prototype.$ = function(selector) {
        return this.$el.find(selector);
      };

      DiscussionThreadView.prototype.initialize = function() {
        DiscussionThreadView.__super__.initialize.call(this);
        return this.createShowView();
      };

      DiscussionThreadView.prototype.renderTemplate = function() {
        this.template = _.template($("#thread-template").html());
        return this.template(this.model.toJSON());
      };

      DiscussionThreadView.prototype.render = function() {
        this.$el.html(this.renderTemplate());
        this.$el.find(".loading").hide();
        this.delegateEvents();
        this.renderShowView();
        this.renderAttrs();
        this.$("span.timeago").timeago();
        this.makeWmdEditor("reply-body");
        this.renderResponses();
        return this;
      };

      DiscussionThreadView.prototype.cleanup = function() {
        if (this.responsesRequest != null) {
          return this.responsesRequest.abort();
        }
      };

      DiscussionThreadView.prototype.renderResponses = function() {
        var _this = this;
        setTimeout(function() {
          return _this.$el.find(".loading").show();
        }, 200);
        return this.responsesRequest = DiscussionUtil.safeAjax({
          url: DiscussionUtil.urlFor('retrieve_single_thread', this.model.get('commentable_id'), this.model.id),
          success: function(data, textStatus, xhr) {
            var comments;
            _this.responsesRequest = null;
            _this.$el.find(".loading").remove();
            Content.loadContentInfos(data['annotated_content_info']);
            comments = new Comments(data['content']['children']);
            comments.each(_this.renderResponse);
            return _this.trigger("thread:responses:rendered");
          }
        });
      };

      DiscussionThreadView.prototype.renderResponse = function(response) {
        var view;
        response.set('thread', this.model);
        view = new ThreadResponseView({
          model: response
        });
        view.on("comment:add", this.addComment);
        view.on("comment:endorse", this.endorseThread);
        view.render();
        this.$el.find(".responses").append(view.el);
        return view.afterInsert();
      };

      DiscussionThreadView.prototype.addComment = function() {
        return this.model.comment();
      };

      DiscussionThreadView.prototype.endorseThread = function(endorsed) {
        var is_endorsed;
        is_endorsed = this.$el.find(".is-endorsed").length;
        return this.model.set('endorsed', is_endorsed);
      };

      DiscussionThreadView.prototype.submitComment = function(event) {
        var body, comment, url,
          _this = this;
        event.preventDefault();
        url = this.model.urlFor('reply');
        body = this.getWmdContent("reply-body");
        if (!body.trim().length) {
          return;
        }
        this.setWmdContent("reply-body", "");
        comment = new Comment({
          body: body,
          created_at: (new Date()).toISOString(),
          username: window.user.get("username"),
          votes: {
            up_count: 0
          },
          abuse_flaggers: [],
          endorsed: false,
          user_id: window.user.get("id")
        });
        comment.set('thread', this.model.get('thread'));
        this.renderResponse(comment);
        this.model.addComment();
        return DiscussionUtil.safeAjax({
          $elem: $(event.target),
          url: url,
          type: "POST",
          dataType: 'json',
          data: {
            body: body
          },
          success: function(data, textStatus) {
            comment.updateInfo(data.annotated_content_info);
            return comment.set(data.content);
          }
        });
      };

      DiscussionThreadView.prototype.edit = function(event) {
        this.createEditView();
        return this.renderEditView();
      };

      DiscussionThreadView.prototype.update = function(event) {
        var newBody, newTitle, url,
          _this = this;
        newTitle = this.editView.$(".edit-post-title").val();
        newBody = this.editView.$(".edit-post-body textarea").val();
        url = DiscussionUtil.urlFor('update_thread', this.model.id);
        return DiscussionUtil.safeAjax({
          $elem: $(event.target),
          $loading: event ? $(event.target) : void 0,
          url: url,
          type: "POST",
          dataType: 'json',
          async: false,
          data: {
            title: newTitle,
            body: newBody
          },
          error: DiscussionUtil.formErrorHandler(this.$(".edit-post-form-errors")),
          success: function(response, textStatus) {
            _this.editView.$(".edit-post-title").val("").attr("prev-text", "");
            _this.editView.$(".edit-post-body textarea").val("").attr("prev-text", "");
            _this.editView.$(".edit-post-tags").val("");
            _this.editView.$(".edit-post-tags").importTags("");
            _this.editView.$(".wmd-preview p").html("");
            _this.model.set({
              title: newTitle,
              body: newBody,
              tags: response.content.tags
            });
            _this.createShowView();
            return _this.renderShowView();
          }
        });
      };

      DiscussionThreadView.prototype.createEditView = function() {
        if (this.showView != null) {
          this.showView.undelegateEvents();
          this.showView.$el.empty();
          this.showView = null;
        }
        this.editView = new DiscussionThreadEditView({
          model: this.model
        });
        this.editView.bind("thread:update", this.update);
        return this.editView.bind("thread:cancel_edit", this.cancelEdit);
      };

      DiscussionThreadView.prototype.renderSubView = function(view) {
        view.setElement(this.$('.thread-content-wrapper'));
        view.render();
        return view.delegateEvents();
      };

      DiscussionThreadView.prototype.renderEditView = function() {
        return this.renderSubView(this.editView);
      };

      DiscussionThreadView.prototype.createShowView = function() {
        if (this.editView != null) {
          this.editView.undelegateEvents();
          this.editView.$el.empty();
          this.editView = null;
        }
        this.showView = new DiscussionThreadShowView({
          model: this.model
        });
        this.showView.bind("thread:_delete", this._delete);
        return this.showView.bind("thread:edit", this.edit);
      };

      DiscussionThreadView.prototype.renderShowView = function() {
        return this.renderSubView(this.showView);
      };

      DiscussionThreadView.prototype.cancelEdit = function(event) {
        event.preventDefault();
        this.createShowView();
        return this.renderShowView();
      };

      DiscussionThreadView.prototype._delete = function(event) {
        var $elem, url,
          _this = this;
        url = this.model.urlFor('_delete');
        if (!this.model.can('can_delete')) {
          return;
        }
        if (!confirm("Are you sure to delete thread \"" + (this.model.get('title')) + "\"?")) {
          return;
        }
        this.model.remove();
        this.showView.undelegateEvents();
        this.undelegateEvents();
        this.$el.empty();
        $elem = $(event.target);
        return DiscussionUtil.safeAjax({
          $elem: $elem,
          url: url,
          type: "POST",
          success: function(response, textStatus) {}
        });
      };

      return DiscussionThreadView;

    })(DiscussionContentView);
  }

}).call(this);