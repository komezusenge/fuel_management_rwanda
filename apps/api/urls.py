from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Users
    path('users/', include('apps.users.urls')),

    # Branches
    path('branches/', include('apps.branches.urls')),

    # Tanks
    path('tanks/', include('apps.tanks.urls')),

    # Pumps & Shifts
    path('pumps/', include('apps.pumps.urls')),

    # Sales, Prices, Discounts
    path('sales/', include('apps.sales.urls')),

    # Customers & Credit
    path('customers/', include('apps.customers.urls')),

    # Reports & Dashboard
    path('reports/', include('apps.reports.urls')),
]
