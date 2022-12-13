from django.db import models

class photo(models.Model) :
    photo = models.ImageField(upload_to="%Y/%m/%d", null=True, blank=True)
    photo_reg_date  = models.DateField(auto_now = True, null=True)

    def __str__(self):
        return str(self.title)