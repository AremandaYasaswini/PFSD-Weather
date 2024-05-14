from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('weather/', views.weather, name='weather'),
    path('weather-results/', views.weather_results, name='weather_results'),
    path('signup/', views.signup, name='signup'),
]