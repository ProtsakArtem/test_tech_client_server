from django.db import models

# Create your models here.


class DataRecord(models.Model):
    name = models.CharField(max_length=256)
    encrypted_data = models.TextField()