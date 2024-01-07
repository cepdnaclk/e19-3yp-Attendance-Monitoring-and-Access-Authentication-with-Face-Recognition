from django.urls import path
from . import views

# URL Configuration
urlpatterns = [
    path('hello/', views.say_hello),
    path('detect/', views.compare_faces),
    path('publish/', views.publish_message),

]
