import django_tables2 as tables # initiate django_tables
from django.urls import reverse
from django.utils.html import format_html

## Import models
from .models import *
from Map.models import *

class PatokDashboardTable(tables.Table):
    class Meta:
        model = HguPatok
        sequence = (
            "no_patok",
            "afd_name",
            "block_name",
            "longitude",
            "latitude",
            "periode",
            "status",
        )
        exclude = (
            "gid",
            "objectid",
            "kode",
            "x",
            "y",
            "geom",
            "geom",
            "geom",)
        attrs = {
            "class": "table table-hover table-striped align-middle",
            'thead': {
                'class': 'table-success',
                },
            }  # Add Bootstrap classes
        
class PatokTab(tables.Table):
    edit = tables.TemplateColumn(
                            template_code='''
                                            <a href="{% url 'PatokEdit' record.gid %}" class="btn btn-sm btn-outline-success" role="button" aria-pressed="true">Edit</a>
                                            ''',
                            verbose_name='Edit'
                            )
    class Meta:
        model = HguPatok
        sequence = (
            "no_patok",
            "afd_name",
            "block_name",
            "longitude",
            "latitude",
            "periode",
            "status",
        )
        exclude = (
            "gid",
            "objectid",
            "kode",
            "x",
            "y",
            "geom",
            "geom",
            "geom",)
        attrs = {
            "class": "table table-hover table-striped align-middle",
            'thead': {
                'class': 'table-success',
                },
            }  # Add Bootstrap classes
