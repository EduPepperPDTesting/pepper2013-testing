function getFormData(form,flds){
  var data={}
  $.each(flds,function(i,n){
    data[n]=$(form[n]).val();
  })
  return data;
}
function infoAndWait(box,info,seconds,go){
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
function dropDistrict(form,state_id,callback){
  $.get('/reg_kits/drop_districts',{state_id:state_id},function(r){
      if((typeof r) == 'string'){
        r=$.parseJSON(r)
      }
      var html="";
      var drop=form.find("select[name=district_id]");
      drop.find("option").filter(function(){return this.getAttribute("value")!=""}).remove()
      for(k in r){
        d=r[k];
        html+="<option value='" + d.id+"'>" + d.name + " - " + d.code + "</option>";
      }
      drop.append(html)
      if(callback instanceof Function)callback.apply(drop[0]);
  });
}
function dropSchool(form,state_id,district_id,callback){
  $.get('/reg_kits/drop_schools',{state_id:state_id,district_id:district_id},function(r){
    if((typeof r) == 'string')r=$.parseJSON(r)
    var html="";
    var drop=form.find("select[name=school_id]")
    drop.find("option").filter(function(){return this.getAttribute("value")!=""}).remove()
    for(k in r){
      d=r[k];
      html+="<option value='" + d.id+"'>" + d.name + "</option>"
    }
    drop.append(html)
    if(callback instanceof Function)callback.apply(drop[0]);
  });
}
function dropCohort(form,state_id,district_id,callback){
  $.get('/reg_kits/drop_cohorts',{state_id:state_id,district_id:district_id},function(r){
    if((typeof r) == 'string')r=$.parseJSON(r)
    var html="";
    var drop=form.find("select[name=cohort_id]")         
    drop.find("option").filter(function(){return this.getAttribute("value")!=""}).remove()
    for(k in r){
      d=r[k];
      html+="<option value='" + d.id+"'>" + d.code + "</option>"
    }
    drop.append(html)
    if(callback instanceof Function)callback.apply(drop[0]);
  });
}             
