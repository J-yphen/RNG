from django.db import models

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=256, primary_key=True)
    data = models.BigIntegerField()
    exp = models.DateField()

