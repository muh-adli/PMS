from django.urls import path
from .views import Register, LogoutUser, LandingPage


urlpatterns = [
    path('', LandingPage, name='LandingPage'),
    path('register/', Register, name='Register'),
    path('logout/', LogoutUser, name='LogoutUser'),
]