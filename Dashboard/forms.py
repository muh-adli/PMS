from django import forms
from .models import *

class EditTankosFormAdd(forms.ModelForm):
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
        model = HguBlock
        fields = ('afd_name','block_name','area')

class EditTankosForm(forms.ModelForm):
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
        model = TankosAplsummary
        fields = ('dumps','aplikasi')


class EditDumpForm(forms.ModelForm):
    afdeling = forms.CharField(
        label="Afdeling",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    block = forms.CharField(
        label="Block",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    location = forms.CharField(
        label="Location",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    dump_date = forms.CharField(
        label="Date",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
                }
        )
    )
    class Meta:
        model = TankosDumpdata
        fields = (
            'afdeling',
            'block',
            'location',
            'dump_date',
        )

class EditPatokForm(forms.ModelForm):
    periode_choices = (
        ("", "None"),
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
    )

    block_name = forms.CharField(
        label="Block",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    afd_name = forms.CharField(
        label="Afdeling",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    no_patok = forms.CharField(
        label="Nomor Patok",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    longitude = forms.CharField(
        label="longitude",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    latitude = forms.CharField(
        label="latitude",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        )
    )
    periode = forms.ChoiceField(
        label="periode",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }
        ),
        choices=periode_choices,
    )
    status = forms.CharField(
        label="Status",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'}
        ),
        required=False  # Make the status field optional
    )

    class Meta:
        model = HguPatok
        fields = (
            'block_name',
            'afd_name',
            'no_patok',
            'longitude',
            'latitude',
            'periode',
            'status',
        )
