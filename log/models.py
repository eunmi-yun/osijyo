from django.db import models

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
    status_code = models.ForeignKey("status", related_name="status", on_delete=models.CASCADE, db_column="status_code")
    disease_code = models.ForeignKey("disease", related_name="disease", on_delete=models.CASCADE, db_column="disease_code")
    image = models.ImageField(upload_to = "", null=True, blank=True)

    class Meta :
        managed = False
        db_table = 'history'