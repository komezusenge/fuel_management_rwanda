from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Pump, ShiftRecord
from .serializers import PumpSerializer, ShiftRecordSerializer, CloseShiftSerializer
from apps.users.permissions import IsAdmin, IsBranchManager, IsPompiste, IsBranchOrAbove


class PumpListCreateView(generics.ListCreateAPIView):
    serializer_class = PumpSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'fuel_type', 'is_active']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBranchManager()]
        return [IsPompiste()]

    def get_queryset(self):
        qs = Pump.objects.select_related('branch', 'tank').all()
        user = self.request.user
        if user.role in ['pompiste', 'branch_manager'] and user.branch:
            qs = qs.filter(branch=user.branch)
        return qs


class PumpDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pump.objects.select_related('branch', 'tank').all()
    serializer_class = PumpSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsBranchManager()]
        return [IsPompiste()]


class ShiftRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = ShiftRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pump', 'date', 'is_closed', 'pump__branch']
    permission_classes = [IsPompiste]

    def get_queryset(self):
        qs = ShiftRecord.objects.select_related('pompiste', 'pump__branch').all()
        user = self.request.user
        if user.is_pompiste:
            qs = qs.filter(pompiste=user)
        elif user.is_branch_manager and user.branch:
            qs = qs.filter(pump__branch=user.branch)
        return qs


class ShiftRecordDetailView(generics.RetrieveUpdateAPIView):
    queryset = ShiftRecord.objects.select_related('pompiste', 'pump__branch').all()
    serializer_class = ShiftRecordSerializer
    permission_classes = [IsPompiste]


@api_view(['POST'])
@permission_classes([IsPompiste])
def close_shift(request, pk):
    """Close a shift by entering the end meter reading."""
    try:
        shift = ShiftRecord.objects.get(pk=pk)
    except ShiftRecord.DoesNotExist:
        return Response({'detail': 'Shift not found.'}, status=status.HTTP_404_NOT_FOUND)

    if shift.pompiste != request.user and not request.user.is_branch_manager:
        return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CloseShiftSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        shift.close_shift(serializer.validated_data['end_index'])
    except ValueError:
        return Response(
            {'detail': 'Invalid end index: must be greater than or equal to the start index, and shift must not already be closed.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if serializer.validated_data.get('notes'):
        shift.notes = serializer.validated_data['notes']
        shift.save(update_fields=['notes'])

    # Deduct fuel from tank if pump is linked to a tank
    if shift.pump.tank:
        tank = shift.pump.tank
        new_level = float(tank.current_level) - shift.fuel_sold
        tank.current_level = max(new_level, 0)
        tank.save()

    return Response(ShiftRecordSerializer(shift).data)
