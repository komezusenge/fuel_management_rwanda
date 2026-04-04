from rest_framework import serializers
from .models import Tank, TankRestockingRequest


class TankSerializer(serializers.ModelSerializer):
    fill_percentage = serializers.ReadOnlyField()
    available_space = serializers.ReadOnlyField()
    branch_name = serializers.SerializerMethodField()
    fuel_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Tank
        fields = [
            'id', 'branch', 'branch_name', 'name', 'fuel_type', 'fuel_type_display',
            'capacity', 'current_level', 'minimum_threshold', 'status',
            'fill_percentage', 'available_space', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_fuel_type_display(self, obj):
        return obj.get_fuel_type_display()


class TankRestockingRequestSerializer(serializers.ModelSerializer):
    tank_name = serializers.SerializerMethodField()
    requested_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = TankRestockingRequest
        fields = [
            'id', 'tank', 'tank_name', 'branch_name', 'requested_by', 'requested_by_name',
            'approved_by', 'approved_by_name', 'requested_quantity', 'delivered_quantity',
            'status', 'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'requested_by', 'approved_by', 'status', 'created_at', 'updated_at']

    def get_tank_name(self, obj):
        return str(obj.tank)

    def get_branch_name(self, obj):
        return obj.tank.branch.name

    def get_requested_by_name(self, obj):
        return obj.requested_by.get_full_name() if obj.requested_by else None

    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name() if obj.approved_by else None

    def create(self, validated_data):
        validated_data['requested_by'] = self.context['request'].user
        return super().create(validated_data)
