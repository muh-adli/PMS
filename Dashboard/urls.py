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
    path('tankos/pokok/table', AplPokokTable, name='AplPokokTable'),
    path('tankos/tonase/table', AplTonaseTable, name='AplTonaseTable'),
    path('tankos/table/', TankosTable, name='TankosTable'),
    path('tankos/table/edit/<int:gid>/', TankosEdit, name='TankosEdit'),

    ## Dashboard Pupuk
    path('pupuk/', Pupuk, name='Pupuk'),

    ## Dashboard Monitoring
    path('patok/', Patok, name='Patok'),
    path('patok/table/', PatokTable, name='PatokTable'),
    path('patok/table/', PatokExtract, name='PatokExtract'),
    path('patok/table/<int:gid>/', PatokEdit, name='PatokEdit'),
]