from django import forms
from .models import *

class EditJangkosFormAdd(forms.ModelForm):
    afd_name = forms.CharField(
        label="Afdeling",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        ),
    )
    block_name = forms.CharField(
        label="Block",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    area = forms.CharField(
        label="Area",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    class Meta:
        model = Block
        fields = ('afd_name','block_name','area')

class EditJangkosForm(forms.ModelForm):
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
        fields = ('dumps','aplikasi')


class EditPatokForm(forms.ModelForm):
    periode = (
        ("", "None"),
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
    )

    block_name = forms.CharField(
        label="Block",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    afd_name = forms.CharField(
        label="Afdeling",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    no_patok = forms.CharField(
        label="Nomor Patok",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    longitude = forms.CharField(
        label="longitude",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    latitude = forms.CharField(
        label="latitude",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    periode = forms.ChoiceField(
        label="periode",
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        choices=periode,
    )
    status = forms.CharField(
        label="status",
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'disabled': 'disabled'}
        )
    )
    class Meta:
        model = MonitoringPatokhgu
        fields = (
            'block_name',
            'afd_name',
            'no_patok',
            'longitude',
            'latitude',
            'periode',
            'status',
        )

