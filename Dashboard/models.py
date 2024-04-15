from django.db import models
from Map.models import *
# Create your models here.

class Jangkos(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    afd_name = models.CharField(max_length=50)
    block_name = models.CharField(max_length=15)
    dumps = models.DateField(blank=True, null=True)
    aplikasi = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    selisih = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Jangkos'
