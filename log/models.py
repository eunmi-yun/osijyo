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
    disease_code = models.ForeignKey("disease", related_name="disease", on_delete=models.CASCADE, db_column="disease_code")
    user_id = models.ForeignKey("user", related_name="user", on_delete=models.CASCADE, db_column="user_id")

    class Meta :
        managed = False
        db_table = 'history'