MyChunks=function()
{
  this.chunkTitle="";
  this.courseTitle="";
  this.courseID="";
  this.verticalID="";
  this.userID="";
  this.note="";
  this.URL="";
  this.status=false;
  this.iconLink=null;
  this.cur_vertical_link=null;
  this.isExist=false;
  this.notes_status="edit";
  this.notes_text="";
}
MyChunks.prototype.init=function(position)
{
  This=this;
  this.iconLink=$(".my_chunks_nav_icon");
  this.cur_vertical_link=$("#sequence-list li .active");
  this.cur_chapter_num=get_chapter_num($(".ui-accordion-content .active .section_link").children('p').clone().children().remove().end().text());
  this.iconLink.show();
  this.userID=this.iconLink.find('a').attr("user_id");
  this.verticalID=this.cur_vertical_link.attr("data-id");
  this.courseTitle=$.trim($("#page-nav h2").clone().children().remove().end().text());
  if(this.cur_chapter_num.indexOf(".")>=0){
    this.chunkTitle=this.cur_chapter_num+'.'+position+': '+(this.cur_vertical_link.children('p').clone().children().remove().end().text().split("\n")[0]);
  }
  else{
    this.chunkTitle=this.cur_vertical_link.children('p').clone().children().remove().end().text().split("\n")[0];
  }
  this.course_id=window.location.href.split("courses/")[1].split("/courseware")[0];
  var tempURL='/courses/'+window.location.href.split('/courses/')[1];
  this.URL=tempURL.substr(0,tempURL.lastIndexOf("/")+1)+position;
  mychunks_focus=0;
  $(".mychunks_ftg_button").unbind("click");
  $(".mychunks_delBtn").unbind("click");
  $(".mychunks_del_button").unbind("click");
   $(".mychunks_add_button").unbind("click");
  $(".my_chunks_btn").unbind("click");
  $(".mychunks_content").unbind("click");
  $(".mychunks_content").unbind("keyup");
  $(".mychunks_uploadBtn").unbind("click");
  $(".mychunks_linkBtn").unbind("click");
  $("#mychunks_hyperlink_okBtn").unbind("click");
  $("#mychunks_hyperlink_cancelBtn").unbind("click");
  $("#mychunks_close").unbind("click");
  $("#lean_overlay").unbind("click");
  $(".mychunks_ftg_button").click(function(){
      if(This.notes_status=="update"){
        This.save(1);
        if($(".mychunks_content").text().length<=mychunks_maxCharNum)
        This.setNotesStatus("edit");
      }
      else
      {
        This.setNotesStatus("update");
      }
      
  });
  $(".mychunks_del_button").click(function(){
      This.delete();
      $("#del_mychunks").hide();
      $("#lean_overlay").hide();
  });
  $(".my_chunks_btn").click(function(event) {
    $("#lean_overlay").show();
    This.setNotesStatus("edit");
    if(!This.isExist)
    {
      This.save(0);
    }
    else
    {
      $("#show_mychunks").show();
      This.load();
    }
      
  });
  $(".mychunks_content").focusin(function(){
      if(!mychunks_focus)
      {
        $(this).html("");
        mychunks_focus=1;
      }
  });
  $(".mychunks_content").keyup(function(event){
    mychunks_updateMaxCharNum();
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
  if($(".modal").css("zIndex")<10000)
  {
    $(".modal").addClass("leanmodalStyle");
    $(".modal").hide();
  }
  $("#show_mychunks").find(".close-modal").click(function(){
    $("#show_mychunks").hide();
    $("#lean_overlay").hide();
  })
  $("#del_mychunks").find(".close-modal").click(function(){
    $("#del_mychunks").hide();
    $("#lean_overlay").hide();
  })
  $(".mychunks_delBtn").click(function(){
    $("#show_mychunks").hide();
    $("#del_mychunks").show();
  })
  $(".mychunks_add_button").click(function(){
    $("#add_mychunks").hide();
    $("#show_mychunks").show();
    $("#mychunks_course_title").html(This.courseTitle);
    $("#mychunks_chunk_title").html(This.chunkTitle);
  })
  $("#add_mychunks").find(".close-modal").click(function(){
    $("#add_mychunks").hide();
    $("#lean_overlay").hide();
  })
  $("#lean_overlay").click(function(){
    $("#show_mychunks").hide();
    $("#del_mychunks").hide();
    $(".linkwin").hide();
    $(this).hide();
    if($("#add_mychunks").is(':visible'))
    {
      $("#add_mychunks").hide();
      $("#show_mychunks").show();
      $(this).show();
    }
  })
  this.load();
}
MyChunks.prototype.load=function()
{
  This=this;
  $("#mychunks_course_title").html("");
  $("#mychunks_chunk_title").html("");
  $(".mychunks_content").html("");
  $(".mychunks_ftg_button").hide();
  $(".mychunks_delBtn").hide();
  var datainfo={'info':JSON.stringify({'user_id':this.userID,'vertical_id':this.verticalID})};
  $.post("/my_chunks/get_info",datainfo,function(data){
    $("#my_chunks_link").show();
    $("#mychunks_course_title").html(This.courseTitle);
    $("#mychunks_chunk_title").html(This.chunkTitle);
    if(data['results'].length>0)
    {
      This.setStatus(1);
      mychunks_focus=1;
      This.isExist=true;
      $(".mychunks_delBtn").show();
      if(data['results'][0].note==""||data['results'][0].note=="<br>")
      {
        $(".mychunks_content").html('<p style="color:#646464">Please click the "Edit" button to add notes, pictures and links.</p>');
      }
      else
      {
        $(".mychunks_content").html(data['results'][0].note);
      }
      This.notes_text=data['results'][0].note;
      mychunks_updateMaxCharNum();
    }
    else
    {
      This.setStatus(0);
      mychunks_focus=0;
      This.isExist=false;
      $(".mychunks_delBtn").hide();
    }
    $(".mychunks_ftg_button").show();
    $(".mychunks_delBtn").show();
  });
}
MyChunks.prototype.save=function(v)
{
  This=this;
  var content=$(".mychunks_content");
  var note="";
  if(v)note=content.html();
  if(content.text().length<=mychunks_maxCharNum)
  {
    $(".mychunks_ftg_button").hide();
    $(".mychunks_delBtn").hide();
    var sort_key=generate_sort_key(this.chunkTitle);
    var datainfo={'info':JSON.stringify({'note':note,'user_id':this.userID,'vertical_id':this.verticalID,'courseTitle':this.courseTitle,'chunkTitle':this.chunkTitle,'course_id':this.course_id,'sort_key':sort_key,'url':this.URL})};
    $.post("/my_chunks/save_info",datainfo,function(data){
      mychunks_updateMaxCharNum();
      This.setStatus(1);
      This.isExist=true;
      This.notes_text=note;
      $(".mychunks_ftg_button").show();
      $(".mychunks_delBtn").show();
    });
    //$("#show_mychunks").hide();
    //$("#lean_overlay").hide();
    if(!v)
    {
      $("#add_mychunks").show();
      $("#lean_overlay").show();
      $(".mychunks_content").html('<p style="color:#646464">Please click the "Edit" button to add notes, pictures and links.</p>');
    }
  }
  else
  {
    if(content.text().length>mychunks_maxCharNum)
      alert('Exceed the maximum number of characters.');
  }
}
MyChunks.prototype.delete=function()
{
  This=this;
  var datainfo={'info':JSON.stringify({'user_id':this.userID,'vertical_id':this.verticalID})};
  $.post("/my_chunks/del_info",datainfo,function(data){
    $("#mychunks_course_title").html("");
    $("#mychunks_chunk_title").html("");
    $(".mychunks_content").html("");
    This.isExist=false;
    This.setStatus(0);
  });
}
MyChunks.prototype.setStatus=function(s)
{
  if(s)
  {
    $(".my_chunks_btn").css("backgroundImage","url(/static/images/chunked.png)");
  }
  else
  {
    $(".my_chunks_btn").css("backgroundImage","url(/static/images/unchuncked.png)");
  }
}
MyChunks.prototype.setNotesStatus=function(s)
{
  if(s=="edit")
  {
    this.notes_status="edit";
    $(".mychunks_ftg_button").html("Edit");
    $(".mychunks_content").attr("contenteditable","false");
    $(".mychunks_content").css("backgroundColor","#f6f6f6");
    $(".mychunks_uploadBtn").hide();
    $(".mychunks_linkBtn").hide();
  }
  else
  {
    this.notes_status="update";
    $(".mychunks_ftg_button").html("Update");
    $(".mychunks_content").attr("contenteditable","true");
    $(".mychunks_content").css("backgroundColor","#ffffff");
    $(".mychunks_uploadBtn").show();
    $(".mychunks_linkBtn").show();
    if(this.notes_text==''||this.notes_text=='<br>')
    {
      $(".mychunks_content").html('');
    }
    mychunks_updateMaxCharNum();
  }

}

var mychunks_focus=0;
var mychunks_maxCharNum=1000;
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

function get_chapter_num(str)
{
  list=str.split("\t");
  if(list.length>1)
  {
    return list[0];
  }
  else
  {
    list=str.split(" ");
    return list[0];
  }
}
function generate_sort_key(chunkTitle)
{
  var a=num_sort(chunkTitle);
  return a;
}
function num_sort(x){
    var num = x.split(":")[0];
    var r=0;
    var modulus=1000000
    if(num.indexOf(".")>=0){
      digitalArr=num.split(".");
      for(var i=0;i<digitalArr.length;i++){
          modulus/=100
          try{
            r+=parseInt(digitalArr[i])*modulus;
          }
          catch(err){
            return r;
          }
      }
      return r
    }
    else{
      return x
    }
}