from django.db import models

class user(models.Model) :
    user_id = models.AutoField(primary_key=True)
    user_pw = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    user_email = models.CharField(max_length=50)
    reg_date = models.DateTimeField()

    class Meta :
        managed = False
        db_table = 'user'

class status(models.Model) :
    status_code = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=45)

    class Meta :
        managed = False
        db_table = 'status'

class disease(models.Model) :
    disease_code = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=45)
    disease_cure = models.CharField(max_length=45)
    scientific_name = models.CharField(max_length=50)
    disease_group = models.CharField(max_length=50)

    class Meta :
        managed = False
        db_table = 'disease'


class history (models.Model) :
    history_id = models.AutoField(primary_key=True)
    reg_date = models.DateField()
    disease_name = models.CharField(max_length=50)
    disease_cure = models.CharField(max_length=200)
    status_code = models.ForeignKey(status,models.DO_NOTHING, blank=True,null=False)
    disease_code = models.ForeignKey(disease,models.DO_NOTHING,blank=True,null=True)
    user_id = models.ForeignKey(user,models.DO_NOTHING,blank=True,null=True)

    class Meta :
        managed = False
        db_table = 'history'