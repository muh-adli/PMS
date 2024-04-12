from django.urls import path
from .views import LoginUser, Register, LogoutUser, LandingPage
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'rest', rmhViewSet, basename='rest')

urlpatterns = [
    path('', LandingPage, name='LandingPage'),
    path('register/', Register, name='Register'),
    path('login/', LoginUser, name='LoginUser'),
    path('logout/', LogoutUser, name='LogoutUser'),
]