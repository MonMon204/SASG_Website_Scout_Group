from django.urls import path
from . import views

urlpatterns = [
    path('resources/', views.resources, name='resources'),
    path('camp_sites/', views.camp_sites, name='camp_sites'),
    path('resource/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('camp_site/<int:pk>/', views.camp_site_detail, name='camp_site_detail'),
]