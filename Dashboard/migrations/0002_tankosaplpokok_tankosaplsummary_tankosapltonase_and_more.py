# Generated by Django 4.2.9 on 2024-05-08 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TankosAplpokok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afdeling', models.CharField(blank=True, null=True)),
                ('block', models.CharField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('pokok', models.IntegerField(blank=True, null=True)),
                ('geomid', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tankos_aplpokok',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TankosAplsummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.IntegerField(blank=True, null=True)),
                ('block', models.CharField(blank=True, max_length=5, null=True)),
                ('afdeling', models.CharField(blank=True, max_length=5, null=True)),
                ('tot_pokok', models.IntegerField(blank=True, null=True)),
                ('tot_tonase', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('sph', models.FloatField(blank=True, null=True)),
                ('prog_tonase', models.FloatField(blank=True, null=True)),
                ('prog_pokok', models.BigIntegerField(blank=True, null=True)),
                ('prog_ha', models.FloatField(blank=True, null=True)),
                ('last_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tankos_aplsummary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TankosApltonase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afdeling', models.CharField(blank=True, null=True)),
                ('block', models.CharField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('tonase', models.FloatField(blank=True, null=True)),
                ('geomid', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tankos_apltonase',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TankosDumpsummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afdeling', models.CharField(blank=True, max_length=5, null=True)),
                ('block', models.CharField(blank=True, max_length=5, null=True)),
                ('dump_location', models.BigIntegerField(blank=True, null=True)),
                ('dump_date', models.DateField(blank=True, null=True)),
                ('dump_diff', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('dump_status', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tankos_dumpsummary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TankosSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('afdeling', models.CharField(blank=True, max_length=5, null=True)),
                ('block', models.CharField(blank=True, max_length=5, null=True)),
                ('area', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('date_delta', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('status', models.TextField(blank=True, null=True)),
                ('pokok', models.IntegerField(blank=True, null=True)),
                ('tonase', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tankos_summary',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Jangkos',
        ),
    ]
