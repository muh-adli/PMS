from django import forms
from .models import *

class addPokokForm(forms.ModelForm):
    afdeling = forms.CharField(
        label="Afdeling",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'afdeling'
            }
        ),
    )
    block = forms.CharField(
        label="Block",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'block'
            }
        ),
    )
    date = forms.CharField(
        label="Date",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'date'
            }
        ),
    )
    pokok = forms.CharField(
        label="Pokok",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'pokok'
            }
        ),
    )
    geomid = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'geomid'
            }
        ),
    )

    class Meta:
        model = TankosAplpokok
        fields = (
            'afdeling',
            'block',
            'date',
            'pokok',
            'geomid',
        )
class addTonaseForm(forms.ModelForm):
    afdeling = forms.CharField(
        label="Afdeling",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'afdeling'
            }
        ),
    )
    block = forms.CharField(
        label="Block",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'block'
            }
        ),
    )
    date = forms.CharField(
        label="Date",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'date'
            }
        ),
    )
    tonase = forms.CharField(
        label="Tonase",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'tonase'
            }
        ),
    )
    geomid = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'geomid'
            }
        ),
    )

    class Meta:
        model = TankosApltonase
        fields = (
            'afdeling',
            'block',
            'date',
            'tonase',
            'geomid',
        )

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
    dump_date = forms.DateField(
        label="Dump Date",
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
                }
        )
    )
    apl_date = forms.DateField(
        label="Aplikasi Date",
        required=False,
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
            'apl_date'
        )

class EditPatokForm(forms.ModelForm):
    periode_choices = (
        (None, "None"),
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
