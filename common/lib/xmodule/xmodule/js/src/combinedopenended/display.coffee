class @Rubric

  rubric_category_sel: '.rubric-category'
  rubric_sel: '.rubric'

  constructor: (el) ->
    @el = el

  initialize: (location) =>
    @$(@rubric_sel).data("location", location)
    @$('input[class="score-selection"]').change @tracking_callback
    # set up the hotkeys
    $(window).unbind('keydown', @keypress_callback)
    $(window).keydown @keypress_callback
    # display the 'current' carat
    @categories = @$(@rubric_category_sel)
    @category = @$(@categories.first())
    @category_index = 0

  # locally scoped jquery.
  $: (selector) ->
    $(selector, @el)

  keypress_callback: (event) =>
    # don't try to do this when user is typing in a text input
    if @$(event.target).is('input, textarea')
      return
    # for when we select via top row
    if event.which >= 48 and event.which <= 57
      selected = event.which - 48
    # for when we select via numpad
    else if event.which >= 96 and event.which <= 105
      selected = event.which - 96
    # we don't want to do anything since we haven't pressed a number
    else
      return

    # if we actually have a current category (not past the end)
    if(@category_index <= @categories.length)
      # find the valid selections for this category
      inputs = @$("input[name='score-selection-#{@category_index}']")
      max_score = inputs.length - 1

      if selected > max_score or selected < 0
        return
      inputs.filter("input[value=#{selected}]").click()

      @category_index++
      @category = @$(@categories[@category_index])
    
  tracking_callback: (event) =>
    target_selection = @$(event.target).val()
    # chop off the beginning of the name so that we can get the number of the category
    category = @$(event.target).data("category")
    location = @$(@rubric_sel).data('location')
    # probably want the original problem location as well

    data = {location: location, selection: target_selection, category: category}
    Logger.log 'rubric_select', data

  # finds the scores for each rubric category
  get_score_list: () =>
    # find the number of categories:
    num_categories = @$(@rubric_category_sel).length

    score_lst = []
    # get the score for each one
    for i in [0..(num_categories-1)]
      score = @$("input[name='score-selection-#{i}']:checked").val()
      score_lst.push(score)

    return score_lst

  get_total_score: () =>
    score_lst = @get_score_list()
    tot = 0
    for score in score_lst
      tot += parseInt(score)
    return tot

  check_complete: () =>
     # check to see whether or not any categories have not been scored
    num_categories = @$(@rubric_category_sel).length
    for i in [0..(num_categories-1)]
      score = @$("input[name='score-selection-#{i}']:checked").val()
      if score == undefined
        return false
    return true

class @CombinedOpenEnded

  wrapper_sel: 'section.xmodule_CombinedOpenEndedModule'
  coe_sel: 'section.combined-open-ended'
  reset_button_sel: '.reset-button'
  next_step_sel: '.next-step-button'
  question_header_sel: '.question-header'
  submit_evaluation_sel: '.submit-evaluation-button'
  result_container_sel: 'div.result-container'
  combined_rubric_sel: '.combined-rubric-container'
  open_ended_child_sel: 'section.open-ended-child'
  error_sel: '.error'
  #@begin:textarea className
  #@date:2013-11-02  
  #@end
  #answer_area_sel: 'textarea.answer'
  answer_area_sel: '.mceEditor'
  #@end
  answer_area_div_sel : 'div.answer'
  prompt_sel: '.prompt'
  rubric_wrapper_sel: '.rubric-wrapper'
  hint_wrapper_sel: '.hint-wrapper'
  message_wrapper_sel: '.message-wrapper'
  submit_button_sel: '.submit-button'
  #@begin:Code to show mockup and will be replaced later
  #@date:2013-11-02 
  #save_button_sel: '.save-button'
  #@end
  skip_button_sel: '.skip-button'
  file_upload_list_sel: '.file-upload-list'
  file_upload_sel: '.file-upload'
  file_upload_box_sel: '.file-upload-box'
  file_upload_preview_sel: '.file-upload-preview'
  #@begin:ora loading image
  #@date:2013-11-02 
  ora_loading_sel: '.ora-loading'
  #@end
  fof_sel: 'textarea.feedback-on-feedback'
  sub_id_sel: 'input.submission_id'
  grader_id_sel: 'input.grader_id'
  grader_status_sel: '.grader-status'
  info_rubric_elements_sel: '.rubric-info-item'
  rubric_collapse_sel: '.rubric-collapse'
  next_rubric_sel: '.rubric-next-button'
  previous_rubric_sel: '.rubric-previous-button'
  oe_alert_sel: '.open-ended-alert'

  constructor: (el) ->
    @el=el
    @$el = $(el)
    @reinitialize(el)
    $(window).keydown @keydown_handler
    $(window).keyup @keyup_handler

  # locally scoped jquery.
  $: (selector) ->
    $(selector, @el)

  reinitialize: () ->
    @has_been_reset = false
    @wrapper=@$(@wrapper_sel)
    @coe = @$(@coe_sel)

    @ajax_url = @coe.data('ajax-url')
    @get_html()
    @coe = @$(@coe_sel)

    #Get data from combinedopenended
    @allow_reset = @coe.data('allow_reset')
    @id = @coe.data('id')
    @state = @coe.data('state')
    @task_count = @coe.data('task-count')
    @task_number = @coe.data('task-number')
    @accept_file_upload = @coe.data('accept-file-upload')
    @location = @coe.data('location')
    @data_score = @coe.data('score')
    @data_weight = @coe.data('weight')
    # set up handlers for click tracking
    @rub = new Rubric(@coe)
    @rub.initialize(@location)
    @is_ctrl = false
    #Setup reset
    @reset_button = @$(@reset_button_sel)
    @reset_button.click @reset
    #Setup next problem
    @next_problem_button = @$(@next_step_sel)
    @next_problem_button.click @next_problem

    @question_header = @$(@question_header_sel)
    @question_header.click @collapse_question

    # valid states: 'initial', 'assessing', 'post_assessment', 'done'
    Collapsible.setCollapsibles(@$el)
    @submit_evaluation_button = @$(@submit_evaluation_sel)
    @submit_evaluation_button.click @message_post

    @results_container = @$(@result_container_sel)
    @combined_rubric_container = @$(@combined_rubric_sel)

    # Where to put the rubric once we load it
    @oe = @$(@open_ended_child_sel)

    @errors_area = @$(@oe).find(@error_sel)
    @answer_area = @$(@oe).find(@answer_area_sel)
    @prompt_container = @$(@oe).find(@prompt_sel)
    @rubric_wrapper = @$(@oe).find(@rubric_wrapper_sel)
    @hint_wrapper = @$(@oe).find(@hint_wrapper_sel)
    @message_wrapper = @$(@oe).find(@message_wrapper_sel)
    @submit_button = @$(@oe).find(@submit_button_sel)
    #@begin:Code to show the mockup and will be replaced later
    #@date:2013-11-02 
    #@save_button = @$(@oe).find(@save_button_sel)
    #@end
    @child_state = @oe.data('state')
    @child_type = @oe.data('child-type')
    if @child_type=="openended"
      @skip_button = @$(@oe).find(@skip_button_sel)
      @skip_button.click @skip_post_assessment

    @file_upload_area = @$(@oe).find(@file_upload_sel)
    @file_upload_list = @$(@oe).find(@file_upload_list_sel)
    @can_upload_files = false
    @open_ended_child= @$(@oe).find(@open_ended_child_sel)
    #@begin:ora-loading object reference
    #@date:2013-11-02 
    @ora_loading=@$(@oe).find(@ora_loading_sel)
    #@end
    #@begin:Dont show the out of sync message
    #@out_of_sync_message = 'The problem state got out of sync.  Try reloading the page.'
    @out_of_sync_message = ''
    #@end
    #@begin: Always show prompt
    #@date:2013-11-02
    if @task_number>1
      @prompt_show()
    else if @task_number==1 and @child_state!='initial'
      @prompt_show()
    #@end
    @find_assessment_elements()
    @find_hint_elements()

    @rebind()
  get_html_callback: (response) =>
    #@begin:Avoid the error caused by empty response
    #@date:2013-11-02   
    try
      @coe.replaceWith(response.html)
    catch
    #@end
    '''
    if@child_state!='initial'
      if document.documentElement.scrollTop==0 
        document.body.scrollTop = 0
      else
        document.documentElement.scrollTop = 0
    '''
  get_html: () =>
    url = "#{@ajax_url}/get_html"
    $.ajaxWithPrefix({
                   type: 'POST',
                   url: url,
                   data: {},
                   success: @get_html_callback,
                   async:false
                   });

  show_combined_rubric_current: () =>
    data = {}
    $.postWithPrefix "#{@ajax_url}/get_combined_rubric", data, (response) =>
      #@begin:Avoid the error caused by empty response
      #@date:2013-11-02   
      try
        if response.success
          @combined_rubric_container.after(response.html).remove()
          @combined_rubric_container= @$(@combined_rubric_sel)
          @toggle_rubric("")
          @rubric_collapse = @$(@rubric_collapse_sel)
          @rubric_collapse.click @toggle_rubric
          @hide_rubrics()
          @$(@previous_rubric_sel).click @previous_rubric
          @$(@next_rubric_sel).click @next_rubric
          if response.hide_reset
            @reset_button.hide()
      catch
      #@end

  message_post: (event)=>
    external_grader_message=$(event.target).parent().parent().parent()
    evaluation_scoring = $(event.target).parent()

    fd = new FormData()
    feedback = @$(evaluation_scoring).find(@fof_sel)[0].value
    submission_id = @$(external_grader_message).find(@sub_id_sel)[0].value
    grader_id = @$(external_grader_message).find(@grader_id_sel)[0].value
    score = @$(evaluation_scoring).find("input:radio[name='evaluation-score']:checked").val()

    fd.append('feedback', feedback)
    fd.append('submission_id', submission_id)
    fd.append('grader_id', grader_id)
    if(!score)
      @gentle_alert "You need to pick a rating before you can submit."
      return
    else
      fd.append('score', score)

    settings =
      type: "POST"
      data: fd
      processData: false
      contentType: false
      success: (response) =>
        @gentle_alert response.msg
        @$('section.evaluation').slideToggle()
        @message_wrapper.html(response.message_html)


    $.ajaxWithPrefix("#{@ajax_url}/save_post_assessment", settings)


  rebind: () =>
    # rebind to the appropriate function for the current state
    @answer_area.toggleClass(@location);
    @submit_button.unbind('click')
    @submit_button.show()
    #@begin:Code to show mockup and will be replaced later
    #@date:2013-11-02
    #@save_button.show()
    #@end
    @reset_button.hide()
    @hide_file_upload()
    @next_problem_button.hide()
    #@begin:Hide ora_loading
    #@date:2013-11-02
    @ora_loading.hide()
    #@end
    @hint_area.attr('disabled', false)
    #@begin:Hide rubric_wrapper
    #@date:2013-11-02
    @rubric_wrapper.hide()
    #@end
    #@begin:Code to show mockup and will be replaced later
    #@date:2013-11-02
    #@save_button.click @save_text
    #@end
    @submit_button.prop('value', 'Submit')
    @submit_button.click @save_answer
    #@begin: Dont show the Response text box when accept_file_upload is true
    #@date:2013-11-02
    if @accept_file_upload== "True"
       @answer_area.hide()
    #@end
    if @task_number==1 and @child_state=='assessing'
       @prompt_show()
    if @child_state == 'done'
      @rubric_wrapper.hide()
      #@begin:Code to show mockup and will be replaced later
      #@date:2013-11-02
      #@save_button.hide()
      #@end
    if @child_type=="openended"
      @skip_button.hide()
    if @allow_reset=="True"
      #@begin:Code to show mockup and will be replaced later
      #@date:2013-11-02
      #@show_combined_rubric_current()
      #@end
      @reset_button.show()
      @submit_button.hide()
      @answer_area.attr("disabled", true)
      @replace_text_inputs()
      @hint_area.attr('disabled', true)
      if @task_number<@task_count
        @gentle_alert "Your score did not meet the criteria to move to the next step."
    #@begin:Initialize the initial_submit state including tinyMCE
    #@date:2013-11-02
    else if @child_state == 'initial_submit'
      
      @answer_area.attr("disabled", false)
      if @accept_file_upload== "True"
         @submit_button.attr("disabled",true)
      @rubric_wrapper.hide()
      @setup_file_upload()
      tinyMCE_class_init(@location)
      #@begin:Always show prompt
      #@date:2013-11-02
      @prompt_show()
      #@end
    #@begin:Initialize the initial_submit state including tinyMCE
    #@date:2013-11-02
    else if @child_state == 'initial'
      @answer_area.attr("disabled", false)
      if @accept_file_upload== "True"
         @submit_button.attr("disabled",true)
      @setup_file_upload()
      tinyMCE_class_init(@location)
      #@begin:Always show prompt
      #@date:2013-11-02
      @prompt_show()
      #@end
    #@end
    else if @child_state == 'assessing'
      #@begin:Distinguish upload file and non-upload file in assessing
      @setup_file_upload()
      if @accept_file_upload== "True"
         @answer_area.hide()
      else
        @answer_area.attr("disabled", true)
        @replace_text_inputs()
      #@end
      @hide_file_upload()
      if @data_score!='correct'
        @rubric_wrapper.show()
      #@begin:Change the text shown in submit_button
      #@date:2013-11-02
      @submit_button.prop('value', 'Enter')
      #@end
      @submit_button.click @save_assessment
      @submit_button.attr("disabled",true)
      #@begin:Dont show answer_area
      #@date:2013-11-02
      $("#"+@answer_area.attr("id")+"_parent").remove()
      #@end
      @prompt_show()
      if @child_type == "openended"
        @submit_button.hide()
        @queueing()
        @grader_status = @$(@grader_status_sel)
        @grader_status.html("<span class='grading'>Your response has been submitted.  Please check back later for your grade.</span> ")
      else if @child_type == "selfassessment"
        @setup_score_selection()
    else if @child_state == 'post_assessment'
      if @child_type=="openended"
        @skip_button.show()
        @skip_post_assessment()
      @answer_area.attr("disabled", true)
      @replace_text_inputs()
      @submit_button.prop('value', 'Submit post-assessment')
      if @child_type=="selfassessment"
         @submit_button.click @save_hint
      else
        @submit_button.click @message_post
    else if @child_state == 'done'
      #@begin:Install file upload
      #@date:2013-11-02
      @setup_file_upload()
      #@end
      #@begin:Dont use rubric_current
      #@date:2013-11-02
      #@show_combined_rubric_current()
      #@end
      @rubric_wrapper.hide()
      @answer_area.attr("disabled", true)
      #@begin:Distinguish upload file and non-upload file in done
      #@date:2013-11-02
      if @accept_file_upload== "True"
         @answer_area.hide()
      else
        @answer_area.attr("disabled", true)
        @replace_text_inputs()
      #@end
      #@begin:Hide file_upload attribution
      #@date:2013-11-02
      @hide_file_upload()
      #@end
      @hint_area.attr('disabled', true)
      @submit_button.hide()
    
      @reset_button.show()
      if @child_type=="openended"
        @skip_button.hide()
      if @task_number<@task_count
        @next_problem_button.show()
      else
        @reset_button.show()
      $("#"+@answer_area.attr("id")+"_parent").remove()

  find_assessment_elements: ->
    @assessment = @$('input[name="grade-selection"]')

  find_hint_elements: ->
    @hint_area = @$('textarea.post_assessment')

  replace_answer: (response) =>
    if response.success
      @rubric_wrapper.html(response.rubric_html)
      @rubric_wrapper.show()
      @rub = new Rubric(@coe)
      @rub.initialize(@location)
      @child_state = 'assessing'
      @find_assessment_elements()
      @rebind()
      answer_area_div = @$(@answer_area_div_sel)
      answer_area_div.val(response.student_response)
    else
      @gentle_alert response.error

  save_answer: (event) =>
    @ora_loading.show()
    if @data_score!='correct'
      @rubric_wrapper.show()
    event.preventDefault()
    @answer_area.attr("disabled", true)
    max_filesize = 2*1000*1000 #2MB
    #pre_can_upload_files = @can_upload_files
    if @child_state == 'initial' or @child_state == 'initial_submit'
      files = ""
      if @can_upload_files == true
        files = @$(@file_upload_box_sel)[0].files[0]
        if files!= undefined and files!= null
          if files.size > max_filesize
            @can_upload_files = false
            files = ""
        else
          @can_upload_files = false
      fd = new FormData()
      fd.append('student_answer', @get_text())
      fd.append('student_file', "")
      fd.append('can_upload_files', @can_upload_files)
      fd.append('display_name',@$('.problemtype').text())
      fd.append('page',$("#sequence-list a.active").attr("data-element"))
      settings =
        type: "POST"
        data: fd
        processData: false
        contentType: false
        async: false
        success: (response) =>
          @ora_loading.hide()
          if response==null
            alert("Network error. Please try again.")
            return false
          if @data_score!='correct'
            @replace_answer(response)
          else
            @skip_assessment()

      $.ajaxWithPrefix("#{@ajax_url}/save_answer",settings)
    else
      @errors_area.html(@out_of_sync_message)
  #@begin:Save without submitting
  #@date:2013-11-02    
  save_text: (event) =>
    #event.preventDefault()
    @ora_loading.show()
    @child_state = 'initial'
    max_filesize = 2*1000*1000 #2MB
    #pre_can_upload_files = @can_upload_files
    if @child_state == 'initial'
      files = ""
      if @can_upload_files == true
        files = @$(@file_upload_box_sel)[0].files[0]
        if files != undefined
          if files.size > max_filesize
            @can_upload_files = false
            files = ""
        else
          @can_upload_files = false
      fd = new FormData()
      #fd.append('student_answer', @answer_area.val())
      fd.append('student_answer', @get_text())
      #alert("val_"+$(".mceEditor").attr("id")+"___"+@answer_area.attr("id"))
      #alert("mc"+tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML)
      fd.append('student_file', files)
      fd.append('file_info', '')
      fd.append('can_upload_files', @can_upload_files)

      settings =
        type: "POST"
        data: fd
        processData: false
        contentType: false
        async: false
        success: (response) =>
          @ora_loading.hide()
          alert("Successfully saved!")

      $.ajaxWithPrefix("#{@ajax_url}/save_text",settings)
    else
      @errors_area.html(@out_of_sync_message)
  #@end
  #@begin:Upload files
  #@date:2013-11-02
  upload_file: (event) =>
    event.preventDefault()
    @ora_loading.show()
    setTimeout(()=>
      @child_state = 'initial'
      max_filesize = 2*1000*1000 #2MB
      #pre_can_upload_files = @can_upload_files
      @can_upload_files = true
      if @child_state == 'initial'
        files = ""
        if @can_upload_files == true
          files = @$(@file_upload_box_sel)[0].files[0]
          if files != undefined 
            if files.size > max_filesize
              @can_upload_files = false
              files = ""
              alert("File is too large.(2MB limit per attachment)")
              @ora_loading.hide()
              @$(@file_upload_box_sel)[0].files=[]
              @$(@file_upload_box_sel)[0].outerHTML=@$(@file_upload_box_sel)[0].outerHTML
              @$(@file_upload_box_sel).change @preview_image
              return false
          else
            @can_upload_files = false

        fd = new FormData()
        #fd.append('student_answer', @answer_area.val())
        fd.append('student_answer', @get_text())
        #alert("val_"+$(".mceEditor").attr("id")+"___"+@answer_area.attr("id"))
        #alert("mc"+tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML)
        fd.append('student_file', files)
        fd.append('file_info', '')
        fd.append('can_upload_files', @can_upload_files)

        settings =
          type: "POST"
          data: fd
          processData: false
          contentType: false
          async: false
          success: (response) =>
            @ora_loading.hide()
            if response==null
              alert("Network error. Please try again.")
              return false
            if response.success==true
              @$(@file_upload_box_sel)[0].outerHTML=@$(@file_upload_box_sel)[0].outerHTML
              @$(@file_upload_box_sel).change @preview_image
              alert("The file upload is successful. PLEASE REMEMBER TO PRESS SUBMIT TO SAVE.")
            else
              alert("Upload fail")
            file_item=$(response.file_info).text().split("##")
            if /\.(gif|jpg|jpeg|png|GIF|JPG|PNG)$/.test(file_item[1])
                #insertImageItem=" | <a class='insert_image_btn' href='javascript:void(0)'>Insert Image</a>"
                insertImageItem=""
            else
                insertImageItem=""
            file_upload_item=$("<div class='file_upload_item' style='margin:10px;'>"+file_item[1]+" | <a href="+"'"+file_item[0]+"'"+" target='_blank'>Download</a><span class='file_upload_item_edit'> | <a class='remove_btn' href='javascript:void(0)' rel="+"'"+$(response.file_info).text()+"'"+">Remove</a>"+insertImageItem+"</span></div>")
            @file_upload_list.append(file_upload_item)
            file_upload_item.find(".remove_btn").click(()=> 
                @remove_file(file_item[2],file_upload_item)
            )
            #file_upload_item.find(".insert_image_btn").click(()=> 
                #tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML+="<img src="+"'"+file_item[0]+"'/>"
            #)
            answer_area_val=$("<div>"+@answer_area.val()+"</div>")
            answer_area_val.find(".file_url").each((i,ele) =>
              $(ele).remove()
            )
            @file_upload_list.find(".file_upload_item").each((i,ele) =>
              answer_area_val.append("<div class='file_url' style='display:none'>"+$(ele).find(".remove_btn")[0].rel+"</div>")
              #@answer_area.val(tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML)
            )
            #@answer_area.val(tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML)
            @answer_area.val(answer_area_val.html())
            if @file_upload_list.find('.file_upload_item').length>0
              @submit_button.attr('disabled',false)
            else
              @submit_button.attr('disabled',true)
        $.ajaxWithPrefix("#{@ajax_url}/save_text",settings)
      else
        @errors_area.html(@out_of_sync_message)
    ,2000)
  #@end
  #@begin:Delete uploaded files
  #@date:2013-11-02
  remove_file: (key,item) =>
    @ora_loading.show()
    setTimeout(()=>
      fd = new FormData()
      fd.append('file_key', key)
      settings =
          type: "POST"
          data: fd
          processData: false
          contentType: false
          async: false
          success: (response) =>
            if response==null
              @ora_loading.hide()
              alert("Network error. Please try again.")
              return false
            item.remove()
            answer_area_val=$("<div>"+@answer_area.val()+"</div>")
            answer_area_val.find(".file_url").each((i,ele) =>
              $(ele).remove();
            )
            #@answer_area.val(answer_area_val.html())
            @file_upload_list.find(".file_upload_item").each((i,ele) =>
              answer_area_val.append("<div class='file_url' style='display:none'>"+$(ele).find(".remove_btn")[0].rel+"</div>")
            )
            @answer_area.val(answer_area_val.html())
            @remove_confirm()
      $.ajaxWithPrefix("#{@ajax_url}/remove_file",settings)
    ,2000)
  #@end
  #@begin:Confirm and save after deleting the uploaded file
  #@date:2013-11-02
  remove_confirm:() =>
    @child_state = 'initial'
    max_filesize = 2*1000*1000 #2MB
    #pre_can_upload_files = @can_upload_files
    if @child_state == 'initial'
      files = ""
      if @can_upload_files == true
        files = @$(@file_upload_box_sel)[0].files[0]
        if files != undefined
          if files.size > max_filesize
            @can_upload_files = false
            files = ""
        else
          @can_upload_files = false
      fd = new FormData()
      #fd.append('student_answer', @answer_area.val())
      fd.append('student_answer', @get_text())
      #alert("val_"+$(".mceEditor").attr("id")+"___"+@answer_area.attr("id"))
      #alert("mc"+tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML)
      fd.append('student_file', '')
      fd.append('file_info', '')
      fd.append('can_upload_files', @can_upload_files)
      settings =
        type: "POST"
        data: fd
        processData: false
        contentType: false
        async: false
        success: (response) =>
          @ora_loading.hide()
          @$(@file_upload_box_sel)[0].outerHTML=@$(@file_upload_box_sel)[0].outerHTML
          @$(@file_upload_box_sel).change @preview_image
          if @file_upload_list.find('.file_upload_item').length>0
            @submit_button.attr('disabled',false)
          else
            @submit_button.attr('disabled',true)
            if @accept_file_upload == "True"
              #console.log("externalTimer del")
              @data_score='incorrect'
              externalTimer.delete({'type':'combinedopenended','weight':@data_weight,'id':@location})
          alert("The file is removed successfully.")

      $.ajaxWithPrefix("#{@ajax_url}/save_text",settings)
    else
      @errors_area.html(@out_of_sync_message)
  #@end
  #@begin:Confirm and save after uploading the file
  #@date:2013-11-02
  upload_confirm:() =>
    max_filesize = 2*1000*1000 #2MB
    #pre_can_upload_files = @can_upload_files
    if @child_state == 'initial' or @child_state == 'initial_submit'
      files = ""
      if @can_upload_files == true
        files = @$(@file_upload_box_sel)[0].files[0]
        if files != undefined
          if files.size > max_filesize
            @can_upload_files = false
            files = ""
        else
          @can_upload_files = false
      fd = new FormData()
      #fd.append('student_answer', @answer_area.val())
      fd.append('student_answer', @get_text())
      #alert("val_"+$(".mceEditor").attr("id")+"___"+@answer_area.attr("id"))
      #alert("mc"+tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML)
      fd.append('student_file', '')
      fd.append('file_info', '')
      fd.append('can_upload_files', @can_upload_files)
      settings =
        type: "POST"
        data: fd
        processData: false
        contentType: false
        async: false
        success: (response) =>
          @ora_loading.hide()
          alert("Upload success!")


      $.ajaxWithPrefix("#{@ajax_url}/save_text",settings)
    else
      @errors_area.html(@out_of_sync_message)
  #@end
  #@begin:Get the text
  #@date:2013-11-02
  get_text:()=>
    if @accept_file_upload!= "True"
      return tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML
    else
      return @answer_area.val()
  #@end
  #@begin:Set up the text
  #@date:2013-11-02
  set_text:(val)=>
    if @accept_file_upload!= "True"
      return tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML=val
    else
      return @answer_area.val(val)
  #@end
  keydown_handler: (event) =>
    #Previously, responses were submitted when hitting enter.  Add in a modifier that ensures that ctrl+enter is needed.
    if event.which == 17 && @is_ctrl==false
      @is_ctrl=true
    else if @is_ctrl==true && event.which == 13 && @child_state == 'assessing' && @rub.check_complete()
      @save_assessment(event)

  keyup_handler: (event) =>
    #Handle keyup event when ctrl key is released
    if event.which == 17 && @is_ctrl==true
      @is_ctrl=false

  save_assessment: (event) =>
    @ora_loading.show()
    @submit_button.attr("disabled",true)
    @submit_button.hide()
    event.preventDefault()
    if @child_state == 'assessing' && @rub.check_complete()
      checked_assessment = @rub.get_total_score()
      score_list = @rub.get_score_list()
      data = {'assessment' : checked_assessment, 'score_list' : score_list}
      $.postWithPrefix "#{@ajax_url}/save_assessment", data, (response) =>
        #@begin:Hide ora_loading \ when response is empty
        #@date:2013-11-02
        @ora_loading.hide()
        if response==null
            alert("Network error. Please try again.")
            return false
        if response.success
          if @accept_file_upload == "True"
            #console.log("externalTimer save")
            externalTimer.save({'type':'combinedopenended','weight':@data_weight,'id':@location})
          @child_state = response.state

          if @child_state == 'post_assessment'
            @hint_wrapper.html(response.hint_html)
            @find_hint_elements()
          else if @child_state == 'done'
            @rubric_wrapper.hide()

          @rebind()
        else
          @errors_area.html(response.error)
    else
      @errors_area.html(@out_of_sync_message)

  skip_assessment: () =>
    #$("#"+@answer_area.attr("id")+"_parent").remove()
    @submit_button.attr("disabled",true)
    @submit_button.hide()
    data = {'assessment' : 1, 'score_list' : 1}
    $.postWithPrefix "#{@ajax_url}/save_assessment", data, (response) =>
      @ora_loading.hide()
      if response==null
          alert("Network error. Please try again.")
          return false
      if response.success
        @child_state = response.state

        if @child_state == 'post_assessment'
          @hint_wrapper.html(response.hint_html)
          @find_hint_elements()
        else if @child_state == 'done'
          @rubric_wrapper.hide()

        @rebind()
      else
        @errors_area.html(response.error)
    
  save_hint:  (event) =>
    event.preventDefault()
    if @child_state == 'post_assessment'
      data = {'hint' : @hint_area.val()}

      $.postWithPrefix "#{@ajax_url}/save_post_assessment", data, (response) =>
        if response.success
          @message_wrapper.html(response.message_html)
          @child_state = 'done'
          @rebind()
        else
          @errors_area.html(response.error)
    else
      @errors_area.html(@out_of_sync_message)

  skip_post_assessment: =>
    if @child_state == 'post_assessment'

      $.postWithPrefix "#{@ajax_url}/skip_post_assessment", {}, (response) =>
        if response.success
          @child_state = 'done'
          @rebind()
        else
          @errors_area.html(response.error)
    else
      @errors_area.html(@out_of_sync_message)

  reset: (event) =>
    event.preventDefault()
    if @child_state == 'done' or @allow_reset=="True"
      $.postWithPrefix "#{@ajax_url}/reset", {}, (response) =>
        @ora_loading.hide()
        if @accept_file_upload== "True"
            @answer_area.hide()
        if response==null
            alert("Network error. Please try again.")
            return false
        if response.success
          @answer_area.val('')
          @rubric_wrapper.html('')
          @hint_wrapper.html('')
          @message_wrapper.html('')
          @child_state = 'initial'
          @coe.after(response.html).remove()
          @allow_reset="False"
          @reinitialize(@element)
          @has_been_reset = true
          tinyMCE_sate(0)
          @rebind()
          @reset_button.hide()
        else
          @errors_area.html(response.error)
    else
      @errors_area.html(@out_of_sync_message)

  next_problem: =>
    if @child_state == 'done'
      $.postWithPrefix "#{@ajax_url}/next_problem", {}, (response) =>
        if response.success
          @answer_area.val('')
          @rubric_wrapper.html('')
          @hint_wrapper.html('')
          @message_wrapper.html('')
          @child_state = 'initial'
          @coe.after(response.html).remove()
          @reinitialize(@element)
          @rebind()
          @next_problem_button.hide()
          if !response.allow_reset
            @gentle_alert "Moved to next step."
          else
            @gentle_alert "Your score did not meet the criteria to move to the next step."
            @show_combined_rubric_current()
        else
          @errors_area.html(response.error)
    else
      @errors_area.html(@out_of_sync_message)

  gentle_alert: (msg) =>
    if @$el.find(@oe_alert_sel).length
      @$el.find(@oe_alert_sel).remove()
    alert_elem = "<div class='open-ended-alert'>" + msg + "</div>"
    @$el.find('.open-ended-action').after(alert_elem)
    @$el.find(@oe_alert_sel).css(opacity: 0).animate(opacity: 1, 700)

  queueing: =>
    if @child_state=="assessing" and @child_type=="openended"
      if window.queuePollerID # Only one poller 'thread' per Problem
        window.clearTimeout(window.queuePollerID)
      window.queuePollerID = window.setTimeout(@poll, 10000)

  poll: =>
    $.postWithPrefix "#{@ajax_url}/check_for_score", (response) =>
      if response.state == "done" or response.state=="post_assessment"
        delete window.queuePollerID
        @reload()
      else
        window.queuePollerID = window.setTimeout(@poll, 10000)
  #@begin:Upload configuration file
  #@date:2013-11-02 
  setup_file_upload: =>
    if @accept_file_upload == "True"
      @answer_area.hide()
      if window.File and window.FileReader and window.FileList and window.Blob
        @can_upload_files = true
        @file_upload_area.html('<input type="file" class="file-upload-box"><img class="file-upload-preview" src="#" alt="" />')
        @file_upload_area.show()
        @$(@file_upload_preview_sel).hide()
        @$(@file_upload_box_sel).change @preview_image
        #alert($("<div>"+@answer_area.val()+"</div>").find(".file_url").length)
        @file_upload_list.empty()
        $("<div>"+@answer_area.val()+"</div>").find(".file_url").each((i,ele) =>
            file_item=$(ele).text().split("##")
            if /\.(gif|jpg|jpeg|png|GIF|JPG|PNG)$/.test(file_item[1])
              #insertImageItem=" | <a class='insert_image_btn' href='javascript:void(0)'>Insert Image</a>"
              insertImageItem=""
            else
              insertImageItem=""
            file_upload_item=$("<div class='file_upload_item' style='margin:10px;'>"+file_item[1]+" | <a href="+"'"+file_item[0]+"'"+" target='_blank'>Download</a><span class='file_upload_item_edit'> | <a class='remove_btn' href='javascript:void(0)' rel="+"'"+$(ele).text()+"'"+">Remove</a>"+insertImageItem+"</span></div>")
            @file_upload_list.append(file_upload_item)
            file_upload_item.find(".remove_btn").click(()=> 
                @remove_file(file_item[2],file_upload_item)
            )
            #file_upload_item.find(".insert_image_btn").click(()=> 
                #tinyMCE.getInstanceById(@answer_area.attr("id")).getBody().innerHTML+="<img src="+"'"+file_item[0]+"'/>"
            #)
            
        )
        if @file_upload_list.find('.file_upload_item').length>0
          @submit_button.attr('disabled',false)
        else
          @submit_button.attr('disabled',true)
      else
        @gentle_alert 'File uploads are required for this question, but are not supported in this browser. Try the newest version of google chrome.  Alternatively, if you have uploaded the image to the web, you can paste a link to it into the answer box.'
  #@end
  hide_file_upload: =>
    if @accept_file_upload == "True"
      @file_upload_area.hide()
      @file_upload_list.find(".file_upload_item_edit").hide()

  replace_text_inputs: =>
    answer_class = @answer_area.attr('class')
    answer_id = @answer_area.attr('id')
    #@begin:Get value of HTML output
    #@date:2013-11-02 
    if $("#"+@answer_area.attr("id")+"_parent").length>0
      answer_val = @get_text()
    else
      answer_val = @answer_area.val()
    #@end
    new_text = ''
    new_text = "<div class='#{answer_class}' id='#{answer_id}'>#{answer_val}</div>"
    @answer_area.replaceWith(new_text)
  # wrap this so that it can be mocked
  reload: ->
    @reinitialize()

  collapse_question: (event) =>
    @prompt_container.slideToggle()
    @prompt_container.toggleClass('open')
    if @question_header.text() == "Hide Prompt"
      new_text = "Show Prompt"
      Logger.log 'oe_hide_question', {location: @location}
    else
      Logger.log 'oe_show_question', {location: @location}
      new_text = "Hide Prompt"
    @question_header.text(new_text)
    return false

  hide_rubrics: () =>
    rubrics = @$(@combined_rubric_sel)
    for rub in rubrics
      if @$(rub).data('status')=="shown"
        @$(rub).show()
      else
        @$(rub).hide()

  next_rubric: =>
    @shift_rubric(1)
    return false

  previous_rubric: =>
    @shift_rubric(-1)
    return false

  shift_rubric: (i) =>
    rubrics = @$(@combined_rubric_sel)
    number = 0
    for rub in rubrics
      if @$(rub).data('status')=="shown"
        number = @$(rub).data('number')
      @$(rub).data('status','hidden')
    if i==1 and number < rubrics.length - 1
      number = number + i

    if i==-1 and number>0
      number = number + i

    @$(rubrics[number]).data('status', 'shown')
    @hide_rubrics()

  prompt_show: () =>
    if @prompt_container.is(":hidden")==true
      @prompt_container.slideToggle()
      @prompt_container.toggleClass('open')
      @question_header.text("Hide Prompt")

  prompt_hide: () =>
    if @prompt_container.is(":visible")==true
      @prompt_container.slideToggle()
      @prompt_container.toggleClass('open')
      @question_header.text("Show Prompt")

  log_feedback_click: (event) ->
    link_text = @$(event.target).html()
    if link_text == 'See full feedback'
      Logger.log 'oe_show_full_feedback', {}
    else if link_text == 'Respond to Feedback'
      Logger.log 'oe_show_respond_to_feedback', {}
    else
      generated_event_type = link_text.toLowerCase().replace(" ","_")
      Logger.log "oe_" + generated_event_type, {}
  log_feedback_selection: (event) ->
    target_selection = @$(event.target).val()
    Logger.log 'oe_feedback_response_selected', {value: target_selection}

  remove_attribute: (name) =>
    if @$(@file_upload_preview_sel).attr(name)
      @$(@file_upload_preview_sel)[0].removeAttribute(name)

  preview_image: (event) =>
    if @$(@file_upload_box_sel)[0].files && @$(@file_upload_box_sel)[0].files[0]
      @upload_file(event)

  toggle_rubric: (event) =>
    info_rubric_elements = @$(@info_rubric_elements_sel)
    info_rubric_elements.slideToggle()
    return false

  setup_score_selection: () =>
    @$("input[class='score-selection']").change @graded_callback

  graded_callback: () =>
    if @rub.check_complete()
      @submit_button.attr("disabled",false)
      @submit_button.show()