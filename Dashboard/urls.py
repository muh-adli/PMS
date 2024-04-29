from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    path('HomePage/', HomePage, name='HomePage'),
    ## Dashboard
    path('center/', center, name='Center'),
    path('hectare/', hectare, name='Hectare'),

    ## Dashboard Jangkos
    path('jangkos/', jangkos, name='Jangkos'),
    path('jangkos/table/', JangkosTable, name='JangkosTable'),
    path('jangkos/table/edit/<int:gid>/', JangkosEdit, name='JangkosEdit'),
    ## Dashboard Pupuk
    path('pupuk/', pupuk, name='Pupuk'),
    ## Dashboard Monitoring
    path('patok/', Patok, name='Patok'),
    path('patok/table/', PatokTable, name='PatokTable'),
    path('patok/table/<int:gid>/', PatokEdit, name='PatokEdit'),
]