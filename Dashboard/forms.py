from django import forms
from .models import Block, Jangkos

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

