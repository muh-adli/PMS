from django.urls import path

## import function and else
from .views import *

## URL pattern and function
urlpatterns = [
    path('HomePage/', HomePage, name='HomePage'),

    ## Dashboard
    path('center/', center, name='Center'),
    path('hectare/', hectare, name='Hectare'),

    ## Dashboard Tankos
    path('tankos/', Tankos, name='Tankos'),

    ## Dump
    path('dump/table/', DumpTable, name='DumpTable'),
    path('dump/table/<int:gid>/', DumpEdit, name='DumpEdit'),

    ## Aplikasi
    path('apl/summary/table/', AplSummary, name='AplSummary'),

    path('apl/pokok/table/<int:geomid>/', AplPokokTable, name='AplPokokTable'),
    path('apl/pokok/table/edit/', AplPokokEdit, name='AplPokokEdit'),

    path('apl/tonase/table/<int:geomid>/', AplTonaseTable, name='AplTonaseTable'),
    path('apl/tonase/table/edit/', AplTonaseEdit, name='AplTonaseEdit'),

    ## Dashboard Pupuk
    path('pupuk/', Pupuk, name='Pupuk'),

    ## Dashboard Monitoring
    path('patok/', Patok, name='Patok'),
    path('patok/table/', PatokTable, name='PatokTable'),
    path('patok/table/download/', PatokExtract, name='PatokExtract'),
    path('patok/table/<int:gid>/', PatokEdit, name='PatokEdit'),
]