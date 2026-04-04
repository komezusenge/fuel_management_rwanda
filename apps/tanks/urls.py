from django.urls import path
from . import views

urlpatterns = [
    path('', views.TankListCreateView.as_view(), name='tank-list-create'),
    path('<int:pk>/', views.TankDetailView.as_view(), name='tank-detail'),
    path('<int:pk>/add-fuel/', views.add_fuel_to_tank, name='tank-add-fuel'),
    path('restocking/', views.RestockingRequestListCreateView.as_view(), name='restocking-list-create'),
    path('restocking/<int:pk>/', views.RestockingRequestDetailView.as_view(), name='restocking-detail'),
    path('restocking/<int:pk>/approve/', views.approve_restocking_request, name='restocking-approve'),
]
