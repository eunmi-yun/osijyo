from django.db import models
 
class image(models.Model) :
    image = models.ImageField(upload_to = "images/", null=True, blank=True)
    image_reg_date  = models.DateField(auto_now = True, null=True)

    def __str__(self):
        return str(self.title)
