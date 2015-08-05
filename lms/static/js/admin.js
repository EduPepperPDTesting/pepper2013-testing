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
  this.$el.find(".favorite").remove();
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
  $delete.click(function(){
    if($drop.val()){
      if(id=data[$drop.val()].id){
        self.deleteFavorite(id);
      }
    }
  });
  var $save=$("<input type='button' class='small' value='Save'>").appendTo($container);
  $save.click(function(){self.saveFavorite()});
}
FilterControl.prototype.onFavoriteChange=function(filterItem){
  var self=this;
  this.filter=$.parseJSON((filterItem && filterItem.filter)||"{}");
  $.each(this.setting.fields,function(k,f){
    self.getFieldArea(k).val("")
    if(f.type=='drop')
      self.clearDropItems(self.getFieldArea(k));
  });
  $.each(this.setting.fields,function(k,f){
    var value=self.filter[k];
    self.getFieldArea(k).val(value)
    if(f.type=='drop')
      self.loadDropItems(self.getFieldArea(k));
  });
}
FilterControl.prototype.deleteFavorite=function(id){
  var self=this;
  new Dialog($('#dialog')).yesNo("Delete Favorite","Really delete the favorite filter selected?",function(r){
    if(r){
      $.get(self.setting.urls.favorite_delete,{'id':id},function(r){
        if((typeof r) == 'string')r=$.parseJSON(r);
        self.createFavorite();
      });
    }
  });
}
FilterControl.prototype.saveFavorite=function(){
  var self=this;
  var $content=$("<div></div>")
  $content.append("<div style='margin:0 0 15px 0'>Please entry a name of the filter.</div>");
  var $text=$("<input>").appendTo($content);
  var $save=$("<input type=button value=save >").appendTo($content);
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
  var n=0;
  $.each(this.setting.fields,function(k,f){
    if(f.type=="drop"){
      var $drop=$("<select name='"+k+"'><option value=''>Select "+f.display+"</option></select>").appendTo(self.$body);
      $drop.change(function(){
        self.onDropChanged($drop);
      });
    }else if(f.type=="text"){
      var $text=$("<input name='"+k+"' placeholder='"+f.display+"'/>").appendTo(self.$body);
    }
    self.getFieldArea(k).css('width','250px');
    if(++n%3==0)self.$body.append("<br>")
  });
  $.each(this.setting.fields,function(k,f){
    if(f.type=="drop" && !f.require.length){
      self.loadDropItems(self.getFieldArea(k));
    }
  });
}
FilterControl.prototype.getFieldArea=function(name){
  return this.$el.find("*[name="+name+"]");
}
FilterControl.prototype.getDropLoadingArgs=function($drop){
  var self=this;
  var data={};
  $.each(this.setting.fields[$drop.prop('name')].require,function(i,name){
    data[name]=self.getFieldArea(name).val();
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
    self.filter[name]="";
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
    if(f.type=="drop" && f.require.indexOf(name)>-1){
      fn(self.getFieldArea(k));
    }
  });
}
FilterControl.prototype.getFilter=function(){
  var self=this;
  var data={};
  $.each(this.setting.fields,function(k){
    data[k]=self.getFieldArea(k).val();
  });
  return data;
}
//////////////////////////////////////////////////////////////////
function TableControl(el){
  el.control=this;
  this.$el=$(el);
  this.parseSetting();
  this.sort={};
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
  var self=this;
  this.$table=$("<table></table>").appendTo(this.$body);
  this.$thead=$("<tr></tr>").appendTo(this.$table);
  this.$tbody=$("<tbody></tbody>").appendTo(this.$table);
  $.each(this.setting.fields,function(k,f){
    var $th=$("<th class='clearfix'>"+f.display+"</th>").appendTo(self.$thead);
    var order='';
    $("<span class='sort'></span>").appendTo($th).click(function(){
      order=(order=='asc'?'desc':'asc');
      self.sort={sortField:k,sortOrder:order};
      self.loadData(self.currentPage);
    });
    if(!f.show)$th.hide();
  });
  var $thMenu=$("<th class='checkbox-col'></th>").appendTo(this.$thead)
  var $button=$("<span></span>").appendTo($thMenu);
  this.createFieldsSelector($thMenu,$button);
}
TableControl.prototype.createFieldsSelector=function($container,$button){
  var self=this;
  var items=[];
  this.fieldsSelector=new ContextMenu($container,$button)
  $.each(this.setting.fields,function(k,f){
    var $el=$("<label></label>");
    self.fieldsSelector.createItem($el);
    $("<input type='checkbox' "+(f.show?'checked':'')+"/>").appendTo($el).click(function(){
      self.toggleColumn(k);
    });
    $el.append(" "+f.display);
  });
}
TableControl.prototype.toggleColumn=function(name){
  var self=this;
  var n=0;
  this.setting.fields[name].show=!this.setting.fields[name].show;
  $.each(this.setting.fields,function(k,f){
    if(k==name){
      self.$thead.find("th").eq(n).toggle();
      console.log(self.$tbody.find("tr td:nth-child("+n+")").length)
      self.$tbody.find("tr td:nth-child("+(n+1)+")").toggle();
    }
    n++;
  });
}
TableControl.prototype.createFooter=function(){
  this.$footer=$("<div class='paging'></div>").appendTo(this.$body);
}
TableControl.prototype.loadData=function(page){
  this.currentPage=page;
  var self=this;
  var args={size:this.setting.paging.size,page:page};
  var args=$.extend(args,this.filter,this.sort);
  $.get(this.setting.urls.data,args,function(r){
    if((typeof r) == 'string')r=$.parseJSON(r);
    self.$tbody.html(""); 
    $.each(r.rows,function(i,row){
      var $row=$("<tr></tr>").appendTo(self.$tbody);
      $.each(self.setting.fields,function(k,f){
        var $td=$("<td>"+row[k]+"</td>").appendTo($row);
        if(!f.show)$td.hide();
      });
      $("<td><input type='checkbox' class='check-row' value='"+row.id+"'/></td>").appendTo($row);
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
TableControl.prototype.getCheckedValues=function(){
  var ar=[];
  this.$tbody.find("input.check-row").each(function(){
    if(this.checked) ar.push(this.value)
  });
  return ar;
}
//////////////////////////////////////////////////////////////////
function Dialog(el){
  this.$dialog=$(el);
}
Dialog.prototype.showOverlay=function(){
  this.$overlay=$("<div class='lean-overlay'></div>");
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
Dialog.prototype.yesNo=function(title,content,callback){
  var self=this;
  this.show(title,content);
  var $content=this.$dialog.find('.content');
  var $buttons=$("<div></div>").appendTo($content)
  $("<input type='button' value='Yes'>").appendTo($buttons).click(function(){
    self.hide();
    callback(true);
  });
  $("<input type='button' value='No'>").appendTo($buttons).click(function(){
    self.hide();
    callback(false);
  });
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
function ContextMenu($container,$button){
  var self=this;
  this.$container=$("<ul class='context-menu'></ul>").appendTo($container);
  $(document).on('click', function(event) {
    if (!$(event.target).is($button[0]) && !$(event.target).closest(".context-menu").length) {
      $(".context-menu").hide();
    }
  });
  $button.click(function(){self.toggle()});
}
ContextMenu.prototype.createItem=function($el){
  var $li=$("<li></li>").appendTo(this.$container);
  $li.append($el);
}
ContextMenu.prototype.toggle=function(){
  this.$container.toggle();
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
