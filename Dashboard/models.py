from django.db import models
from django import forms
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

class EditJangkosForm(forms.ModelForm):
    afd_name = forms.CharField(
        label="Afdeling",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'readonly':'readonly'}
        )
    )
    block_name = forms.CharField(
        label="Block",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'readonly':'readonly'}
        )
    )
    dumps = forms.DateField(
        label="Dumps",
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'type': 'date'}
        )
    )
    aplikasi = forms.DateField(
        label="Aplikasi",
        widget=forms.DateInput(
            attrs={'class': 'form-control',
                   'type': 'date'}
        )
    )
    class Meta:
        model = Jangkos
        fields = ('afd_name','block_name','dumps','aplikasi')
