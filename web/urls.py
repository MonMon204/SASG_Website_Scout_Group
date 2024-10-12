from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('registerinfo/', views.register_user_info, name='registerinfo'),
    path('profile/', views.profile, name='profile'),
    path('add-announcement/', views.add_announcement, name='add_announcement'),
    path('add-event/', views.add_event, name='add_event'),
    path('add-gallery/', views.add_gallery, name='add_gallery'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('my-district/', views.my_district, name='my_district'),
]