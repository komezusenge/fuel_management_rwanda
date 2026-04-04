from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreditCustomerListCreateView.as_view(), name='customer-list-create'),
    path('<int:pk>/', views.CreditCustomerDetailView.as_view(), name='customer-detail'),
    path('<int:pk>/balance/', views.customer_balance, name='customer-balance'),
    path('transactions/', views.CreditTransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', views.CreditTransactionDetailView.as_view(), name='transaction-detail'),
    path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
]
