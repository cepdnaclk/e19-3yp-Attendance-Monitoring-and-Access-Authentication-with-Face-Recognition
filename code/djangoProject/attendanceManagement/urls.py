from django.urls import path
from . import views

# URL Configuration
urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),
    path('configure/', views.ConfigureDeviceView.as_view(), name='configure')
]
