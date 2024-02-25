from django.db import models

# Create your models here.
class amrika(models.Model):
    unit= models.CharField(max_length=10, null = True, blank = True)
    salary = models.FloatField()