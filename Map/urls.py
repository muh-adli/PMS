from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    ### Map Urls
    path('hectarestatement/', MapHectare, name='MapHectare'),

    ### API Urls
    ## Polygon
    path('api/v1/hgu/', HGUBoundary, name='HGUBoundary'),
    path('api/v1/afdeling/', AfdelingBoundary, name='AfdelingBoundary'),
    path('api/v1/block/', BlockBoundary, name='BlockData'),
    # path('api/v1/jangkos/', JangkosData, name='JangkosData'),
    path('api/v1/planted/', PlantedData, name='PlantedData'),
    
    path('api/v2/apl/', AplDataV2, name='Apl_v2'),
    path('api/v2/planted/', PlantedDataV2, name='PlantedDataV2'),
    path('api/v2/block/', BlockDataV2, name='BlockDataV2'),

    ## Line
    path('api/v1/road/', RoadData, name='RoadData'), ## TODO: serialize multiline data

    ## Point
    path('api/v1/jembatan/', JembatanData, name='JembatanData'),
    path('api/v1/patok/', PatokData, name='PatokData'),
    path('api/v1/dump/', DumpData, name='DumpData'),
    path('api/v2/dump/', DumpDataV2, name='Dump_v2'),
    

]