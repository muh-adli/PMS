from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    path('HomePage/', HomePage, name='HomePage'),
    ## Dashboard
    path('dasboard/center/', center, name='Center'),
    path('dasboard/hectare/', hectare, name='Hectare'),

    ## Dashboard Jangkos
    path('dasboard/jangkos/', jangkos, name='Jangkos'),
    path('dasboard/jangkos/table/', JangkosTable, name='JangkosTable'),
    path('dasboard/jangkos/table/edit/<int:gid>/', JangkosEdit, name='JangkosEdit'),
    ## Dashboard Pupuk
    path('dasboard/pupuk/', pupuk, name='Pupuk'),
    ## Dashboard Monitoring
    path('dasboard/monitoring/', Monitoring, name='Monitoring'),
    path('dasboard/monitoring/patok/table/', PatokTable, name='PatokTable'),
    path('dasboard/monitoring/patok/table/<int:gid>/', PatokEdit, name='PatokEdit'),
]