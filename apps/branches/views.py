from rest_framework import generics
from .models import Branch
from .serializers import BranchSerializer
from apps.users.permissions import IsAdmin, IsHQManager, IsBranchManager


class BranchListCreateView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsBranchManager()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('active_only'):
            qs = qs.filter(is_active=True)
        return qs


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [IsBranchManager()]
