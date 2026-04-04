from django.urls import path
from . import views

urlpatterns = [
    path('', views.PumpListCreateView.as_view(), name='pump-list-create'),
    path('<int:pk>/', views.PumpDetailView.as_view(), name='pump-detail'),
    path('shifts/', views.ShiftRecordListCreateView.as_view(), name='shift-list-create'),
    path('shifts/<int:pk>/', views.ShiftRecordDetailView.as_view(), name='shift-detail'),
    path('shifts/<int:pk>/close/', views.close_shift, name='shift-close'),
]
