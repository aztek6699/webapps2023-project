from django.urls import path

from . import views

urlpatterns = [
    path('create_request/<str:email>/', views.create_request, name='create_request'),
    path('pending_requests/', views.pending_request, name='pending_requests'),
    path('accept/<int:req_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:req_id>/', views.reject_request, name='reject_request'),
    path('cancel/<int:req_id>/', views.cancel_request, name='cancel_request'),
]
