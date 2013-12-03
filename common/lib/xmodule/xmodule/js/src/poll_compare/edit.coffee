class @POLLCompareEditingDescriptor
  @isInactiveClass : "is-inactive"

  constructor: (element) ->
    @element = element;
    @base_asset_url = @element.find("#editor-tab").data('base-asset-url')
    if @base_asset_url == undefined
      @base_asset_url = null

    @advanced_editor = CodeMirror.fromTextArea($(".edit-box", @element)[0], {
      mode: "text/xml"
      lineNumbers: true
      lineWrapping: true
      tabindex: 1
    })

    @$advancedEditorWrapper = $(@advanced_editor.getWrapperElement())
    @$advancedEditorWrapper.addClass(POLLCompareEditingDescriptor.isInactiveClass)

#   This is a workaround for the fact that tinyMCE's baseURL property is not getting correctly set on AWS
#   instances (like sandbox). It is not necessary to explicitly set baseURL when running locally.
    @$baseUrl = "/static"
    tinyMCE.baseURL = "#{@$baseUrl}/js/vendor/tiny_mce"
    @tiny_mce_textarea = $(".tiny-mce", @element).tinymce({
      script_url : "#{@$baseUrl}/js/vendor/tiny_mce/tiny_mce.js",
      theme : "advanced",
      skin: 'studio',
      schema: "html5",
      # Necessary to preserve relative URLs to our images.
      convert_urls : false,
      # TODO: we should share this CSS with studio (and LMS)
      content_css : "#{@$baseUrl}/css/tiny-mce.css",
      # The default popup_css path uses an absolute path referencing page in which tinyMCE is being hosted.
      # Supply the correct relative path instead.
      popup_css: "#{@$baseUrl}/js/vendor/tiny_mce/themes/advanced/skins/default/dialog.css",
      formats : {
        # Disable h4, h5, and h6 styles as we don't have CSS for them.
        h4: {},
        h5: {},
        h6: {},
        # tinyMCE does block level for code by default
        code: {inline: 'code'}
      },
      # Disable visual aid on borderless table.
      visual:false,
      # We may want to add "styleselect" when we collect all styles used throughout the LMS
      theme_advanced_buttons1 : "formatselect,bold,italic,underline,|,bullist,numlist,outdent,indent,|,blockquote,wrapAsCode,|,link,unlink",
      theme_advanced_toolbar_location : "top",
      theme_advanced_toolbar_align : "left",
      theme_advanced_statusbar_location : "none",
      theme_advanced_resizing : true,
      theme_advanced_blockformats : "p,pre,h1,h2,h3",
      width: '100%',
      height: '400px',
      setup : @setupTinyMCE,
      # Cannot get access to tinyMCE Editor instance (for focusing) until after it is rendered.
      # The tinyMCE callback passes in the editor as a paramter.
      init_instance_callback: @initInstanceCallback
    })

    @showingVisualEditor = false
    # Doing these find operations within onSwitchEditor leads to sporadic failures on Chrome (version 20 and older).
    $element = $(element)
    @$htmlTab = $element.find('.html-tab')
    @$visualTab = $element.find('.visual-tab')
    @element.on('click', '.editor-tabs .tab', @onSwitchEditor)

    # @element.off('click', '.editor-tabs .tab', @onSwitchEditor)
    # text = @advanced_editor.getValue()
    # alert("text:".concat(text))
    
    # @$htmlTab.addClass('current')
    # @$visualTab.removeClass('current')
    # @$mceToolbar.toggleClass(POLLCompareEditingDescriptor.isInactiveClass)
    # @$advancedEditorWrapper.toggleClass(POLLCompareEditingDescriptor.isInactiveClass)

    # visualEditor = @getVisualEditor()
    # @showAdvancedEditor(visualEditor)

    # @advanced_editor.setCursor(0)
    # @advanced_editor.refresh()
    # @advanced_editor.focus()
    # @showingVisualEditor = false    

  setupTinyMCE: (ed) =>
    ed.addButton('wrapAsCode', {
      title : 'Code',
      image : "#{@$baseUrl}/images/ico-tinymce-code.png",
      onclick : () ->
        ed.formatter.toggle('code')
        # Without this, the dirty flag does not get set unless the user also types in text.
        # Visual Editor must be marked as dirty or else we won't populate the Advanced Editor from it.
        ed.isNotDirty = false
    })

    ed.onNodeChange.add((editor, command, e) ->
      command.setActive('wrapAsCode', e.nodeName == 'CODE')
    )

    @visualEditor = ed

  onSwitchEditor: (e) =>
    e.preventDefault();
    $currentTarget = $(e.currentTarget)
    if not $currentTarget.hasClass('current')
      $currentTarget.addClass('current')
      @$mceToolbar.toggleClass(POLLCompareEditingDescriptor.isInactiveClass)
      @$advancedEditorWrapper.toggleClass(POLLCompareEditingDescriptor.isInactiveClass)

      visualEditor = @getVisualEditor()
      if $currentTarget.data('tab') is 'visual'
        @$htmlTab.removeClass('current')
        @showVisualEditor(visualEditor)
      else
        @$visualTab.removeClass('current')
        @showAdvancedEditor(visualEditor)

    # options = {
    #   mode: "text/xml"
    #   lineNumbers: true
    #   lineWrapping: true
    #   tabindex: 1
    # }
    
    # line = @advanced_editor.getLineHandle(0)
    # mode = window.CodeMirror.getMode(options, "text/xml")
    # state = @advanced_editor.getStateAfter(line)
    # line.highlight(mode, state, 4)
    # styles = line.styles
    
    # @advanced_editor.displayName = "";
    # @advanced_editor.name = "";
    # @advanced_editor.reset = "";
    # @advanced_editor._question = "";
    # @advanced_editor.answers = new Array();
    # tagN = 0;

    # for i in [0..styles.length]
    #   if styles[i] == "display_name"
    #     @advanced_editor.display_name = styles[i+4]
    #   else if styles[i] == "name"
    #     @advanced_editor.name = styles[i+4]
    #   else if styles[i] == "reset"
    #     @advanced_editor.reset = styles[i+4]
    #   else if styles[i] == "tag" && tagN < 2
    #     tagN++
    #     if tagN == 2
    #       while styles[i]!="<answer" && i<styles.length
    #         if styles[i]!="atom" && styles[i]!="" &&  styles[i]!=null && styles[i]!="tag"
    #           @advanced_editor._question = @advanced_editor._question.concat(styles[i])
    #         i++
    #       i--
    #   else if styles[i] == "<answer" || styles[i] == "</answer><answer"
    #     _id = styles[i+8]
    #     _answer = ""
    #     i += 11
    #     while (styles[++i]!="</answer><answer" && styles[i]!="</answer>" && i<styles.length)
    #       if styles[i]!="atom" && styles[i]!="tag" && styles[i]!=null && styles[i]!="</answer></poll_question>"
    #         _answer = _answer.concat(styles[i])

    #     tmpAnswer = {
    #       "id": _id,
    #       "answer": _answer
    #     }
    #     @advanced_editor.answers.push(tmpAnswer)

  # Show the Advanced (codemirror) Editor. Pulled out as a helper method for unit testing.
  showAdvancedEditor: (visualEditor) ->
    if visualEditor.isDirty()
      content = rewriteStaticLinks(visualEditor.getContent({no_events: 1}), @base_asset_url, '/static/')
      @advanced_editor.setValue(content)
      @advanced_editor.setCursor(0)
    @advanced_editor.refresh()
    @advanced_editor.focus()
    @showingVisualEditor = false

  # Show the Visual (tinyMCE) Editor. Pulled out as a helper method for unit testing.
  showVisualEditor: (visualEditor) ->
    # In order for isDirty() to return true ONLY if edits have been made after setting the text,
    # both the startContent must be sync'ed up and the dirty flag set to false.
    content = rewriteStaticLinks(@advanced_editor.getValue(), '/static/', @base_asset_url)
    visualEditor.setContent(content)
    visualEditor.startContent = content
    @focusVisualEditor(visualEditor)
    @showingVisualEditor = true

  initInstanceCallback: (visualEditor) =>
    visualEditor.setContent(rewriteStaticLinks(@advanced_editor.getValue(), '/static/', @base_asset_url))
    @focusVisualEditor(visualEditor)

  focusVisualEditor: (visualEditor) =>
    visualEditor.focus()
    # Need to mark editor as not dirty both when it is initially created and when we switch back to it.
    visualEditor.isNotDirty = true
    if not @$mceToolbar?
      @$mceToolbar = $(@element).find('table.mceToolbar')

  getVisualEditor: () ->
    ###
    Returns the instance of TinyMCE.
    This is different from the textarea that exists in the HTML template (@tiny_mce_textarea.

    Pulled out as a helper method for unit test.
    ###
    return @visualEditor

  unescape: (str) ->
    str = str.replace("$lt;", "<")
    str = str.replace("&gt;", ">")
    str = str.replace("&amp;", "&")
    return str

  save: ->
    @element.off('click', '.editor-tabs .tab', @onSwitchEditor)
    text = @advanced_editor.getValue()
    # alert("text:".concat(text))
    data: text
    # if @showingVisualEditor and visualEditor.isDirty()
    #   text = rewriteStaticLinks(visualEditor.getContent({no_events: 1}), @base_asset_url, '/static/')

    # data: text
    # {
    #   data: {
    #     'question': unescape(@advanced_editor._question),

    #     'answers': [{
    #               'text': unescape(@advanced_editor.answers[0].answer),
    #               'id': unescape(@advanced_editor.answers[0].id)
    #           },{
    #               'text': unescape(@advanced_editor.answers[1].answer),
    #               'id': unescape(@advanced_editor.answers[1].id)
    #           },{
    #               'text': unescape(@advanced_editor.answers[2].answer),
    #               'id': unescape(@advanced_editor.answers[2].id)
    #           }]},
    #   nullout: ['markdown']
    # }
