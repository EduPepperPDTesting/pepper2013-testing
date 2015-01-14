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
  if(state_id=='__NONE__')state_id='-1';
  $.get('/reg_kits/drop_districts',{state_id:state_id},function(r){
      if((typeof r) == 'string'){
        r=$.parseJSON(r)
      }
      var html="";
      var drop=form.find("select[name=district_id]");
      clearOption(drop)
      for(k in r){
        d=r[k];
        html+="<option value='" + d.id+"'>" + d.name + " - " + d.code + "</option>";
      }
      drop.append(html)
      if(callback instanceof Function)callback.apply(drop[0]);
  });
}
function dropSchool(form,state_id,district_id,callback){
  if(state_id=='__NONE__')state_id='-1';
  if(district_id=='__NONE__')district_id='-1';
  $.get('/reg_kits/drop_schools',{state_id:state_id,district_id:district_id},function(r){
    if((typeof r) == 'string')r=$.parseJSON(r)
    var html="";
    var drop=form.find("select[name=school_id]")
    clearOption(drop)
    for(k in r){
      d=r[k];
      html+="<option value='" + d.id+"'>" + d.name + "</option>"
    }
    drop.append(html)
    if(callback instanceof Function)callback.apply(drop[0]);
  });
}
function dropCohort(form,state_id,district_id,callback){
  if(state_id=='__NONE__')state_id='-1';
  if(district_id=='__NONE__')district_id='-1';
  $.get('/reg_kits/drop_cohorts',{state_id:state_id,district_id:district_id},function(r){
    if((typeof r) == 'string')r=$.parseJSON(r)
    var html="";
    var drop=form.find("select[name=cohort_id]")
    clearOption(drop)
    clearOption(drop)
    for(k in r){
      d=r[k];
      html+="<option value='" + d.id+"'>" + d.code + "</option>"
    }
    drop.append(html)
    if(callback instanceof Function)callback.apply(drop[0]);
  });
}             
function clearOption(drop){
  drop.find("option").filter(
    function(){
      return this.getAttribute("value")!="" && this.getAttribute("value")!="__NONE__"
    }
  ).remove()
}
function get_searching(){
  var search=window.location.search;
  var p=[];
  var reg=/([^\?&=]+)=([^\?&=]+)/g
  while(m=reg.exec(search)){
    p[m[1]]=m[2];
  }
  return p;
}
function gen_searching(p){
  var ar=[];
  for(k in p){
    v=p[k];
    ar.push(k+"="+encodeURI(v));
  }
  return "?"+ar.join("&")
}  
function replace_searching(h){
  var p=get_searching();
  for(k in h)p[k]=h[k];
  return gen_searching(p);
}
