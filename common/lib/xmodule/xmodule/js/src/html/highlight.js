$(function () {
  //  $(".xmodule_HtmlModule").each(function(){
  //     if($(this).find(".edu_highlight"))
  //     {
  //       var hl = new Highlight();
  //       hl.init($(this).find(".edu_highlight"));
  //     }
  // });

});
Highlight=function()
{
  this.ajax_url="";
  this.wordItem=[];
  this.data={};
  this.width=600;
  this.toolBar=$("<span class='highlight_toolBar' style='display:block;background:#D4D0C8;width:300px;margin:20px;padding:6px;-moz-border-radius: 15px;-webkit-border-radius: 15px;border-radius:15px;'/>");
  this.content=[];
  this.annotation=null;
  this.currBlock=null;
}
Highlight.prototype.init=function(element)
{
  var wordArr=[];
  var htmlcon="";
  this.width=element.attr('width')||'100%';
  this.ajax_url = element.parent().data('url');
  htmlcon=element.html();
  element.width(this.width);
  //element.empty();
  element.prepend(this.toolBar);
  _this=this;
  element.find('div').each(function(i){
    if($(this).html()==null)
    {
      wordArr[i] = $(this).text().sTrim().split(" ");
    }
    else
    {
      wordArr[i] = $(this).html().toString().sTrim().split(" ");
    }
    
    _this.content[i]=$("<div class='highlight_content' style='float:left;'/>");
    $(this).html(_this.content[i]);
    $(this).append($("<div style='clear:both;'/>"));
  });
  //element.append($("<div style='clear:both;'/>"));

  this.annotation = new Highlight_Annotation();
  this.annotation.init(element);
  htb = new Highlight_ToolBar();
  htb.init(this.toolBar,this,this.annotation);
  for(var i=0;i<wordArr.length;i++)
  {
    this.wordItem[i]=[];
    for(var j=0;j<wordArr[i].length;j++)
    {
      if(wordArr[i][j]!="" && wordArr[i][j]!=" ")
      {
        this.wordItem[i][j] = new Highlight_Block();
        this.wordItem[i][j].init(this,wordArr[i][j],htb,this.annotation);
        this.content[i].append(this.wordItem[i][j].element);
      }
    }
  }
  this.getData();
}
Highlight.prototype.save=function()
{
  this.data={};
  this.data.group=[];
  if(this.currBlock!=null)
    this.currBlock.annotationData=this.annotation.getContent();
  for(var i=0;i<this.wordItem.length;i++)
  {
    this.data.group[i]=[];
    for(var j=0;j<this.wordItem[i].length;j++)
    {
      if(this.wordItem[i][j].status)
      {
        this.data.group[i].push({"index":j,"color":this.wordItem[i][j].color,"annotation":this.wordItem[i][j].annotationData});
      } 
    }
  }
  this.updateData(JSON.stringify(this.data));
}
Highlight.prototype.updateData=function(data)
{
   var fd = new FormData();
   fd.append('highlight_data', data);
   var settings = {
      type: "POST",
      data: fd,
      processData: false,
      contentType: false,
      async: false,
      success: function(response) {
        alert("Successfully saved!");
      }
    };
    return $.ajaxWithPrefix("" + this.ajax_url+ "/update_highlight", settings);
}
Highlight.prototype.updateBlockInfo=function()
{
   for(var i=0;i<this.data.group.length;i++)
   {  
      for(var j=0;j<this.data.group[i].length;j++)
      {
        this.wordItem[i][this.data.group[i][j].index].setColor(this.data.group[i][j].color);
        this.wordItem[i][this.data.group[i][j].index].annotationData=this.data.group[i][j].annotation||'';
      }
   }

}
Highlight.prototype.getData=function()
{
  _this=this;
  var fd = new FormData();
  fd.append('highlight_data', '');
  var settings = {
      type: "POST",
      data: fd,
      processData: false,
      contentType: false,
      async: false,
      success: function(response) {
        if(response.data!="")
        {
          _this.data= eval('(' + response.data + ')');
          _this.updateBlockInfo();
        }
      }
    };
   return $.ajaxWithPrefix("" + this.ajax_url+ "/get_highlight", settings);
}
//--------------------------------------------------------------------

Highlight_Block=function()
{
  this.element=null;
  this.status=0;
  this.index=0;
  this.color="#8656cc";
  this.annotation=null;
  this.annotationData="";
}
Highlight_Block.prototype.init=function(highlight,word,toolbar,annotation)
{
  this.element=$("<div style='float:left;word-wrap:break-word;width:auto;height:auto;margin:2px;-moz-user-select:none;-khtml-user-select:none;user-select:none;cursor:pointer;'></div>");
  this.element.html(word);
  this.element[0].obj=this;
  this.annotation=annotation;
  this.element.click(function(){
    if(highlight.currBlock!=null)
    highlight.currBlock.annotationData=annotation.getContent();
    highlight.currBlock=this.obj;
    if(!this.obj.annotation.active)
    {
      if(!this.obj.status){
        this.obj.setColor(toolbar.selectColor);
      }
      else
      {
        this.obj.clear();
      }
    }
    else
    {
      if(this.obj.status)
      {
        this.obj.annotation.show();
        this.obj.annotation.setTitle($(this).text()+":");
        this.obj.annotation.setContent(this.obj.annotationData);
      }
    }
  });
}
Highlight_Block.prototype.setColor=function(color)
{
  this.color=color;
  this.status=1;
  if(this.color=="U")
  {
    this.element.css("textDecoration","underline");
  }
  else
  {
    this.element.css("backgroundColor",this.color);
  }
  
}
Highlight_Block.prototype.clear=function()
{
  this.status=0;
  //this.annotationData="";
  this.element.css("backgroundColor","");
  this.element.css("textDecoration","none");
}
Highlight_Block.prototype.getColor=function()
{
  return this.color;
}
Highlight_Block.prototype.treatMathjax=function(word)
{
  if(word.indexOf("mathjaxinline")!=-1)
  {
    var height=this.element.find("svg").css("height");
    this.element.css("height",height);
  }
}
//--------------------------------------------------------------------
Highlight_ToolBar=function()
{
  this.element=null;
  this.colorItem=[];
  this.color=["#0fff00","#ffff00","#ff9933","#00ffff","U"];
  this.selectColor=this.color[0];
  this.saveButton=null;
  this.annotationButton=null;
  this.annotation=null;
}
Highlight_ToolBar.prototype.init=function(element,highlight,annotation)
{
  for(var i=0;i<this.color.length;i++)
  {
    this.colorItem[i] = $("<div style='float:left;width:30px;height:30px;border:1px solid #000;cursor:pointer;margin:4px;'/>");
    if(this.color[i]=="U")
    {
       this.colorItem[i].text(this.color[i]);
       this.colorItem[i].css("textAlign","center");
       this.colorItem[i].css("textDecoration","underline");
       this.colorItem[i].css("backgroundColor","#ffffff");
    }
    else
    {
      this.colorItem[i].css("backgroundColor",this.color[i]);
    }
    this.annotation = annotation;
    this.colorItem[i][0].obj=this;
    element.append(this.colorItem[i]);
    this.colorItem[i].click(function(){
      if($(this).text()=="U")
      {
        this.obj.selectColor = "U";
      }
      else
      {
        this.obj.selectColor = $(this).css("backgroundColor");
      }
    });
    
  }
  /*-------------------------annotate provisional hide
  this.annotationButton=$("<div class='annotation_btn icon-comment' style='background:#FFFFFF;width:30px;height:30px;color:#999999;border:1px solid #000;float:left;cursor:pointer;margin:4px;text-align:center;'></div>");
  element.append(this.annotationButton);
  this.annotationButton[0].obj=this;
  this.annotationButton.click(function(){
    if(this.obj.annotation.active)
    {
      this.obj.annotation.active=false;
      this.obj.annotation.hide();
      $(this).css("color","#999999");
    }
    else
    {
      this.obj.annotation.active=true;
      $(this).css("color","#333333");
    }
    });
 ------------------------------------------------------*/
  this.saveButton=$("<div class='button-edu orange' style='float:left;cursor:pointer;margin:4px;text-align:center;'>Save</div><div style='clear:both;'></div>");
  element.append(this.saveButton);
  this.saveButton.click(function(){
    highlight.save();
    });
}
Highlight_Annotation=function()
{
  this.element=null;
  this.title=null;
  this.content=null;
  this.active=false;
}
Highlight_Annotation.prototype.init=function(element)
{
  this.element=$("<div class='annotation-container' style='margin-top:10px;'><div class='annotation-title' style='font-weight:bold;'></div><textarea class='annotation-content' style='width:400px;height:100px;'></textarea></div>");
  this.title=this.element.find('.annotation-title');
  this.content=this.element.find('.annotation-content');
  element.append(this.element);
  this.hide();
}
Highlight_Annotation.prototype.setTitle=function(value)
{
  this.title.text(value)
}
Highlight_Annotation.prototype.setContent=function(value)
{
  this.content.val(value);
}
Highlight_Annotation.prototype.getContent=function()
{
  return this.content.val();
}
Highlight_Annotation.prototype.show=function()
{
  this.element.show();
}
Highlight_Annotation.prototype.hide=function()
{
  this.element.hide()
}
//--------------------------------------------------------------------
String.prototype.sTrim = function() 
{ 
  return this.replace(/(^\s*)|(\s*$)/g, ""); 
}