from django.contrib.gis.db import models

# Create your models here.
class Block(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    block_name = models.CharField(max_length=15, blank=True, null=True)
    werks = models.FloatField(blank=True, null=True)
    afd_code = models.CharField(max_length=50, blank=True, null=True)
    spmon = models.CharField(max_length=50, blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    planted = models.CharField(max_length=50, blank=True, null=True)
    block_code = models.CharField(max_length=50, blank=True, null=True)
    yop = models.CharField(max_length=50, blank=True, null=True)
    topo = models.CharField(max_length=50, blank=True, null=True)
    estate = models.CharField(max_length=50, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32650, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'block'