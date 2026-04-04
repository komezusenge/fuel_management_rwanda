from django.urls import path
from . import views

urlpatterns = [
    path('', views.SaleListCreateView.as_view(), name='sale-list-create'),
    path('<int:pk>/', views.SaleDetailView.as_view(), name='sale-detail'),
    path('prices/', views.FuelPriceListCreateView.as_view(), name='fuel-price-list-create'),
    path('prices/<int:pk>/', views.FuelPriceDetailView.as_view(), name='fuel-price-detail'),
    path('discounts/', views.DiscountListCreateView.as_view(), name='discount-list-create'),
    path('discounts/<int:pk>/', views.DiscountDetailView.as_view(), name='discount-detail'),
]
