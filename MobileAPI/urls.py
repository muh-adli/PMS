from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    ### Login Urls
    path('v1/account/loginRequest', ApiLoginRequest, name='ApiLoginRequest'),

    ### Map Urls
    path('v1/map/block', ApiBlockBoundary, name='ApiBlockBoundary'),
    path('v1/map/dump', ApiDumpBoundary, name='ApiDumpBoundary'),
    path('v1/map/hgu', ApiHguBoundary, name='ApiHguBoundary'),
    path('v1/map/afdeling', ApiAfdelingBoundary, name='ApiAfdelingBoundary'),
    path('v1/map/planted', ApiPlantedBoundary, name='ApiPlantedBoundary'),
    path('v1/map/road', ApiRoadBoundary, name='ApiRoadBoundary'),
    path('v1/map/bridge', ApiBridgeBoundary, name='ApiBridgeBoundary'),
    path('v1/map/patok', ApiPatokBoundary, name='ApiPatokBoundary'),

    ### Data Urls
    path('v1/data/patok', ApiPatokData, name='ApiPatokData'),
    path('v1/save/patok/<int:gid>', ApiSavePatok, name='ApiSavePatok'),
    path('v1/data/planted', ApiPlantedData, name='ApiPlantedData'),
    path('v1/data/dump', ApiDumpData, name='ApiDumpData'),
    path('v1/save/dump/<int:gid>', ApiSaveDump, name='ApiSaveDump'),
    path('v1/data/apl', ApiAplData, name='ApiAplData'),
    path('v1/tankos/chart', ApiTankosChart, name='ApiTankosChart'),

    
    path('v2/tankos/dump', APITankosDump, name='APITankosDump'),
]