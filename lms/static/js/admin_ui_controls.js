//////////////////////////////////////////////////////////////////
function GlobalTaskPanelControl(el){
  var self=this;
  el.control=this;
  this.$el=$(el);
  
  this.$toggle=this.$el.find(".task_pannel_toggle");
  this.$toggle.click(function(){
    var $content=self.$el.find(".content");
    if($content.is(":hidden")){
      $content.slideDown();
    }else{
      $content.slideUp();
    }
  });
  this.dialog=new Dialog(this.$el)
  this.dialog.hideOverlay();
  this.parseSetting();
  this.loadCount();
}
GlobalTaskPanelControl.prototype.updateProgressDialog=function(tasks){
  var self=this;
  this.$el.find(".content").html("");
  $.each(tasks,function(i,t){
    if(t.type=='import'){
      self.dialog.addProgress("Import - "+t.filename);
    }else{
      self.dialog.addProgress("Email");
    }
    self.dialog.setProgress(t.progress,i);
    if(t.progress==100){
      var $progressbar=self.dialog.getProgressBar(i);      
      if(!$progressbar.hasClass("finished")){
        $progressbar.addClass("finished");
      }
      if(self.tasks){
        var prev_progress=null;
        $.each(self.tasks,function(j,t0){
          if(t0.id==t.id && t.type==t.type){
            prev_progress=t0.progress;
          }
        });
        if(prev_progress<100 || !prev_progress)
          self.$toggle.blink({timeout:5000,delay:200});
      }
    }
  });
  this.tasks=tasks;
}
GlobalTaskPanelControl.prototype.parseSetting=function(){
  var $holder=this.$el.find("textarea.setting");
  this.setting=$.parseJSON($holder.val());
  $holder.remove();
}
GlobalTaskPanelControl.prototype.loadCount=function(){
  var self=this;
  $.get(this.setting.urls.count,function(r){
    if(r.tasks.length==0){
      self.$el.hide();
    }else{
      self.$el.show();
      self.$toggle.val(r.tasks.length+" running task"+(r.tasks.length>1?"s":""))
      self.updateProgressDialog(r.tasks);
    }
    setTimeout(function(){self.loadCount()},self.setting.interval)
  });
}
//////////////////////////////////////////////////////////////////
function FilterControl(el){
  el.control=this;
  this.filter={};
  this.$el=$(el);
  this.$body=$(el).find(".body");
  this.parseSetting();
  this.createFields();
  this.initFavorite();
}
FilterControl.prototype.parseSetting=function(){
  var $holder=this.$el.find("textarea.setting");
  this.setting=$.parseJSON($holder.val());
  $holder.remove();
}
FilterControl.prototype.initFavorite=function(){
  if(!this.setting.favorite.show) return;
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
  $.get(this.setting.favorite.urls.load,{},function(r){
    data=r;
    if((typeof data) == 'string')data=$.parseJSON(r);
    $.each(data,function(i,item){
      $("<option value='"+i+"'>"+item.name+"</option>").appendTo($drop);
    });
    $drop.val('');
  });
  $container.append("<br/>");
  $("<input type='button' class='small' value='Delete'>").appendTo($container)
    .click(function(){
      if($drop.val()){
        if(id=data[$drop.val()].id){
          self.deleteFavorite(id);
        }
      }
    });
  $("<input type='button' class='small' value='Save'>").appendTo($container)
    .click(function(){self.saveFavorite()});
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
  new Dialog($('#dialog')).showYesNo("Delete Favorite","Really delete the favorite filter selected?",function(r){
    if(r){
      $.get(self.setting.favorite.urls.remove,{'id':id},function(r){
        if((typeof r) == 'string')r=$.parseJSON(r);
        self.initFavorite();
        self.onFavoriteServerUpdated();
      });
    }
  });
}
FilterControl.prototype.onFavoriteServerUpdated=function(){
  if(fn=this.$el[0].onFavoriteServerUpdated)fn();
}
FilterControl.prototype.saveFavorite=function(){
  var self=this;
  var dialog=new Dialog($('#dialog'))
  var $content=$("<div></div>");
  $content.append("<div style='margin:0 0 15px 0'>Please entry a name of the filter.</div>");
  var $text=$("<input>").appendTo($content);
  var $save=$("<input type=button value=save >").appendTo($content);
  function showInputName(){
    $save.click(function(){
      var name=$text.val();
      if(!name){
        dialog.showButtons("Save Filter", "Invalid name.");
        return;
      }
      var exists=self.$el.find(".favorite select option").filter(function(){
        return $(this).html()==name;
      }).length>0;
      if(exists)
        dialog.showButtons(
          "Save Filter"
          , "The same name filter exists, do you want to overwrite it?"
          , ["Rename","Overwrite","Cancel"]
          , function(choice){
            if(choice==0) showInputName(); else if (choice==1) save(); else this.hide();
          });
      else
        save();
    });
    dialog.show('Save Filter',$content);
  }
  function save(){
    var name=$text.val();
    var filter=self.getFilter();
    $.get(self.setting.favorite.urls.save,{name:name,'filter':JSON.stringify(filter)},function(r){
      if((typeof r) == 'string')r=$.parseJSON(r);
      this.hide();
      self.initFavorite();
      self.onFavoriteServerUpdated();
    });
  }
  showInputName();
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
  this.$paging=$(el).find(".paging");
  this.createTable();
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
    if(f.sort){
      var order=(f.sort=='-'?'asc':'desc');
      var $arrow=$("<span class='sort'></span>").appendTo($th)
      $th.addClass("sort_head");
      $th.click(function(){
        order=(order=='asc'?'desc':'asc');
        self.sort={sortField:k,sortOrder:order};
        self.reload();
        $arrow[0].className=(order=='asc'?'sort_up':'sort_dn');
      });
    }
    if(!f.show)$th.hide();
  });
  var $thMenu=$("<th class='checkbox-col'></th>").appendTo(this.$thead)
  var $trigger=$("<span class='menu-trigger'></span>").appendTo($thMenu);
  this.createFieldsSelector($thMenu,$trigger);
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
TableControl.prototype.reload=function(){
  this.loadData(this.currentPage);
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
      var identifier=self.setting.field_row_identifier;
      $("<td><input type='checkbox' class='check-row' value='"+row[identifier]+"'/></td>").appendTo($row);
    });
    self.updatePager(r.paging);
    self.$el[0].onDataLoaded && self.$el[0].onDataLoaded();
  });
}
TableControl.prototype.getFieldCells=function(name){
  var n=0,col=0;
  $.each(this.setting.fields,function(k){
    n++;
    if(k==name){
      col=n; return false;
    }
  });
  if(col) return this.$tbody.find("tr td:nth-child("+col+")");
}
TableControl.prototype.getPagingInfo=function(){
  return this.pagingInfo;
}
TableControl.prototype.updatePager=function(info){
  var self=this;
  this.pagingInfo=info;
  this.$paging.html("");
  this.$paging.append(" Total: "+info.total+" ");
  var $input=$("<input value='"+info.page+"'>").appendTo(this.$paging);
  $input.keyup(function(e){
    if(e.keyCode==13){
      var p=$(this).val().replace(/^(\s+)|(\s+)$/,'')
      if(/^[1-9]\d*$/.test(p)){
        self.loadData(p);
      }else{
        $(this).val(info.page)
      }
    }
  });  
  $("<span>"+"/"+info.pages+"</span>").appendTo(this.$paging);
  if(info.pages>1){
    if(info.page>1){
      var $prev=$("<a href='#'>Prev</a>").appendTo(this.$paging);
      $prev.click(function(){
        self.loadData(info.page-1);
        return false;
      });
    }
    if(info.page<info.pages){
      var $next=$("<a href='#'>Next</a>").appendTo(this.$paging);
      $next.click(function(){
        self.loadData(info.page+1);
        return false;
      });
    }
  }
  var sizes=this.setting.paging.sizes;
  if(sizes && sizes.length){
    this.$paging.append(" Items Per Page ");
    var $select=$("<select></select>").appendTo(this.$paging);
    $select.change(function(){
      self.setting.paging.size=$(this).val();
      self.loadData(1);
    })
    $.each(sizes,function(i,size){
      $("<option>"+size+"</option>").appendTo($select);
    });
    $select.val(self.setting.paging.size);
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
TableControl.prototype.checkAll=function(b){
  this.$tbody.find("input.check-row").each(function(){
    this.checked=b;
  });
}
//////////////////////////////////////////////////////////////////
function Dialog(el){
  var self=this;
  this.$ei=$(el);
  this.$ei.find('.close-modal').off("click").click(function(){
    self.hide();
  });
}
Dialog.prototype.showOverlay=function(){
  if(!this.$overlay){
    this.$overlay=$("<div class='lean-overlay'></div>");
    this.$overlay.appendTo(document.body);
  }
  this.$overlay.css('display','block');
}
Dialog.prototype.hideOverlay=function(){
  if(this.$overlay){
    this.$overlay.remove();
    this.$overlay=null;
  }
}
Dialog.prototype.hide=function(){
  this.$ei.css('display','none');
  this.hideOverlay();
}
Dialog.prototype.setTitle=function(title){
  this.$ei.find('.dialog-title').html(title);
}
Dialog.prototype.setContent=function(content){
  this.$ei.find('.content').html("");
  this.$ei.find('.content').append(content);  
}
Dialog.prototype.showYesNo=function(title,content,callback){
  var self=this;
  this.show(title,content);
  var $content=this.$ei.find('.content');
  var $buttons=$("<div></div>").appendTo($content)
  $("<input type='button' value='Yes'>").appendTo($buttons).click(function(){
    callback.apply(self,[true]);
  });
  $("<input type='button' value='No'>").appendTo($buttons).click(function(){
    callback.apply(self,[false]);
  });
}
Dialog.prototype.showProgress=function(title,content,name){
  var self=this;
  this.show(title,content);
  this.addProgress(name);
}
Dialog.prototype.addProgress=function(name){
  var self=this;
  name=name?name+": ":"";
  var $content=this.$ei.find('.content');
  var $progress=$("<div class='progressbar'>\
<div class='progressbar_text'>\
<span>"+name+"</span>\
<span class='progressbar_perc'></span></div>\
<div class='progressbar_flow'></div></div>").appendTo($content);
  function set($p,percent){
    $p.find(".progressbar_perc").text(percent+"%")
    $p.find(".progressbar_flow").css('width',percent+'%');
  }
  this.setProgress=function(percent,id){
    set(self.getProgressBar(id),percent);
  }
  this.getProgressBar=function(id){
    if(typeof id=='undefined')id=0;
    var ret=$content.find(".progressbar").eq(id);
    return ret;
  }
  set($progress,0);
}
Dialog.prototype.showButtons=function(title,content,labels,callback){
  var self=this;
  this.show(title,content);
  var $content=this.$ei.find('.content');
  var $buttons=$("<div></div>").appendTo($content)
  $.each(labels,function(i,label){
    $("<input type='button' value='"+label+"'>").appendTo($buttons).click(function(){
      callback.apply(self,[i]);
    });  
  });
}
Dialog.prototype.show=function(title,content){
  var self=this;
  this.showOverlay();
  this.setTitle(title);
  this.setContent(content);
  this.$ei.fadeIn(200);
}
Dialog.prototype.isOn=function(){
  return !this.$ei.is(":hidden");
}
//////////////////////////////////////////////////////////////////
function ContextMenu($container,$trigger){
  var self=this;
  this.$container=$("<ul class='context-menu'></ul>").appendTo($container);
  $(document).on('click', function(event) {
    if (!$(event.target).hasClass('menu-trigger') && !$(event.target).closest(".context-menu").length) {
      $(".context-menu").hide();
    }
  });
  $trigger.click(function(){
    self.toggle();
  });
}
ContextMenu.prototype.createItem=function($el){
  var $li=$("<li></li>").appendTo(this.$container);
  $li.append($el);
}
ContextMenu.prototype.toggle=function(){
  this.$container.toggle();
}
