from django.db import models
from Map.models import *
# Create your models here.

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
