from django.db import models

# Create your models here.
class Token:
    token = models.CharField(max_length=256, primary_key=True)
    data = models.IntegerField()
    exp = models.DateField()

