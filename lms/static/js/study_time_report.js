var study_time_content_isload = false;
var study_time_content_loadNum = 0;
var study_time_content_totalNum = 0;
var cur_course_id = "";
$(function() {
  study_time_content_update(study_time_content_loadNum);
  $(".top_btn").click(function() {
    $(window).scrollTop(0);
  })
  $(".top_btn").mouseover(function() {
    $(this).find('.top_btn_img_1').hide();
    $(this).find('.top_btn_img_2').show();
  })
  $(".top_btn").mouseout(function() {
    $(this).find('.top_btn_img_1').show();
    $(this).find('.top_btn_img_2').hide();
  })
  $(window).bind("scroll", function() {
    var scrollTop = $(this).scrollTop();　　
    var scrollHeight = $(document).height();　　
    var windowHeight = $(this).height();
    if ((scrollTop + windowHeight == scrollHeight) && study_time_content_isload) {
      study_time_content_loadNum = $(".vertical_title").length;
      study_time_content_update(study_time_content_loadNum);
    }
  })
})

function study_time_content_update(skip) {
  study_time_content_isload = false;
  $(".loadInfo").text("Loading ...");
  $(".loadInfo").show();
  $.post("/study_time/get_info_range", {
    skip: skip,
    limit: 20
  }, function(data) {
    study_time_content_init(data)
  });
}

function study_time_content_init(data) {
  study_time_content_totalNum = data.count;
  for (var i = 0; i < data.results.length; i++) {
    study_time_content_createItem(data.results[i]);
  }
  if (study_time_content_loadNum >= study_time_content_totalNum) {
    study_time_content_isload = false;
    if (study_time_content_totalNum > 0) {
      $(".loadInfo").text("You have reached the end of the record.");
    } else {
      $(".loadInfo").text("You have not started to learn, so there is no record.");
    }
    $(".loadInfo").show();
  } else {
    study_time_content_isload = true;
    $(".loadInfo").hide();
  }

  if ($(window).scrollTop() > 0) {
    $(".top_btn").show();
  }

}

function study_time_content_createItem(data) {
  var idArr = data.location.split("/");
  var data_id = idArr[0] + "/" + idArr[1];
  var data_course_id = idArr[0] + "/" + idArr[1] + "/" + idArr[2];
  var ele = $('<div style="padding-bottom:20px;" class="vertical_info"><table cellspacing="10"><tr><td style="padding-top:15px;"><div style="width:280px; height:100px; background:url(/c4x/' + data_id + '/asset/course_author_img.jpg);background-repeat:no-repeat;"/></td><td style="vertical-align:middle;"><div class="course_title"><b>Course:</b> ' + data.course_name + '</div><div class="course_title"><b>Discussion:</b> ' + study_time_format(data.discussion_time) + '</div><div class="course_title"><b>Portfolio:</b> ' + study_time_format(data.portfolio_time) + '</div><div class="course_title"><b>External Course Time:</b> ' + study_time_format(data.external_time) + '</div></td></tr><tr><td width="400" style="padding-top:15px;"><b>Chapter:</b></td><td style="padding-top:15px;"><b>Studying time:</b></td></tr></table></div>');
  element = $('<div style="padding-bottom:20px;" course-id="' + data_course_id + '"><table><tr><td width="400"><div><a class="vertical_title" course_title="' + data.course_name + '" href="/courses/' + data.location + '">' + data.vertical_name + '</a></div></td><td><div class="timeItem" data-id="' + data.vertical_id + '">' + study_time_format(data.time) + '</div></td></tr></table><hr/></div>');
  if (cur_course_id == "" || cur_course_id != data_course_id || $("div[course-id=" + "'" + data_course_id + "'" + "]").length < 1) {
    cur_course_id = data_course_id;
    $('.study_time_container').append(ele);
  }
  $('.study_time_container').append(element);
}

function study_time_padding(v) {
  if (v.toString().length <= 1) return '0' + v;
  return v;
}

function study_time_format(t) {
  var hour = study_time_padding(Math.floor(t / 60 / 60));
  var minute = study_time_padding(Math.floor(t / 60 % 60));
  var second = study_time_padding(Math.floor(t % 60));
  return hour + ":" + minute + ":" + second;
}