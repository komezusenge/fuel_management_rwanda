from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tank, TankRestockingRequest, RestockingRequestStatus
from .serializers import TankSerializer, TankRestockingRequestSerializer
from apps.users.permissions import IsAdmin, IsHQManager, IsBranchManager, IsBranchOrAbove


class TankListCreateView(generics.ListCreateAPIView):
    serializer_class = TankSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'fuel_type', 'status']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsBranchManager()]

    def get_queryset(self):
        qs = Tank.objects.select_related('branch').all()
        user = self.request.user
        if user.role in ['pompiste', 'branch_manager'] and user.branch:
            qs = qs.filter(branch=user.branch)
        return qs


class TankDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tank.objects.select_related('branch').all()
    serializer_class = TankSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsBranchManager()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsBranchManager()]


@api_view(['POST'])
@permission_classes([IsBranchManager])
def add_fuel_to_tank(request, pk):
    """Add fuel to a tank (restocking)."""
    try:
        tank = Tank.objects.get(pk=pk)
    except Tank.DoesNotExist:
        return Response({'detail': 'Tank not found.'}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity')
    if not quantity:
        return Response({'detail': 'Quantity is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        return Response({'detail': 'Invalid quantity.'}, status=status.HTTP_400_BAD_REQUEST)

    if quantity <= 0:
        return Response({'detail': 'Quantity must be positive.'}, status=status.HTTP_400_BAD_REQUEST)

    new_level = float(tank.current_level) + quantity
    if new_level > float(tank.capacity):
        return Response(
            {'detail': f'Adding {quantity}L would exceed tank capacity of {tank.capacity}L.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    tank.current_level = new_level
    tank.save()
    return Response(TankSerializer(tank).data)


class RestockingRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = TankRestockingRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'tank__branch']
    permission_classes = [IsBranchManager]

    def get_queryset(self):
        qs = TankRestockingRequest.objects.select_related(
            'tank__branch', 'requested_by', 'approved_by'
        ).all()
        user = self.request.user
        if user.role in ['pompiste', 'branch_manager'] and user.branch:
            qs = qs.filter(tank__branch=user.branch)
        return qs


class RestockingRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = TankRestockingRequest.objects.select_related(
        'tank__branch', 'requested_by', 'approved_by'
    ).all()
    serializer_class = TankRestockingRequestSerializer
    permission_classes = [IsBranchManager]


@api_view(['POST'])
@permission_classes([IsHQManager])
def approve_restocking_request(request, pk):
    """Approve or reject a restocking request."""
    try:
        req = TankRestockingRequest.objects.get(pk=pk)
    except TankRestockingRequest.DoesNotExist:
        return Response({'detail': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

    action = request.data.get('action')
    if action not in ['approve', 'reject']:
        return Response({'detail': 'Action must be approve or reject.'}, status=status.HTTP_400_BAD_REQUEST)

    if req.status != RestockingRequestStatus.PENDING:
        return Response({'detail': 'Request is not pending.'}, status=status.HTTP_400_BAD_REQUEST)

    req.approved_by = request.user
    req.notes = request.data.get('notes', req.notes)
    req.status = RestockingRequestStatus.APPROVED if action == 'approve' else RestockingRequestStatus.REJECTED
    req.save()
    return Response(TankRestockingRequestSerializer(req).data)
