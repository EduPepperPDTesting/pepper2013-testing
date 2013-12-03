var easy={}
easy.form={}
easy.form.getFormData=function(form,flds){
  var data={}
  $.each(flds,function(i,n){
    data[n]=$(form[n]).val();
  })
  return data;
}
easy.form.infoAndWait=function(box,info,seconds,go){
  var w=seconds;
  $(box).show()
  function count(){
    $(box).html(info + ". <b>" + w + "</b>");
    setTimeout(function(){
      if(w < 1){
        window.location.href=go;
      }else{
        w--;
        count()
      }
    },1000);                             
  }
  count();
}
