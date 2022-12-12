from django.db import models


class history (models.Model) :
    history_id = models.AutoField(primary_key=True)
    reg_date = models.DateField()
    disease_name = models.CharField(max_length=50)
    disease_cure = models.CharField(max_length=200)
    
    class Meta :
        managed = False
        db_table = 'history'