
db.PepRegTrainingView.remove({'school_year':'current'});
db.pepreg_training.find().forEach(function(x){
    delete x._id;
    x.school_year = 'current';
    x.key = x.school_year + '_' + x.training_id;
    db.PepRegTrainingView.save(x);
})

db.PepRegStudentView.remove({'school_year':'current'});
db.pepreg_student.find().forEach(function(x){
    delete x._id;
    x.school_year = 'current';
    if(x.instructor_id != 'NULL'){
        x.instructor_status = 'Yes';
    }
    else{
        x.instructor_status = 'No';
    }  
    x.key = x.school_year + '_' + x.training_id; 
    db.PepRegStudentView.save(x);
})
