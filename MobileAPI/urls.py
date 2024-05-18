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

    ### Data Urls
    path('v1/data/patok', ApiPatokData, name='ApiPatokData'),
    path('v1/data/planted', ApiPlantedData, name='ApiPlantedData'),
    path('v1/data/dump', ApiDumpData, name='ApiDumpData'),

]