from django.urls import path
from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    ### Map Urls
    path('v1/account/loginRequest', ApiLoginRequest, name='ApiLoginRequest'),
    path('v1/map/block', ApiBlockBoundary, name='ApiBlockBoundary'),

]