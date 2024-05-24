from django.contrib.gis.db import models

# Create your models here.
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


class HguAfdeling(models.Model):
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
        db_table = 'hgu_afdeling'

class HguBlock(models.Model):
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
        db_table = 'hgu_block'

class HguJalan(models.Model):
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
    panjang = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    geom = models.MultiLineStringField(srid=32650, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hgu_jalan'


class HguJembatan(models.Model):
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
        db_table = 'hgu_jembatan'


class HguPatok(models.Model):
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
    update_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hgu_patok'


class HguPlanted(models.Model):
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
        db_table = 'hgu_planted'


class KaveldOa(models.Model):
    gid = models.AutoField(primary_key=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    block_name = models.CharField(max_length=15, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    werks = models.FloatField(blank=True, null=True)
    afd_code = models.CharField(max_length=50, blank=True, null=True)
    spmon = models.CharField(max_length=50, blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    planted = models.CharField(max_length=50, blank=True, null=True)
    luas20 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    luas20q2 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    block_code = models.CharField(max_length=50, blank=True, null=True)
    yop = models.CharField(max_length=50, blank=True, null=True)
    topo = models.CharField(max_length=50, blank=True, null=True)
    estate = models.CharField(max_length=50, blank=True, null=True)
    driven = models.CharField(max_length=20, blank=True, null=True)
    shape_le_1 = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    kaveld = models.CharField(max_length=10, blank=True, null=True)
    ancak = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32650, dim=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kaveld_oa'


class TankosAplgeom(models.Model):
    gid = models.AutoField(primary_key=True)
    afdeling = models.CharField(max_length=5)
    block = models.CharField(max_length=5)
    tot_pokok = models.IntegerField(blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tot_tonase = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    aplikasi = models.DateField(blank=True, null=True)
    prog_pokok = models.IntegerField(blank=True, null=True)
    prog_tonase = models.FloatField(blank=True, null=True)
    sph = models.FloatField(blank=True, null=True)
    geom = models.MultiPolygonField(srid=32650, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tankos_aplgeom'


class TankosDumpdata(models.Model):
    gid = models.AutoField(primary_key=True)
    afdeling = models.CharField(max_length=5, blank=True, null=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    location = models.CharField(max_length=10, blank=True, null=True)
    dump_date = models.DateField(blank=True, null=True)
    geom = models.PointField(srid=32650, blank=True, null=True)
    apl_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tankos_dumpdata'
        
class TankosDumpApi(models.Model):
    gid = models.IntegerField(primary_key=True)
    afdeling = models.CharField(max_length=5, blank=True, null=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    location = models.CharField(max_length=10, blank=True, null=True)
    dump_date = models.DateField(blank=True, null=True)
    apl_date = models.DateField(blank=True, null=True)
    date_diff = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    geometry = models.GeometryField(srid=4326, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'tankos_dump_api'
        
class TankosAplApi(models.Model):
    gid = models.IntegerField(primary_key=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    afdeling = models.CharField(max_length=5, blank=True, null=True)
    tot_pokok = models.IntegerField(blank=True, null=True)
    tot_tonase = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sph = models.FloatField(blank=True, null=True)
    prog_tonase = models.FloatField(blank=True, null=True)
    prog_pokok = models.BigIntegerField(blank=True, null=True)
    prog_ha = models.FloatField(blank=True, null=True)
    last_date = models.DateField(blank=True, null=True)
    geometry = models.GeometryField(srid=4326, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'tankos_apl_api'
        
class HgublockView(models.Model):
    gid = models.IntegerField(primary_key=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    block_name = models.CharField(max_length=15, blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    st_transform = models.GeometryField(srid=32650, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'hgublock_view'


class HguplantedView(models.Model):
    gid = models.IntegerField(primary_key=True)
    afd_name = models.CharField(max_length=50, blank=True, null=True)
    block_name = models.CharField(max_length=15, blank=True, null=True)
    ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    st_transform = models.GeometryField(srid=32650, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'hguplanted_view'