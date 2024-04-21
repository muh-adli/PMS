from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    path('HomePage/', HomePage, name='HomePage'),
    ## Dashboard Jangkos
    path('dasboard/center/', center, name='center'),
    ## Dashboard Jangkos
    path('dasboard/jangkos/', jangkos, name='jangkos'),
    path('dasboard/jangkos/table/', JangkosTable, name='JangkosTable'),
    path('dasboard/jangkos/table/edit/<int:gid>/', JangkosEdit, name='JangkosEdit'),
    ## Dashboard Pupuk
    path('dasboard/pupuk/', pupuk, name='pupuk'),
    ## Dashboard Monitoring
    path('dasboard/monitoring/', Monitoring, name='Monitoring'),
    path('monitoring/patok/table/', PatokTable, name='PatokTable'),
    path('monitoring/patok/table/<int:gid>/', PatokEdit, name='PatokEdit'),
]