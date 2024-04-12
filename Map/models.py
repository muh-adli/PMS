from django.contrib.gis.db import models

# Create your models here.
class Afdeling(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    werks = models.FloatField(blank=True, null=True)
    afd_code = models.CharField(max_length=50, blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    spmon = models.DateField(blank=True, null=True)
    estate = models.CharField(max_length=50, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32650, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'afdeling'

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

class Hgu(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    werks = models.IntegerField(blank=True, null=True)
    comp_code = models.IntegerField(blank=True, null=True)
    spmon = models.DateField(blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32650, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hgu'

class Jembatan(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    werks = models.FloatField(blank=True, null=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    block_name = models.CharField(max_length=15, blank=True, null=True)
    kategory = models.CharField(max_length=20, blank=True, null=True)
    dimensi = models.CharField(max_length=20, blank=True, null=True)
    kondisi = models.CharField(max_length=50, blank=True, null=True)
    topo = models.CharField(max_length=50, blank=True, null=True)
    planted = models.CharField(max_length=50, blank=True, null=True)
    yop = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    x = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    y = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    keterangan = models.CharField(max_length=15, blank=True, null=True)
    geom = models.PointField(srid=32650, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jembatan'


class MonitoringPatokhgu(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    kode = models.CharField(max_length=20, blank=True, null=True)
    x = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    y = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    block_name = models.CharField(max_length=10, blank=True, null=True)
    afd_name = models.CharField(max_length=20, blank=True, null=True)
    no_patok = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    periode = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    geom = models.PointField(srid=32650, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitoring_patokhgu'


class Planted(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    block_name = models.CharField(max_length=15, blank=True, null=True)
    block_sap = models.CharField(max_length=3, blank=True, null=True)
    spmon = models.DateField(blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tahun = models.CharField(max_length=10, blank=True, null=True)
    level_1 = models.CharField(max_length=25, blank=True, null=True)
    level_2 = models.CharField(max_length=25, blank=True, null=True)
    werks = models.CharField(max_length=50, blank=True, null=True)
    ln_cat = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32650, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'planted'


class Road(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.FloatField(blank=True, null=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    block_name = models.CharField(max_length=15, blank=True, null=True)
    road_cat = models.CharField(max_length=30, blank=True, null=True)
    road_name = models.CharField(max_length=20, blank=True, null=True)
    perkerasan = models.CharField(max_length=50, blank=True, null=True)
    keterangan = models.CharField(max_length=50, blank=True, null=True)
    spmon = models.CharField(max_length=50, blank=True, null=True)
    rd_sym = models.CharField(max_length=50, blank=True, null=True)
    road_code = models.CharField(max_length=50, blank=True, null=True)
    werks = models.FloatField(blank=True, null=True)
    kj = models.CharField(max_length=15, blank=True, null=True)
    panjang = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.MultiLineStringField(srid=32650, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'road'