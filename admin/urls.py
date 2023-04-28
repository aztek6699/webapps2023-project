from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin'),
    path('register_admin/', views.register_new_admin, name='register_admin'),
    path('all_user/', views.all_user, name='all_user'),
    path('all_transfer/', views.all_transfer, name='all_transfer'),
    path('all_request/', views.all_request, name='all_request'),
]
