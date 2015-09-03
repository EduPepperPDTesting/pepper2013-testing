var copy = false;
function CertificateEditor(editor){
    this.content='';
    this.CKEDITOR=editor;
    this.isReadOnly=false;
    this.isPublish=false; 
    this.currView='Editor';
    this.certificateID=0;
    this.association_type=0;
    this.association=0;
    this.certificate_name=""
    this.editorState=[];
}
CertificateEditor.prototype.init=function(){
    this.content='';
    this.isPublish=false; 
    this.currView='Editor'; 
    this.certificateID=0;
    this.association_type=0;
    this.association=0;
    this.CKEDITOR.setData("");
    this.certificate_name="";
    $(".certificate_name").val('');
    this.setReadOnly(false);
    this.setPublishIcon(this.isPublish);
}
CertificateEditor.prototype.loadCertificate=function(id){
    this.certificateID=id;
    var self=this;
      $.post("/configuration/certificate/load_data",{id:this.certificateID},function(r){
         self.certificate_name=r.certificate_name;
         self.association_type=r.association_type||0;
         self.association=r.association||0;
         self.content=r.content;
         self.CKEDITOR.setData(self.content);
         self.isPublish=self.association_type==0?false:true;
         self.setReadOnly(r.readonly);
         self.setPublishIcon(self.isPublish);
         $(".certificate_name").val(self.certificate_name);
         self.setState();
      });
    setTimeout(function(){CKEDITOR.instances.certificate_editor.resetDirty();},750);
    copy = false;
}
CertificateEditor.prototype.save=function(callback){
    this.certificate_name=$(".certificate_name").val();
    if(this.certificate_name==""){
      new Dialog($('#dialog')).show('Error','You need a name for your certificate.');return;
    }
    else{
      var self=this;
      var data={id:this.certificateID,name:this.certificate_name,content:this.CKEDITOR.getData(),association_type:this.association_type,association:this.association,readonly:this.isReadOnly};
      $.post("/configuration/certificate/save",data,function(r){
          if(r.success){
            self.certificateID=r.id;
            self.setState();
            new Dialog($('#dialog')).show('OK',r.msg);
          }
          else{new Dialog($('#dialog')).show('Error',r.msg);}
          (callback && typeof(callback) === "function") && callback();
          return;
      });
    }
}
CertificateEditor.prototype.copy=function(){
 var self=this;
 if(this.isStateChange()){
     var dirty = CKEDITOR.instances.certificate_editor.checkDirty();
     if(dirty || copy) {
         new Dialog($('#dialog')).showButtons("Warning", "<p>Do you want to save the current certificate?</p><br/>", ['Yes', 'No'], function (choice) {
             if (choice == 0) {
                 this.hide();
                 self.save(function () {
                     self.createCopy();
                 });

             } else {
                 copy = true;
                 this.hide();
                 self.createCopy();
             }
         })
     }else{
         copy = true;
         self.createCopy();
     }
  }
  else{
    self.createCopy();
  }
}
CertificateEditor.prototype.createCopy=function(){
  copy = true;
  this.isPublish=false;
  this.currView='Editor'; 
  this.certificateID=0;
  this.association_type=0;
  this.association=0;
  this.setReadOnly(false);
  this.certificate_name=$(".certificate_name").val();
  this.certificate_name=this.certificate_name+"_copy";
  $(".certificate_name").val(this.certificate_name);
  this.setPublishIcon(this.isPublish);
  this.setReadOnlyIcon(this.isReadOnly);
  this.setState();
}
CertificateEditor.prototype.publish=function(filter){
    this.association_type=filter['association_type'];
    this.association=filter['association'];
    this.isPublish=true;
    ceditor.setPublishIcon(this.isPublish);
}
CertificateEditor.prototype.unPublish=function(){
    this.association_type=0;
    this.association=0;
    this.isPublish=false;
    ceditor.setPublishIcon(this.isPublish);
}
CertificateEditor.prototype.setState=function(){
   this.editorState=[];
   for (var p in this) {
      if(typeof(this[p])!='function'&& p!='editorState'){
        this.editorState[p]=this[p];
      }
    }
}
CertificateEditor.prototype.isStateChange=function(){
  this.certificate_name=$(".certificate_name").val();
  this.content=this.CKEDITOR.getData();
    for (var p in this) {
      if(typeof(this[p])!='function'&& p!='editorState'){
        if(this.editorState[p]!=this[p]){        
          return true;
        }
      }
    }
    return false;
}
CertificateEditor.prototype.cancel=function(callback){
   var self=this;

    var dirty = CKEDITOR.instances.certificate_editor.checkDirty();
    if(dirty || copy) {
        new Dialog($('#dialog')).showButtons("Warning", "<p style='font-size:13px;'>You will lose any changes you have made to this certificate if you continue.</p><br/>", ['Continue Editing', 'Cancel Edits'], function (choice) {
            if (choice == 0) {
                this.hide();
            } else {
                this.hide();
                self.init();
                (callback && typeof(callback) === "function") && callback();
            }
        })
    }else{
        self.init();
        (callback && typeof(callback) === "function") && callback();
    }

}
CertificateEditor.prototype.delete=function(callback){
   var self=this;
   new Dialog($('#dialog')).showButtons("Warning","<p>Are you sure you want to delete this certificate?</p><br/>",['Yes','No'],function(choice){
      if(choice==0){ 
        if(self.certificateID>0){
          $.post('/configuration/certificate/delete',{ids:self.certificateID},function(){(callback && typeof(callback) === "function") && callback();});
          this.hide();
        }
        else{
          self.init();
          this.hide();
          (callback && typeof(callback) === "function") && callback();
        }
      }else{this.hide();}
    }) 
 
}
CertificateEditor.prototype.setReadOnly=function(b,user_select){
  //user_select:Read-only it is true by the value set by the user, otherwise false.
  var userSelect=user_select||false;
  this.isReadOnly=Boolean(b);
  this.CKEDITOR.setReadOnly(b);
  this.setReadOnlyIcon(b);
  var dirty = CKEDITOR.instances.certificate_editor.checkDirty();

  if((dirty || copy) && b && userSelect)this.saveYesNo("Save certificate","<p>You want to save the certificate?</p><br/>");

}
CertificateEditor.prototype.saveYesNo=function(title,content){

      var self = this;
      new Dialog($('#dialog')).showButtons(title, content, ['Yes', 'No'], function (choice) {
          if (choice == 0) {
              self.save();
              this.hide();
          }
          else {
              this.hide();
          }
      })

}
CertificateEditor.prototype.print=function(element){
  this.CKEDITOR.execCommand('print');
}
CertificateEditor.prototype.switchView=function(name){
  this.currView=name;
}
CertificateEditor.prototype.replacePlaceholder=function(str){
  var placeholderSet={};
  placeholderSet.firstname="John";
  placeholderSet.lastname="Doe";
  placeholderSet.coursename="Wonderful Course";
  placeholderSet.coursenumber="PEP101x";
  placeholderSet.date="January 16, 2015";
  placeholderSet.hours="10 hours";
  for(var p in placeholderSet)str=str.replaceAll('{'+p+'}',placeholderSet[p]);
  return str;
}
CertificateEditor.prototype.setPublishIcon=function(b){
  if(b){$('.imgBtn_publish').parent().hide();$('.imgBtn_unpublish').parent().show();}
  else{$('.imgBtn_publish').parent().show();$('.imgBtn_unpublish').parent().hide();}
}
CertificateEditor.prototype.setReadOnlyIcon=function(b){
  if(b){$('.imgBtn_readonly').parent().hide();$('.imgBtn_edit').parent().show();}
  else{$('.imgBtn_readonly').parent().show();$('.imgBtn_edit').parent().hide();}
}

