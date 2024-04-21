from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    path('HomePage/', HomePage, name='HomePage'),
    ## Dashboard Jangkos
    path('jangkos/', jangkos, name='jangkos'),
    path('jangkos/table/', JangkosTable, name='JangkosTable'),
    path('jangkos/table/edit/<int:gid>/', JangkosEdit, name='JangkosEdit'),
    ## Dashboard Pupuk
    path('pupuk/', pupuk, name='pupuk'),
    ## Dashboard Monitoring
    path('monitoring/', Monitoring, name='Monitoring'),
    path('monitoring/patok/table/', PatokTable, name='PatokTable'),
    path('monitoring/patok/table/<int:gid>/', PatokEdit, name='PatokEdit'),
]