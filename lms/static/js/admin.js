function FilterControl(el){
  el.control=this;
  this.filter={};
  this.$el=$(el);
  this.$body=$(el).find(".body");
  this.parseSetting();
  this.createFields();
  this.createFavorite();
}
FilterControl.prototype.parseSetting=function(){
  var $holder=this.$el.find("textarea.setting");
  this.setting=$.parseJSON($holder.val());
  $holder.remove();
}
FilterControl.prototype.createFavorite=function(){
  var self=this;
  this.$el.addClass("clearfix");
  var $container=$("<div class='favorite'></div>").appendTo(this.$el);
  $container.css('float','right');
  var $drop=$("<select><option value=''></option></select>").appendTo($container);
  var data=[]
  $drop.change(function(){
    self.onFavoriteChange(data[$(this).val()]);
  });
  $.get(this.setting.urls.favorite_load,{},function(r){
    data=r;
    if((typeof data) == 'string')data=$.parseJSON(r);
    $.each(data,function(i,item){
      $("<option value='"+i+"'>"+item.name+"</option>").appendTo($drop);
    });
  });
  $container.append("<br/>");
  var $delete=$("<input type='button' class='small' value='Delete'>").appendTo($container);
  $delete.click(function(){self.deleteFavorite($(this).val())});
  var $save=$("<input type='button' class='small' value='Save'>").appendTo($container);
  $save.click(function(){self.saveFavorite()});
}
FilterControl.prototype.onFavoriteChange=function(filterItem){
  var self=this;
  this.filter=$.parseJSON((filterItem && filterItem.filter)||"{}");
  //** clear all
  $.each(this.setting.fields,function(k,f){
    if(f.require.length)
      self.clearDropItems(self.getDrop(k));
    else
      self.getDrop(k).val('');
  });
  //** load all (if required ready)
  $.each(this.filter,function(k,v){
    self.loadDropItems(self.getDrop(k));
  });
}
FilterControl.prototype.deleteFavorite=function(id){
  $.get(this.setting.urls.favorite_delete,{'id':id},function(r){
    if((typeof r) == 'string')r=$.parseJSON(r);
  });
}
FilterControl.prototype.saveFavorite=function(){
  var self=this;
  var $content=$("<div></div>")
  $content.append("Please entry a name of the filter.<br>");
  var $text=$("<input>").appendTo($content);
  var $save=$("<input type=button value=save>").appendTo($content);
  var dialog=new Dialog($('#dialog'))
  dialog.show('Save Filter',$content);
  $save.click(function(){
    var filter=self.getFilter();
    $.get(self.setting.urls.favorite_save,{name:$text.val(),'filter':JSON.stringify(filter)},function(r){
      if((typeof r) == 'string')r=$.parseJSON(r);
      dialog.hide();
    });
  });
}
FilterControl.prototype.createFields=function(){
  var self=this;
  $.each(this.setting.fields,function(k,f){
    var Name=k.replace(/^\w/,function(s){return s.toUpperCase()});
    var $drop=$("<select name='"+k+"'><option value=''>Select "+Name+"</option></select>").appendTo(self.$body);
    $drop.change(function(){
      self.onDropChanged($drop);
    });
  });
  $.each(this.setting.fields,function(k,f){
    if(!f.require.length){
      self.loadDropItems(self.getDrop(k));
    }
  });
}
FilterControl.prototype.getDrop=function(name){
  return this.$el.find("select[name="+name+"]");
}
FilterControl.prototype.getDropLoadingArgs=function($drop){
  var self=this;
  var data={};
  $.each(this.setting.fields[$drop.prop('name')].require,function(i,name){
    data[name]=self.getDrop(name).val();
    if(data[name]==''){
      data=null;
      return false;
    }
  });
  return data;
}
FilterControl.prototype.formatOption=function(s,item){
  return s.replace(/\{(\w+)\}/g,function(s0,s1){
    return item[s1];
  });
}
FilterControl.prototype.clearDropItems=function($drop){
  var self=this;
  $drop.find("option").filter(
    function(){return this.getAttribute("value")!=""}
  ).remove();
  this.callByRequire($drop.prop('name'),function($d){
    self.clearDropItems($d);
  });
}
FilterControl.prototype.loadDropItems=function($drop){
  var self=this;
  this.clearDropItems($drop);
  var name=$drop.prop('name');
  var f=this.setting.fields[name];
  var args=this.getDropLoadingArgs($drop);
  if(!args)return;
  $.get(f.url,args,function(r){
    if((typeof r) == 'string')r=$.parseJSON(r);
    $.each(r,function(i,item){
      $drop.append(self.formatOption(f.format,item));
    });
    var fv=self.filter[name];
    if(fv!==undefined && fv!=""){
      $drop.val(fv);
      $drop.change();
    }
  });
}
FilterControl.prototype.onDropChanged=function($drop){
  var self=this;
  var f=this.setting.fields[$drop.prop('name')];
  this.callByRequire($drop.prop('name'),function($d){
    self.loadDropItems($d);
  });
}
FilterControl.prototype.callByRequire=function(name,fn){
  var self=this;
  $.each(this.setting.fields,function(k,f){
    if(f.require.indexOf(name)>-1){
      fn(self.getDrop(k));
    }
  });
}
FilterControl.prototype.getFilter=function(){
  var self=this;
  var data={};
  $.each(this.setting.fields,function(k){
    data[k]=self.getDrop(k).val();
  });
  return data;
}
//////////////////////////////////////////////////////////////////
function TableControl(el){
  el.control=this;
  this.$el=$(el);
  this.parseSetting();
  this.$body=$(el).find(".body");
  this.createTable();
  this.createFooter();
  this.loadData(1);
}
TableControl.prototype.parseSetting=function(){
  var $holder=this.$el.find("textarea.setting");
  this.setting=$.parseJSON($holder.val());
  $holder.remove();
}
TableControl.prototype.createTable=function(){
  this.$table=$("<table></table>").appendTo(this.$body);
  var $head=$("<tr></tr>").appendTo(this.$table);
  this.$tbody=$("<tbody></tbody>").appendTo(this.$table);
  $.each(this.setting.fields,function(k,f){
    $("<th>"+f.display+"</th>").appendTo($head);
  });
  $("<th class='checkboxCol'>M</th>").appendTo($head);
}
TableControl.prototype.createFooter=function(){
  this.$footer=$("<div class='paging'></div>").appendTo(this.$body);
}
TableControl.prototype.loadData=function(page){
  var self=this;
  var args={size:this.setting.paging.size,page:page}
  var args=$.extend(args,this.filter)
  $.get(this.setting.urls.data,args,function(r){
    if((typeof r) == 'string')r=$.parseJSON(r);
    self.$tbody.html(""); 
    $.each(r.rows,function(i,row){
      var $row=$("<tr></tr>").appendTo(self.$tbody);
      $.each(self.setting.fields,function(k){
        $("<td>"+row[k]+"</td>").appendTo($row);
      });
      $("<td><input type='checkbox'/></td>").appendTo($row);
    });
    self.updatePager(r.paging);
  });
}
TableControl.prototype.updatePager=function(info){
  var self=this;
  this.$footer.html("");
  var $input=$("<input value='"+info.page+"'>").appendTo(this.$footer);
  $input.keyup(function(e){
    if(e.keyCode==13){
      var p=$(this).val().replace(/^(\s+)|(\s+)$/,'')
      if(/^[1-9]\d*$/.test(p)){
        self.loadData(p);
      }else{
        alert("Invalid page number '"+p+"'")
      }
    }
  });  
  $("<span>"+"/"+info.pages+"</span>").appendTo(this.$footer);
  if(info.pages>1){
    if(info.page>1){
      var $prev=$("<a href='#'>Prev</a>").appendTo(self.$footer);
      $prev.click(function(){
        self.loadData(info.page-1);
        return false;
      });
    }
    if(info.page<info.pages){
      var $next=$("<a href='#'>Next</a>").appendTo(self.$footer);
      $next.click(function(){
        self.loadData(info.page+1);
        return false;
      });
    }
  }
}
TableControl.prototype.updateFilter=function(f){
  this.filter=f;
  this.loadData(1);
}
//////////////////////////////////////////////////////////////////
function Dialog(el){
  this.$dialog=$(el);
}
Dialog.prototype.showOverlay=function(){
  this.$overlay=$("<div class='lean_overlay'></div>");
  this.$overlay.appendTo(document.body);
  this.$overlay.css('display','block');
}
Dialog.prototype.hideOverlay=function(){
  this.$overlay.remove();
}
Dialog.prototype.hide=function(){
  this.$dialog.css('display','none');
  this.hideOverlay();
}
Dialog.prototype.setTitle=function(title){
  this.$dialog.find('.dialog-title').html(title);
}
Dialog.prototype.setContent=function(content){
  this.$dialog.find('.content').html("");
  this.$dialog.find('.content').append(content);  
}
Dialog.prototype.show=function(title,content){
  var self=this;
  this.showOverlay();
  this.setTitle(title);
  this.setContent(content);
  this.$dialog.find('.close-modal').click(function(){
    self.hide();
  });
  this.$dialog.fadeIn(200);
}
//////////////////////////////////////////////////////////////////
var userData={}
userData.$form=$("#filter_form");
userData.submit=function(form){
  var self=this
  var form=this.$form[0];
  // input checking
  var state_id=$(form.state_id).val();
  var district_id=$(form.district_id).val();
  if(!state_id || !district_id){
    new Dialog($('#dialog')).show('Error','You must select a State, District and file to import.');
    return false;
  }
  if(!((/\.csv/i).test(form.file.value))){
    new Dialog($('#dialog')).show('Error','Please select a CSV file.');
    return false;
  }    
  // submit
  var fd = new FormData(form);    
  $.ajax({
    url: "/configuration/import_user_submit/",
    data: fd,
    processData: false,
    contentType: false,
    type: 'POST',
    enctype: 'multipart/form-data',
    mimeType: 'multipart/form-data',
    success: function(data){
      self.renderProgress(data.taskId);
    }
  });
}
userData.renderProgress=function(taskId){
  var dialog=new Dialog($('#dialog'));
  dialog.show('User Data Import',"<span class='progressinfo'></span> <div class='progressbar'><div class='progressbar_flow'></div></div>");
  (function getStatus(){
    setTimeout(function(){
      $.post("/configuration/task_status/",{taskId:taskId},function(r){
        dialog.setTitle();
        $(".modal .progressbar_flow").css('width',r.precent+'%');
        if(r.precent<100){
          $(".modal .progressinfo").html('importing users...<br>'+Math.round(r.precent)+'%');
          getStatus();
        }else{
          dialog.setContent("<p style='font-size:20px;font-weight:bold;'>Import Complete</p><br>If there were any errors, you will receive them in an email.");
        }
      });
    },1000);
  })();
}
userData.bindEvents=function(){
  var self=this;
  this.$form.submit(function(){
    self.submit();
    return false;
  });
}
userData.bindEvents();
$(".expand_title").click(function(){
  var $div=$(this).next("div.expand_div");
  if($div.is(':visible')){
    $div.hide();
    $(this).removeClass('expand_title_expanded');
  }else{
    $div.show();
    $(this).addClass('expand_title_expanded');
  }
});
