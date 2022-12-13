from django.db import models


class history (models.Model) :
    history_id = models.AutoField(primary_key=True)
    reg_date = models.DateField()
    disease_name = models.CharField(max_length=50)
    disease_cure = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="%Y/%m/%d", null=True, blank=True)
    
    @property
    def image_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
    class Meta :
        managed = False
        db_table = 'log_log'