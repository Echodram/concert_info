from django.db import models

class Information(models.Model):
    nom = models.CharField(max_length=250)
    telephone = models.CharField(max_length=25, unique=True)
    recevoirInfo = models.BooleanField(default=False)

    
    
   
    