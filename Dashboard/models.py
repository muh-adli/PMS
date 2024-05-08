from django.db import models
from Map.models import *
# Create your models here.

## Tables

class TankosAplpokok(models.Model):
    afdeling = models.CharField(blank=True, null=True)
    block = models.CharField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    pokok = models.IntegerField(blank=True, null=True)
    geomid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tankos_aplpokok'

class TankosApltonase(models.Model):
    afdeling = models.CharField(blank=True, null=True)
    block = models.CharField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    tonase = models.FloatField(blank=True, null=True)
    geomid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tankos_apltonase'


## Views
class TankosDumpsummary(models.Model):
    afdeling = models.CharField(max_length=5, blank=True, null=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    dump_location = models.BigIntegerField(blank=True, null=True)
    dump_date = models.DateField(blank=True, null=True)
    dump_diff = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dump_status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'tankos_dumpsummary'


class TankosSummary(models.Model):
    afdeling = models.CharField(max_length=5, blank=True, null=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    date_delta = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    pokok = models.IntegerField(blank=True, null=True)
    tonase = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'tankos_summary'

class TankosAplsummary(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    afdeling = models.CharField(max_length=5, blank=True, null=True)
    tot_pokok = models.IntegerField(blank=True, null=True)
    tot_tonase = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sph = models.FloatField(blank=True, null=True)
    prog_tonase = models.FloatField(blank=True, null=True)
    prog_pokok = models.BigIntegerField(blank=True, null=True)
    prog_ha = models.FloatField(blank=True, null=True)
    last_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'tankos_aplsummary'
        
class TankosDumpview(models.Model):
    gid = models.IntegerField(primary_key=True)
    afdeling = models.CharField(max_length=5, blank=True, null=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    location = models.CharField(max_length=10, blank=True, null=True)
    dump_date = models.DateField(blank=True, null=True)
    apl_date = models.DateField(blank=True, null=True)
    date_diff = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'tankos_dumpview'

