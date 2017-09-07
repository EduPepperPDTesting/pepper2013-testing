from django.db import models
from django.contrib.auth.models import User
from student.models import District, State
from administration.models import PepRegTraining, PepRegStudent

# class TrainingTrainings(models.Model):
#     class Meta:
#         db_table = 'training_trainings'
#     name = models.CharField(blank=False, max_length=255, db_index=True)
#     state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, blank=True)
#     district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)

class TrainingUsers(models.Model):
    class Meta:
        db_table = 'training_users'
    training = models.ForeignKey(PepRegTraining, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)