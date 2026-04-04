from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Sale, FuelPrice, Discount
from .serializers import SaleSerializer, FuelPriceSerializer, DiscountSerializer
from apps.users.permissions import IsAdmin, IsBranchManager, IsPompiste, IsHQStaff


class FuelPriceListCreateView(generics.ListCreateAPIView):
    queryset = FuelPrice.objects.select_related('set_by').all()
    serializer_class = FuelPriceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fuel_type']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsPompiste()]


class FuelPriceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FuelPrice.objects.all()
    serializer_class = FuelPriceSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [IsPompiste()]


class SaleListCreateView(generics.ListCreateAPIView):
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['branch', 'sale_type', 'fuel_type', 'date', 'shift']
    ordering_fields = ['date', 'amount', 'liters']
    ordering = ['-date']
    permission_classes = [IsPompiste]

    def get_queryset(self):
        qs = Sale.objects.select_related('branch', 'recorded_by', 'credit_customer').all()
        user = self.request.user
        if user.is_pompiste and user.branch:
            qs = qs.filter(branch=user.branch)
        elif user.is_branch_manager and user.branch:
            qs = qs.filter(branch=user.branch)
        return qs


class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.select_related('branch', 'recorded_by', 'credit_customer').all()
    serializer_class = SaleSerializer

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [IsBranchManager()]
        return [IsPompiste()]


class DiscountListCreateView(generics.ListCreateAPIView):
    queryset = Discount.objects.select_related('sale', 'applied_by').all()
    serializer_class = DiscountSerializer
    permission_classes = [IsBranchManager]


class DiscountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsBranchManager]
