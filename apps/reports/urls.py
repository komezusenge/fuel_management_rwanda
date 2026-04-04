from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.daily_report, name='daily-report'),
    path('monthly/', views.monthly_report, name='monthly-report'),
    path('dashboard/', views.hq_dashboard, name='hq-dashboard'),
    path('financial/', views.financial_report, name='financial-report'),
]
