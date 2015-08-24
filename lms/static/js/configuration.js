//////////////////////////////////////////////////////////////////
$(".expand_title").click(function(){
  var $div=$(this).next("div.expand_div");
  if($div.is(':visible')){
    $div.slideUp("slow"); 
    $(this).removeClass("expand_title_expanded");
  }else{
    $div.slideDown("slow");
    $(this).addClass("expand_title_expanded");
  }
});
//////////////////////////////////////////////////////////////////
TableControl.prototype.createTable=function(){
  var self=this;
  this.$table=$("<table></table>").appendTo(this.$body);
  this.$head=$("<thead></thead>").appendTo(this.$table);
  this.$thead=$("<tr></tr>").appendTo(this.$head);
  this.$tbody=$("<tbody></tbody>").appendTo(this.$table);
  $.each(this.setting.fields,function(k,f){
    var $th=$("<th class='clearfix'>"+f.display+"</th>").appendTo(self.$thead);
    if(f.sort){
      var order=(f.sort=='-'?'asc':'desc');
      $("<span class='sort'></span>").appendTo($th).click(function(){
        order=(order=='asc'?'desc':'asc');
        self.sort={sortField:k,sortOrder:order};
        self.reload();
      });
    }
    if(!f.show)$th.hide();
  });
  var $thMenu=$("<th class='checkbox-col'></th>").appendTo(this.$thead)
  var $trigger=$("<span class='menu-trigger'></span>").appendTo($thMenu);
  this.createFieldsSelector($thMenu,$trigger);
}
String.prototype.replaceAll = function(s1,s2){
　return this.replace(new RegExp(s1,"gm"),s2);
}