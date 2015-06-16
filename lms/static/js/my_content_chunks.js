var mychunks_content_isload = false;
var mychunks_content_loadNum = 0;
var mychunks_content_totalNum = 0;
var mychunks_focus=0;
var mychunks_maxCharNum=1000;
var mychunks_share_focus=0;
var mychunks_share_maxCharNum=100;
var cur_course_id="";
var mychunks_notes_status="edit";
var mychunks_notes_text='';
$(function () {
    mychunks_content_update(mychunks_content_loadNum);
    $(".top_btn").click(function(){
      $(window).scrollTop(0);
    })
    $(".top_btn").mouseover(function(){
      $(this).find('.top_btn_img_1').hide();
      $(this).find('.top_btn_img_2').show();
    })
    $(".top_btn").mouseout(function(){
      $(this).find('.top_btn_img_1').show();
      $(this).find('.top_btn_img_2').hide();
    })
    $(window).bind("scroll", function(){
      var scrollTop = $(this).scrollTop();
　　  var scrollHeight = $(document).height();
　　  var windowHeight = $(this).height();
      if((scrollTop + windowHeight == scrollHeight) && mychunks_content_isload)
      {
        mychunks_content_loadNum=$(".chunk_title").length;
        mychunks_content_update(mychunks_content_loadNum);
      }
    })
    $(".mychunks_ftg_button").click(function(){
      var This=this;
      var content=$(".mychunks_content");
      var verticalID=$("#show_mychunks").attr("data-id");
      if(mychunks_notes_status=="update")
      {
        if(content.text().length<=mychunks_maxCharNum)
        {
          $(this).hide();
          var datainfo={'info':JSON.stringify({'note':content.html(),'vertical_id':verticalID})};
          $.post("/my_chunks/save_info",datainfo,function(data){
            mychunks_updateMaxCharNum();
            mychunks_notes_text=content.html();
            $(This).show();
          });
          //$("#show_mychunks").hide();
          //$("#lean_overlay").hide();
          mychunks_setNotesStatus("edit");
        }
        else
        {
          if(content.text().length>mychunks_maxCharNum)
            alert('Exceed the maximum number of characters.');
        }
      }
      else
      {
        mychunks_setNotesStatus("update");
      }
    });
    $(".mychunks_share_button").click(function(){
      var content=$(".mychunks_share_content");
      var user_id_arr=[];
      $(".share_checkbox").each(function(index) {
        if($(this).attr("ischeck")=="true")
        {
          user_id_arr.push($(this).attr("user-id"));
        }
      });
      if(content.text().length<=mychunks_share_maxCharNum&&user_id_arr.length>0)
      {
        var user_id=user_id_arr.length>1?user_id_arr.join(","):user_id_arr[0];
        var interviewer_id=$("#share_mychunks").attr("user-id");
        var interviewer_name=$("#share_mychunks").attr("user-name");
        var course_number=$("#share_mychunks").attr("course_number");
        var data_url=$("#share_mychunks").attr("data-url");
        var body=mychunks_share_focus>0?content.text():'';
        if (user_id_arr.length>1)
        {
          var datainfo={'info':JSON.stringify({'course_number':course_number,'user_id':user_id,'interviewer_id':interviewer_id,'interviewer_name':interviewer_name,'type':'my_chunks','body':body,'location':data_url,'date':(new Date()).toISOString(),'activate':'false','multiple':'true'})};
        }
        else
        {
          var datainfo={'info':JSON.stringify({'course_number':course_number,'user_id':user_id,'interviewer_id':interviewer_id,'interviewer_name':interviewer_name,'type':'my_chunks','body':body,'location':data_url,'date':(new Date()).toISOString(),'activate':'false'})};
        }
        $.post("/interactive_update/save_info",datainfo,function(){
          $("#shared_ok_mychunks").show();
          $("#lean_overlay").show();
          $(window).scrollTop(0);
        });
        $("#share_mychunks").hide();
        $("#lean_overlay").hide();
        content.html("");
        mychunks_share_updateMaxCharNum();
        content.html("<p class='mychunks_txt_prompt'>Add a Message ...</p>");
      }
      else
      {
        if(user_id_arr.length<=0)
          alert('Select at least one user.');
        if(content.text().length>mychunks_share_maxCharNum)
          alert('Exceed the maximum number of characters.');
      }
    });
    $(".mychunks_content").focusin(function(){
      if(!mychunks_focus)
      {
        $(this).html("");
        mychunks_focus=1;
      }
    });
    $(".mychunks_share_content").focusin(function(){
      if(!mychunks_share_focus)
      {
        $(this).html("");
        mychunks_share_focus=1;
      }
    });
    $(".mychunks_content").keyup(function(event){
      mychunks_updateMaxCharNum();
    });
    $(".mychunks_share_content").keyup(function(event){
      mychunks_share_updateMaxCharNum();
    });
    $(".mychunks_uploadBtn").click(function(){
    $("#mychunks_browseFile").click();
    })
    $(".mychunks_linkBtn").click(function(){
      $(".mychunks_linkwin").show();
    })
    $("#mychunks_hyperlink_okBtn").click(function(){
      var content = $(".mychunks_content");
      if($("#mychunks_link_url_val").val()!='')
      {
        if(!mychunks_focus)
        {
          content.html("");
          mychunks_focus=1;
        }
        content.html(content.html()+mychunks_hyperlinks($("#mychunks_link_url_val").val(),$("#mychunks_link_title_val").val()));
        $(".mychunks_linkwin").hide();
      }
    })
    $("#mychunks_hyperlink_cancelBtn").click(function(){
      $(".mychunks_linkwin").hide();
    })
    $("#mychunks_close").click(function(){
      $(".mychunks_linkwin").hide();
      var content = $('.mychunks_content');
      content.html("");
      mychunks_updateMaxCharNum();
    })
    $("#mychunks_share_close").click(function(){
      var content = $('.mychunks_share_content');
      content.html("");
      mychunks_share_updateMaxCharNum();
      content.html("<p class='mychunks_txt_prompt'>Add a Message ...</p>");
    })
    $(".share_checkbox").click(function() {
      if($(this).attr("ischeck")=="true"){
        mychunks_setShareStatus($(this),0);
      }
      else
      {
        mychunks_setShareStatus($(this),1);
      }
    });
    $(".select_all_checkbox").click(function() {
      if($(this).attr("ischeck")=="true"){
        mychunks_setShareStatus($(this),0);
        mychunks_setShareStatus($(".share_checkbox"),0);
      }
      else
      {
        mychunks_setShareStatus($(this),1);
        mychunks_setShareStatus($(".share_checkbox"),1);
      }
    });
    if($(".modal").css("zIndex")<10000)
    {
      $(".modal").addClass("leanmodalStyle");
      $(".modal").hide();
    }
    $("#show_mychunks").find(".close-modal").click(function(){
      $("#show_mychunks").hide();
      $(".linkwin").hide();
      $("#lean_overlay").hide();
      $(".mychunks_content").html("");
    })
    $("#del_mychunks").find(".close-modal").click(function(){
      $("#del_mychunks").hide();
      $("#lean_overlay").hide();
    })
    $("#share_mychunks").find(".close-modal").click(function(){
      $("#share_mychunks").hide();
      $("#lean_overlay").hide();
    })
    $("#shared_ok_mychunks").find(".close-modal").click(function(){
      $("#shared_ok_mychunks").hide();
      $("#lean_overlay").hide();
    })
    $("#rate_results").find(".close-modal").click(function(){
      $("#rate_results").hide();
      $("#lean_overlay").hide();
    })
    $(".mychunks_del_button").click(function(){
      var eleID=$("#del_mychunks").attr("ele-id");
      var courseID=$("#del_mychunks").attr("course-id");
      var datainfo={'info':JSON.stringify({'vertical_id':$("#del_mychunks").attr("data-id")})};
      $.post("/my_chunks/del_info",datainfo,function(data){
        var curDelObj=$("#"+eleID);
        if(curDelObj.prev().prop("className")=="chunks_info" && $("div[course-id="+"'"+courseID+"'"+"]").length==1)curDelObj.prev().remove();
        curDelObj.remove();
        if($(".chunks_info").length<1)
        $(".loadInfo").text("You have no content chunks bookmarked, please visit your favorite content, add them and share with your peers.");
      });
      $("#del_mychunks").hide();
      $("#lean_overlay").hide();
    })
    $(".mychunks_shared_ok_button").click(function(){
      $("#shared_ok_mychunks").hide();
      $("#lean_overlay").hide();
    }) 
    $("#lean_overlay").click(function(){
      $("#show_mychunks").hide();
      $("#del_mychunks").hide();
      $("#share_mychunks").hide();
      $("#shared_ok_mychunks").hide();
      $("#rate_results").hide();
      $(".linkwin").hide();
      $(".mychunks_content").html("");
      $(this).hide();
    })
    
    $(".mychunks_share_content").focusin(function(){
      if(!mychunks_share_focus)
      {
        $(this).html("");
        mychunks_share_focus=1;
      }
    });
 });

function mychunks_content_update(skip)
{
    mychunks_content_isload = false;
    $(".loadInfo").text("Loading ...");
    $(".loadInfo").show();
    $.post("/my_chunks/get_info_range",{skip:skip,limit:20},function(data){
        mychunks_content_init(data)
    });
}
function mychunks_content_init(data)
{   
    mychunks_content_totalNum = data.count;
    //mychunks_content_loadNum+=20;
    for(var i=0;i<data.results.length;i++)
    {
      mychunks_content_createItem(data.results[i]);
    }
    if(mychunks_content_loadNum>=mychunks_content_totalNum)
    {
        mychunks_content_isload = false;
        if(mychunks_content_totalNum>0)
        {
          $(".loadInfo").text("You have reached the end of your Pepper content chunks.");
        }
        else
        {
          $(".loadInfo").text("You have no content chunks bookmarked, please visit your favorite content, add them and share with your peers.");
        }
        $(".loadInfo").show();
    }
    else
    {
      mychunks_content_isload = true;
      $(".loadInfo").hide();
    }
    
    if($(window).scrollTop()>0)
    {
      $(".top_btn").show();
    }
    
} 
function mychunks_content_createItem(data)
{
  var ele_id="chunk_"+new Date().getTime()+Math.floor(Math.random()*999);
  var idArr=data.course_id.split("/");
  var data_id=idArr[0]+"/"+idArr[1];
  var ele=$('<div style="padding-bottom:20px;" class="chunks_info"><table cellspacing="10"><tr><td style="padding-top:15px;"><div style="width:280px; height:100px; background:url(/c4x/'+data_id+'/asset/course_author_img.jpg);background-repeat:no-repeat;"/></td><td style="vertical-align:middle;"><b>Course:</b> '+data.courseTitle+'</td></tr><tr><td width="400" style="padding-top:15px;"><b>My Chunks:</b></td><td style="padding-top:15px;"><b>Rate the Chunk:</b></td></tr></table></div>');
  element=$('<div style="padding-bottom:20px;" id="'+ele_id+'" course-id="'+data.course_id+'"><table><tr><td width="400"><div><a class="chunk_title" course_title="'+data.courseTitle+'" href="'+data.url+'">'+data.chunkTitle+'</a></div><div style="padding:5px 0 0 30px;" data-id="'+data.vertical_id+'"><a href="#" class="noteBtn"><span style="color:#388e9b;font-size:13px;">Notes</span></a> - <a href="#" class="shareBtn"><span style="color:#388e9b;font-size:13px;">Share</span></a> - <a href="#" class="delBtn"><span style="color:#388e9b;font-size:13px;">Delete</span></a></div></td><td><div class="rateSetItem" data-id="'+data.vertical_id+'"><table cellPadding=5><tr><td width="240">High-Quality</td><td><div class="hq_rate rateItem" data-name="hq_rate" data-score="'+data.hq_rate+'"></td></tr><tr><td>Interactive & Engaging</td><td><div class="ie_rate rateItem" data-name="ie_rate" data-score="'+data.ie_rate+'"></div></td></tr><tr><td>Practical Application</td><td><div class="pa_rate rateItem" data-name="pa_rate" data-score="'+data.pa_rate+'"></div></td></tr><tr><td></td><td><a class="see_results_btn btnx dashboard-btn1" href="javascript:void(0);" style="font-size:12px;padding:6px 20px 6px 20px;">See Results</a></td></tr></table></td></tr></table><hr/></div>');
  if(cur_course_id==""||cur_course_id!=data.course_id||$("div[course-id="+"'"+data.course_id+"'"+"]").length<1)
  {
    cur_course_id=data.course_id;
    $('.mychunks_container').append(ele);
  }
  $('.mychunks_container').append(element);

  element.find(".noteBtn").click(function(){
    $("#show_mychunks").show();
    $("#lean_overlay").show();
    $(".mychunks_ftg_button").hide();
    $(window).scrollTop(0);
    mychunks_setNotesStatus("edit")
    var vertical_id=$(this).parent().attr("data-id");
    $("#show_mychunks").attr("data-id",vertical_id)
    var datainfo={'info':JSON.stringify({'vertical_id':vertical_id})};
    $.post("/my_chunks/get_info",datainfo,function(data){
      mychunks_focus=1;
      if(data['results'][0].note==""||data['results'][0].note=="<br>")
      {
        $(".mychunks_content").html('<p class="mychunks_txt_prompt">Please click the "Edit" button to add notes, pictures and links.</p>');
      }
      else
      {
        $(".mychunks_content").html(data['results'][0].note);
      }
      mychunks_notes_text=data['results'][0].note;
      $(".mychunks_ftg_button").show();
      mychunks_updateMaxCharNum();
      });
  })
  element.find(".delBtn").click(function(){
    $("#del_mychunks").show();
    $("#lean_overlay").show();
    $("#del_mychunks").attr("data-id",$(this).parent().attr("data-id"))
    $("#del_mychunks").attr("ele-id",$(this).parent().parent().parent().parent().parent().parent().attr("id"))
    $("#del_mychunks").attr("course-id",$(this).parent().parent().parent().parent().parent().parent().attr("course-id"))
    $(window).scrollTop(0);
  })
  element.find(".shareBtn").click(function(){
    $("#share_mychunks").show();
    $("#lean_overlay").show();
    var chunk_title = $(this).parent().parent().find(".chunk_title");
    var chapter_num;
    var content=$(".mychunks_share_content");
    if(chunk_title.text().indexOf(":")>=0)
    {
      chapter_num=" "+chunk_title.text().split(':')[0];
    }
    else
    {
      chapter_num="";
    }
    $("#share_mychunks").attr("course_number",chunk_title.attr("course_title").split(" ")[0]+chapter_num);
    $("#share_mychunks").attr("data-url",chunk_title.attr("href"));
    content.html("");
    mychunks_share_updateMaxCharNum();
    content.html("<p class='mychunks_txt_prompt'>Add a Message ...</p>");
    $(window).scrollTop(0);
    mychunks_share_init();
  })
  element.find(".see_results_btn").click(function(){
    $("#rate_results").show();
    $("#lean_overlay").show();
    rate_integrate_init($(this).parent().parent().parent(),$("#rate_results"),$(this).parent().parent().parent().parent().parent().attr("data-id"));
    $(window).scrollTop(0);
  })
  rate_init($(element));
}
function mychunks_upload_file()
{
    var fd, files, max_filesize, settings;
    var content=$(".mychunks_content");
    max_filesize = 0.5 * 1000 * 1000;
    if (/\.(bmp|gif|jpg|jpeg|png|BMP|GIF|JPG|PNG)$/.test($("#mychunks_browseFile")[0].files[0].name)) {
    files = "";
    files = $("#mychunks_browseFile")[0].files[0];
    if (files != void 0) {
      if (files.size > max_filesize) {
        files = "";
        alert("File is too large. Max file size is 500 Kb.");
        $("#mychunks_browseFile")[0].files = [];
        return false;
      }
    } 
    fd = new FormData();
    fd.append('image_file', files);
    settings = {
      type: "POST",
      data: fd,
      processData: false,
      contentType: false,
      async: false,
      success: function(response) {
        if (response == null) {
          alert("Network error. Please try again.");
          return false;
        }
        if (response.success == true) {
          alert("Upload success!");
        } else {
          alert("Upload fail");
        }
        if(!mychunks_focus)
        {
          content.html("");
          mychunks_focus=1;
        }
        content.html(content.html()+"<img src='"+response.file_info+"' onload='mychunks_changeImg(this);' alt='[Image loading ...]'> </img>");
        mychunks_updateMaxCharNum();
      }
    }
    return $.ajax("/message_board/upload_image",settings);

  } else {
    alert("The file format is not supported.");
  }
}
function mychunks_changeImg(objImg)
{
 var max = 300;
 if(objImg.width > max)
 {
    var scaling = 1-(objImg.width-max)/objImg.width;
    objImg.width = objImg.width*scaling;
    objImg.height = objImg.height;
 }
}
function mychunks_hyperlinks(url,title)
{
  //return str.replace(new RegExp("("+"[a-zA-z]+://[^ ]*"+")",'g'),"<a href='$1' target='_blank'>$1</a>");
  if(title=="")
  title = url;
  if(url.indexOf('://')<0)
  url="http://"+url;
  return "<a href='"+url+"' target='_blank'>"+title+"</a><br/>";
}
function mychunks_updateMaxCharNum()
{
  var charNum = $(".mychunks_content").text().length;
  var num = charNum>mychunks_maxCharNum?"<font color='#ff0000'>"+charNum+"</font>":charNum;
  $("#mychunks_curr_char_num").html(num);
}
function mychunks_share_updateMaxCharNum()
{
  var charNum = $(".mychunks_share_content").text().length;
  var num = charNum>mychunks_share_maxCharNum?"<font color='#ff0000'>"+charNum+"</font>":charNum;
  $("#message_curr_char_num").html(num);
}
function mychunks_share_init()
{
  mychunks_share_focus=0;
  mychunks_setShareStatus($(".share_checkbox"),0);
  mychunks_setShareStatus($(".select_all_checkbox"),0);
}
mychunks_setShareStatus=function(ele,s)
{
  if(s)
  {
    ele.children(".checkbox_img_true").show();
    ele.children(".checkbox_img_false").hide();
    ele.attr("ischeck","true");
  }
  else
  {
    ele.children(".checkbox_img_false").show();
    ele.children(".checkbox_img_true").hide();
    ele.attr("ischeck","false");
  }
}
mychunks_setNotesStatus=function(s)
{
  if(s=="edit")
  {
    mychunks_notes_status="edit";
    $(".mychunks_ftg_button").html("Edit");
    $(".mychunks_content").attr("contenteditable","false");
    $(".mychunks_content").css("backgroundColor","#f6f6f6");
    $(".mychunks_uploadBtn").hide();
    $(".mychunks_linkBtn").hide();
  }
  else
  {
    mychunks_notes_status="update";
    $(".mychunks_ftg_button").html("Update");
    $(".mychunks_content").attr("contenteditable","true");
    $(".mychunks_content").css("backgroundColor","#ffffff");
    $(".mychunks_uploadBtn").show();
    $(".mychunks_linkBtn").show();
    if(mychunks_notes_text==''||mychunks_notes_text=='<br>')
    {
      $(".mychunks_content").html('');
    }
    mychunks_updateMaxCharNum();
  }
}
//----------------------------------------------------------Rating
function rate_init(element)
{
  $.fn.raty.defaults.path = '/static/js/vendor/raty/lib/img';
  element.find('.rateItem').raty({hints:['Poor','Fair','Average','Good','Great'],click: function(score, evt) {
      var This=this;
      var datainfo={'info':JSON.stringify({'rate_name':$(this).attr('data-name'),'rate_value':score,'vertical_id':$(this).parent().parent().parent().parent().parent().attr('data-id')})};
      $(this).parent().parent().parent().parent().find('.rateItem').raty('readOnly',true);
      $.post("/my_chunks/set_rate",datainfo,function(){
        $(This).parent().parent().parent().parent().find('.rateItem').raty('readOnly',false);
      });
    },
    score: function() {
      return $(this).attr('data-score');
    }

  });
  element.find('.hq_rate').raty('set',{starOn:'star-on-blue.png',starHalf:'star-half-blue.png'});
  element.find('.ie_rate').raty('set',{starOn:'star-on-green.png',starHalf:'star-half-green.png'});
  element.find('.pa_rate').raty('set',{starOn:'star-on-orange.png',starHalf:'star-half-orange.png'});
}
function rate_integrate_init(element,rate_ele,vertical_id)
{
  var hq_score=element.find('.hq_rate').raty("score");
  var ie_score=element.find('.ie_rate').raty("score");
  var pa_score=element.find('.pa_rate').raty("score");
  var hints=['Poor','Fair','Average','Good','Great'];
  if(hq_score!=undefined||ie_score!=undefined||pa_score!=undefined)
  {
    $(".rate_results_normal").show();
    $(".rate_results_warn").hide();
    $.fn.raty.defaults.path = '/static/js/vendor/raty/lib/img';
    rate_ele.find('.rateItem').raty({readOnly:true});
    var datainfo={'info':JSON.stringify({'vertical_id':vertical_id})};
    $.post("/my_chunks/get_integrate_rate",datainfo,function(data){
      rate_ele.find('.hq_rate').raty({readOnly:true,score:function(){
        return data.hq_rate.score
      }});
      rate_ele.find('.ie_rate').raty({readOnly:true,score:function(){
        return data.ie_rate.score
      }});
      rate_ele.find('.pa_rate').raty({readOnly:true,score:function(){
        return data.pa_rate.score
      }});
      rate_ele.find('#hq_rate_num').text(data.hq_rate.count);
      rate_ele.find('#ie_rate_num').text(data.ie_rate.count);
      rate_ele.find('#pa_rate_num').text(data.pa_rate.count);
      rate_ele.find('.hq_rate').raty('set',{starOn:'star-on-blue.png',starHalf:'star-half-blue.png'});
      rate_ele.find('.ie_rate').raty('set',{starOn:'star-on-green.png',starHalf:'star-half-green.png'});
      rate_ele.find('.pa_rate').raty('set',{starOn:'star-on-orange.png',starHalf:'star-half-orange.png'});
      rate_ele.find('.hq_rate').attr('title','');
      rate_ele.find('.ie_rate').attr('title','');
      rate_ele.find('.pa_rate').attr('title','');
      rate_ele.find('.hq_rate img').each(function(index, el) {
        $(el).attr('title',hints[index]);
      });
      rate_ele.find('.ie_rate img').each(function(index, el) {
        $(el).attr('title',hints[index]);
      });
      rate_ele.find('.pa_rate img').each(function(index, el) {
        $(el).attr('title',hints[index]);
      });
    });
  }
  else
  {
    $(".rate_results_normal").hide();
    $(".rate_results_warn").show();
  }
  
}