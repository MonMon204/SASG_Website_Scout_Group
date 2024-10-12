from django.urls import path
from . import views

urlpatterns = [
    path('', views.badges_home, name='badges_home'),
    path('badge_details/<int:id>/', views.badge_details, name='badge_details'),
    path('apply_badge/<int:badge_id>/', views.apply_badge, name='apply_badge'),
    path('badge_grading/', views.badge_grading, name='badge_grading'),
    path('badge_grading/<int:member_id>/<int:badge_id>/', views.badge_grading_details, name='badge_grading_details'),
]