from django.urls import path

from . import views

urlpatterns = [
    path('<str:email>/', views.create_transfer, name='transfer'),
]
