ToggleBar=function()
{
    this.status=-1;
    this.title=null;
    this.content=null;
    this.width=600;
    this.color="#F4F4F4";
}
ToggleBar.prototype.init=function(element)
{
    this.title=$(element.find("div")[0]);
    this.content=$(element.find("div")[1]);
    this.width=element.attr("width")||this.width;
    this.color=element.attr("color")||this.color;
    this.title.css("fontSize","1.1em");
    this.title.css("fontWeight","bold");
    this.title.css("marginBottom","5px");
    element.css("margin","5px 0px 40px 5px");
    element.css("width",this.width);
    this.title.css("background",this.color);
    this.content.css("background",this.color);
    this.title.css("padding","10px");
    this.content.css("padding","10px");
    this.content.hide();
    this.title.append("<a href='javascript:void(0)' class='edx_toggle_button' style='float:right;fontWeight:bold;'>+ open</a>");
    this.title.find(".edx_toggle_button")[0].obj=this;
    this.title.find(".edx_toggle_button").click(function(event) {
        this.obj.status*=-1;
        if(this.obj.status>0)
        {
            this.obj.content.show();
            $(this).html("- close");
        }
        else
        {
            this.obj.content.hide();
            $(this).html("+ open");
        }
      
    });
}
$(function () {
   // var edu_tb_element=$('body').find('.edu_toggle_bar');
   // for(var i=0;i<edu_tb_element.length;i++)
   // {
   //      var edu_tb = new ToggleBar();
   //      edu_tb.init($(edu_tb_element[i]));

   // }
});