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

    ### Data Urls
    path('v1/data/patok', ApiPatokData, name='ApiPatokData'),
    path('v1/data/planted', ApiPlantedData, name='ApiPlantedData'),
    path('v1/data/dump', ApiDumpData, name='ApiDumpData'),
    path('v1/save/dump/<int:gid>', ApiSaveDump, name='ApiSaveDump'),
    path('v1/data/apl', ApiAplData, name='ApiAplData'),

]