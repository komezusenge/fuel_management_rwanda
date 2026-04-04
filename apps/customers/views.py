from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import CreditCustomer, CreditTransaction, Payment
from .serializers import CreditCustomerSerializer, CreditTransactionSerializer, PaymentSerializer
from apps.users.permissions import IsPompiste, IsBranchManager, IsHQStaff, IsAccountant


class CreditCustomerListCreateView(generics.ListCreateAPIView):
    serializer_class = CreditCustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['branch', 'is_active']
    search_fields = ['company_name', 'driver_name', 'phone', 'plate_number']
    permission_classes = [IsPompiste]

    def get_queryset(self):
        qs = CreditCustomer.objects.select_related('branch', 'registered_by').all()
        user = self.request.user
        if user.is_pompiste and user.branch:
            qs = qs.filter(branch=user.branch)
        elif user.is_branch_manager and user.branch:
            qs = qs.filter(branch=user.branch)
        return qs


class CreditCustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreditCustomer.objects.select_related('branch', 'registered_by').all()
    serializer_class = CreditCustomerSerializer
    permission_classes = [IsPompiste]


class CreditTransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = CreditTransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'status', 'fuel_type', 'date']
    permission_classes = [IsPompiste]

    def get_queryset(self):
        qs = CreditTransaction.objects.select_related('customer', 'recorded_by').all()
        user = self.request.user
        if user.is_pompiste and user.branch:
            qs = qs.filter(customer__branch=user.branch)
        elif user.is_branch_manager and user.branch:
            qs = qs.filter(customer__branch=user.branch)
        return qs


class CreditTransactionDetailView(generics.RetrieveUpdateAPIView):
    queryset = CreditTransaction.objects.select_related('customer', 'recorded_by').all()
    serializer_class = CreditTransactionSerializer
    permission_classes = [IsBranchManager]


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'date']
    permission_classes = [IsBranchManager]

    def get_queryset(self):
        qs = Payment.objects.select_related('customer', 'received_by').all()
        user = self.request.user
        if user.is_branch_manager and user.branch:
            qs = qs.filter(customer__branch=user.branch)
        return qs


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.select_related('customer', 'received_by').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsBranchManager]


@api_view(['GET'])
@permission_classes([IsBranchManager])
def customer_balance(request, pk):
    """Get outstanding balance for a specific customer."""
    try:
        customer = CreditCustomer.objects.get(pk=pk)
    except CreditCustomer.DoesNotExist:
        return Response({'detail': 'Customer not found.'}, status=404)

    from django.db.models import Sum
    total_charged = customer.transactions.aggregate(total=Sum('total_amount'))['total'] or 0
    total_paid = customer.payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    outstanding = float(total_charged) - float(total_paid)

    return Response({
        'customer_id': customer.pk,
        'company_name': customer.company_name,
        'total_charged': float(total_charged),
        'total_paid': float(total_paid),
        'outstanding_balance': outstanding,
        'credit_limit': float(customer.credit_limit),
    })
