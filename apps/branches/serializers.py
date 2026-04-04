from rest_framework import serializers
from .models import Branch


class BranchSerializer(serializers.ModelSerializer):
    staff_count = serializers.SerializerMethodField()
    tank_count = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = ['id', 'name', 'location', 'phone', 'is_active', 'staff_count', 'tank_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_staff_count(self, obj):
        return obj.staff.filter(is_active=True).count()

    def get_tank_count(self, obj):
        return obj.tanks.count()
