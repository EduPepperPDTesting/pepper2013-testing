String.prototype.isDate=function(formatString){
  formatString = formatString || "ymd";
  var m, year, month, day;
  switch(formatString){
  case "ymd" :
	m = this.match(new RegExp("^((\\d{4})|(\\d{2}))([-./])(\\d{1,2})\\4(\\d{1,2})$"));
	if(m == null ) return false;
	day = m[6];
	month = m[5]--;
	year =  (m[2].length == 4) ? m[2] : GetFullYear(parseInt(m[3], 10));
	break;
  case "dmy" :
	m = this.match(new RegExp("^(\\d{1,2})([-./])(\\d{1,2})\\2((\\d{4})|(\\d{2}))$"));
	if(m == null ) return false;
	day = m[1];
	month = m[3]--;
	year = (m[5].length == 4) ? m[5] : GetFullYear(parseInt(m[6], 10));
	break;
  case "mdy" :
	m = this.match(new RegExp("^(\\d{1,2})([-./])(\\d{1,2})\\2((\\d{4})|(\\d{2}))$"));
	if(m == null ) return false;
	day = m[3];
	month = m[1]--;
	year = (m[5].length == 4) ? m[5] : GetFullYear(parseInt(m[6], 10));
	break;
  default :
	break;
  }
  if(!parseInt(month)) return false;
  month = month==12 ?0:month;
  var date = new Date(year, month, day);
  return (typeof(date) == "object" && year == date.getFullYear() && month == date.getMonth() && day == date.getDate());
  function GetFullYear(y){return ((y<30 ? "20" : "19") + y)|0;}
}
function FormValidator(){
	this.errorMessage=[];
	this.errorItem=[];
}
FormValidator.prototype.chkTypes={
	Require : /.+/,
	Email : /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,
	Phone : /^((\(\d{3}\))|(\d{3}\-))?(\(0\d{2,3}\)|0\d{2,3}-)?[1-9]\d{6,7}$/,
	Mobile : /^((\(\d{3}\))|(\d{3}\-))?1\d{10}$/,
	Url : /^http:\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"\"])*$/,
	IdCard : /^\d{15}(\d{2}[A-Za-z0-9])?$/,
	Currency : /^\d+(\.\d+)?$/,
	Number : /^\d+$/,
	Zip : /^[1-9]\d{5}$/,
	QQ : /^[1-9]\d{4,8}$/,
	Integer : /^[-\+]?\d+$/,
	Double : /^[-\+]?\d+(\.\d+)?$/,
	English : /^[A-Za-z]+$/,
	Chinese :  /^[\u0391-\uFFE5]+$/,
	UnSafe : /^(([A-Z]*|[a-z]*|\d*|[-_\~!@#\$%\^&\*\.\(\)\[\]\{\}<>\?\\\/\'\"]*)|.{0,5})$|\s/,
	SafeString : "this.isSafe(value)",
	Limit : "this.limit(value.length,el.getAttribute('min'),  el.getAttribute('max'))",
	LimitB : "this.limit(this.lenB(value), el.getAttribute('min'), el.getAttribute('max'))",
	Date : "this.isDate(value, el.getAttribute('chkDateFormat'))",
	Repeat : "value == document.getElementsByName(el.getAttribute('to'))[0].value",
	Range : "el.getAttribute('min') < value && value < el.getAttribute('max')",
	Compare : "this.compare(value,el.getAttribute('operator'),el.getAttribute('to'))",
	Custom : "this.exec(value, el.getAttribute('chkRegExp'))",
	Group : "this.mustChecked(el.getAttribute('name'), el.getAttribute('min'), el.getAttribute('max'))"
}
FormValidator.prototype.check=function(elForm,mode){
	var count = elForm.elements.length;
	this.errorItem[0] = elForm;
	for(var i=0;i<count;i++){
		var el=elForm.elements[i];
		if(/text|hidden/i.test(el.type)||/textarea/.test(el.tagName)){
			el.value=el.value.trim();
		}
	  value=el.value;
	  var _chkType = el.getAttribute("chkType");
	  if(!_chkType)continue;
	  if(typeof(_chkType) == "elFormect" || typeof(this.chkTypes[_chkType]) == "undefined")  continue;
      this.clearState(el);
	  if(el.getAttribute("chkRequired") == "false" && value == "") continue;
	  if(this.chkTypes[_chkType] instanceof RegExp){
		if(!this.chkTypes[_chkType].test(value+"")){
		  this.addError(i, el.getAttribute("chkMsg"));
		}
	  }else{
        if(!eval(this.chkTypes[_chkType])) {
		  this.addError(i, el.getAttribute("chkMsg"));
		}
	  }
	}
	if(this.errorMessage.length > 0){
		mode = mode || 1;
		var errCount = this.errorItem.length;
		switch(mode){
		case 2 :
			for(var i=1;i<errCount;i++)
				this.errorItem[i].style.color = "red";
		case 1 :
			alert(this.errorMessage.join("\n"));
			try{this.errorItem[1].focus()}catch(e){}
			break;
		case 3 :
			for(var i=1;i<errCount;i++){
				try{
					var span = document.createElement("SPAN");
					span.id = "__ErrorMessagePanel";
					span.style.color = "red";
					this.errorItem[i].parentNode.appendChild(span);
					span.innerHTML = this.errorMessage[i].replace(/\d+:/,"*");
				}
				catch(e){alert(e.description);}
			}
			try{this.errorItem[1].focus()}catch(e){}
			break;
		default :
			alert(this.errorMessage.join("\n"));
			break;
		}
		return false;
	}
	return true;
}
FormValidator.prototype.isSafe = function(str){
	return !(this.chkTypes.UnSafe.test(str));
}
FormValidator.prototype.clearState = function(elem){
	if(elem.style.color == "red")elem.style.color = "";
	var lastNode = elem.parentNode.childNodes[elem.parentNode.childNodes.length-1];
	if(lastNode.id == "__ErrorMessagePanel")
		elem.parentNode.removeChild(lastNode);
}
FormValidator.prototype.addError =function(index, str){
	this.errorItem[this.errorItem.length] = this.errorItem[0].elements[index];
	this.errorMessage[this.errorMessage.length] = (this.errorMessage.length+1) + ". " + str;
}
FormValidator.prototype.limit = function(len,min,max){
	min = min || 0;
	max = max || Number.MAX_VALUE;
	return min <= len && len <= max;
}
FormValidator.prototype.lenB = function(str){
	return str.replace(/[^\x00-\xff]/g,"**").length;
}
FormValidator.prototype.exec = function(op, reg){
	return new RegExp(reg,"g").test(op);
}
FormValidator.prototype.compare =function(op1,operator,op2){
	switch (operator) {
	case "NotEqual":
		return (op1 != op2);
	case "GreaterThan":
		return (op1 > op2);
	case "GreaterThanEqual":
		return (op1 >= op2);
	case "LessThan":
		return (op1 < op2);
	case "LessThanEqual":
		return (op1 <= op2);
	default:
		return (op1 == op2);            
	}
}
FormValidator.prototype.mustChecked=function(name, min, max){
	var groups = document.getElementsByName(name);
	var hasChecked = 0;
	min = min || 1;
	max = max || groups.length;
	for(var i=groups.length-1;i>=0;i--)
		if(groups[i].checked) hasChecked++;
	return min <= hasChecked && hasChecked <= max;
}
FormValidator.prototype.isDate=function(sValue, formatString){
	return sValue.isDate(formatString)
}
