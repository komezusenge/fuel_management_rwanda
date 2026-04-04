from rest_framework import serializers
from .models import Pump, ShiftRecord


class PumpSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    tank_name = serializers.SerializerMethodField()
    fuel_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Pump
        fields = [
            'id', 'branch', 'branch_name', 'tank', 'tank_name',
            'name', 'fuel_type', 'fuel_type_display', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_tank_name(self, obj):
        return str(obj.tank) if obj.tank else None

    def get_fuel_type_display(self, obj):
        return obj.get_fuel_type_display()


class ShiftRecordSerializer(serializers.ModelSerializer):
    fuel_sold = serializers.ReadOnlyField()
    total_revenue = serializers.ReadOnlyField()
    pompiste_name = serializers.SerializerMethodField()
    pump_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = ShiftRecord
        fields = [
            'id', 'pompiste', 'pompiste_name', 'pump', 'pump_name', 'branch_name',
            'date', 'start_index', 'end_index', 'price_per_liter',
            'fuel_sold', 'total_revenue', 'notes', 'is_closed', 'created_at',
        ]
        read_only_fields = ['id', 'pompiste', 'is_closed', 'created_at']

    def get_pompiste_name(self, obj):
        return obj.pompiste.get_full_name()

    def get_pump_name(self, obj):
        return str(obj.pump)

    def get_branch_name(self, obj):
        return obj.pump.branch.name

    def validate(self, attrs):
        end_index = attrs.get('end_index')
        start_index = attrs.get('start_index')
        if end_index is not None and end_index < start_index:
            raise serializers.ValidationError({'end_index': 'End index cannot be less than start index.'})
        return attrs

    def create(self, validated_data):
        validated_data['pompiste'] = self.context['request'].user
        return super().create(validated_data)


class CloseShiftSerializer(serializers.Serializer):
    end_index = serializers.DecimalField(max_digits=12, decimal_places=2)
    notes = serializers.CharField(required=False, allow_blank=True)
