
# drop table json;
# drop table baseinfo_json;

# drop table baseinfo_enum;

# create table baseinfo_enum(
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `name` varchar(30) NOT NULL,
#   `value` int NOT NULL,
#   `content` varchar(100),
#   `extend` text,
#   `odr` int NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `name` (`name`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

# insert into baseinfo_json set name='percent for profile fields',content='["N/A ","< 5% ","6-10% ","11-15% ","16-20% ","21-25% ","26-30% ","> 30%"]';

# delete from baseinfo_enum;
# insert into baseinfo_enum set value='1',name='percent_lunch',content='N/A',odr='1';
# insert into baseinfo_enum set value='2',name='percent_lunch',content='< 5%',odr='2';
# insert into baseinfo_enum set value='3',name='percent_lunch',content='6-10%',odr='3';
# insert into baseinfo_enum set value='4',name='percent_lunch',content='11-15%',odr='4';
# insert into baseinfo_enum set value='5',name='percent_lunch',content='16-20%',odr='5';
# insert into baseinfo_enum set value='6',name='percent_lunch',content='21-25%',odr='6';
# insert into baseinfo_enum set value='7',name='percent_lunch',content='26-30%',odr='7';
# insert into baseinfo_enum set value='8',name='percent_lunch',content='> 30%',odr='8';

# insert into baseinfo_enum set value='1',name='percent_iep',content='N/A',odr='1';
# insert into baseinfo_enum set value='2',name='percent_iep',content='< 5%',odr='2';
# insert into baseinfo_enum set value='3',name='percent_iep',content='6-10%',odr='3';
# insert into baseinfo_enum set value='4',name='percent_iep',content='11-15%',odr='4';
# insert into baseinfo_enum set value='5',name='percent_iep',content='16-20%',odr='5';
# insert into baseinfo_enum set value='6',name='percent_iep',content='21-25%',odr='6';
# insert into baseinfo_enum set value='7',name='percent_iep',content='26-30%',odr='7';
# insert into baseinfo_enum set value='8',name='percent_iep',content='> 30%',odr='8';

# insert into baseinfo_enum set value='1',name='percent_eng_learner',content='N/A',odr='1';
# insert into baseinfo_enum set value='2',name='percent_eng_learner',content='< 5%',odr='2';
# insert into baseinfo_enum set value='3',name='percent_eng_learner',content='6-10%',odr='3';
# insert into baseinfo_enum set value='4',name='percent_eng_learner',content='11-15%',odr='4';
# insert into baseinfo_enum set value='5',name='percent_eng_learner',content='16-20%',odr='5';
# insert into baseinfo_enum set value='6',name='percent_eng_learner',content='21-25%',odr='6';
# insert into baseinfo_enum set value='7',name='percent_eng_learner',content='26-30%',odr='7';
# insert into baseinfo_enum set value='8',name='percent_eng_learner',content='> 30%',odr='8';

# alter table auth_userprofile add percent_lunch int not null;
# alter table auth_userprofile add percent_iep int not null;
# alter table auth_userprofile add percent_eng_learner int not null;

"""
Models for Base Info
"""
import json

from django.conf import settings
from django.db import models
from django.db import connection

class Enum(models.Model):
    name = models.CharField(blank=False, max_length=30)
    value = models.IntegerField(blank=False) 
    content = models.CharField(blank=False, max_length=100)
    extend = models.TextField(blank=True, max_length=1024)
    odr = models.IntegerField(blank=False) 

    def getList(self,name):
        self.object.filter(name=name).order_by("odr")

