from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    ### Map Urls
    path('HectareStatement/', MapHectare, name='MapHectare'),

    ### API Urls
    ## Boundary
    path('api/v1/hgu/', HGUBoundary, name='HGUBoundary'),
    path('api/v1/afdeling/', AfdelingBoundary, name='AfdelingBoundary'),
    path('api/v1/block/', BlockBoundary, name='BlockBoundary'),
    path('api/v1/jangkos/', JangkosData, name='JangkosData'),
    path('api/v1/planted/', PlantedData, name='PlantedData'),

    ## Point
    path('api/v1/jembatan/', JembatanData, name='JembatanData'),
    path('api/v1/patok/', PatokData, name='PatokData'),

    ## Tankos
    path('api/v1/aplikasi/', TankosAplikasi, name='AplikasiData'),
    path('api/v1/dump/', TankosDump, name='DumpData'),

]