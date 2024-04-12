# Generated by Django 4.2.9 on 2024-02-05 20:23

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blok',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('objectid_1', models.FloatField(blank=True, db_column='OBJECTID_1', null=True)),
                ('est_name', models.CharField(blank=True, db_column='EST_NAME', max_length=50, null=True)),
                ('block_name', models.CharField(blank=True, db_column='BLOCK_NAME', max_length=15, null=True)),
                ('shape_leng', models.DecimalField(blank=True, db_column='Shape_Leng', decimal_places=65535, max_digits=65535, null=True)),
                ('shape_area', models.DecimalField(blank=True, db_column='Shape_Area', decimal_places=65535, max_digits=65535, null=True)),
                ('kaveld_pan', models.CharField(blank=True, db_column='KAVELD_PAN', max_length=10, null=True)),
                ('scale', models.IntegerField(blank=True, db_column='Scale', null=True)),
                ('legal_stat', models.CharField(blank=True, db_column='LEGAL_STAT', max_length=25, null=True)),
                ('genk_rayon', models.IntegerField(blank=True, db_column='GENK_RAYON', null=True)),
                ('jangkos', models.CharField(blank=True, db_column='Jangkos', max_length=20, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=32650)),
                ('dumps', models.DateField(blank=True, null=True)),
                ('aplikasi', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'blok',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('building', models.CharField(blank=True, max_length=80, null=True)),
                ('addr_city', models.CharField(blank=True, max_length=80, null=True)),
                ('komplek', models.CharField(blank=True, max_length=20, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'Building',
                'managed': False,
            },
        ),
    ]
