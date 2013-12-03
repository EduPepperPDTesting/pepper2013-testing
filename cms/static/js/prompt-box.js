function PromptBox(Container,width)
{
	_width=width||240;
	this.source={};
	this.con=$("."+Container);
	this.con.css("position","relative");
	this.box=$("<div style='padding:10px;position:absolute;left:0px;top:0px;width:"+_width+"px;border:1px solid #000;background:#b1fdfd;word-wrap:break-word'>000</div>");
	this.con.append(this.box);
	this.box.hide();

}
PromptBox.prototype.binding=function(name,text,x,y)
{
	var _x=x||0;
	var _y=y||0;
	var _text=text||"";
	var _this=this;
	this.source[name] =this.con.find("#"+name);
	this.source[name][0].x=_x;
	this.source[name][0].y=_y;
	this.source[name][0].text=_text;
	this.source[name].css("cursor","pointer");
	this.source[name].mouseover(function(event) {
		_this.box.html(this.text);
		_this.box.show();
		_this.box.css("margin-left",this.x);
		_this.box.css("margin-top",this.y);
	});
	this.source[name].mouseout(function(event) {
		_this.box.hide();
	});
}