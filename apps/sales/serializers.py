from rest_framework import serializers
from .models import Sale, FuelPrice, Discount


class FuelPriceSerializer(serializers.ModelSerializer):
    fuel_type_display = serializers.SerializerMethodField()
    set_by_name = serializers.SerializerMethodField()

    class Meta:
        model = FuelPrice
        fields = ['id', 'fuel_type', 'fuel_type_display', 'price_per_liter', 'set_by', 'set_by_name', 'effective_from', 'notes']
        read_only_fields = ['id', 'set_by', 'effective_from']

    def get_fuel_type_display(self, obj):
        return obj.get_fuel_type_display()

    def get_set_by_name(self, obj):
        return obj.set_by.get_full_name() if obj.set_by else None

    def create(self, validated_data):
        validated_data['set_by'] = self.context['request'].user
        return super().create(validated_data)


class SaleSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    recorded_by_name = serializers.SerializerMethodField()
    credit_customer_name = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = [
            'id', 'shift', 'branch', 'branch_name', 'sale_type', 'fuel_type',
            'liters', 'price_per_liter', 'amount', 'recorded_by', 'recorded_by_name',
            'credit_customer', 'credit_customer_name', 'date', 'notes',
            'discount_amount', 'created_at',
        ]
        read_only_fields = ['id', 'amount', 'recorded_by', 'created_at']

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_recorded_by_name(self, obj):
        return obj.recorded_by.get_full_name() if obj.recorded_by else None

    def get_credit_customer_name(self, obj):
        return obj.credit_customer.company_name if obj.credit_customer else None

    def get_discount_amount(self, obj):
        if hasattr(obj, 'discount'):
            return obj.discount.discount_amount
        return None

    def validate(self, attrs):
        if attrs.get('sale_type') == 'credit' and not attrs.get('credit_customer'):
            raise serializers.ValidationError({'credit_customer': 'Credit customer is required for credit sales.'})
        return attrs

    def create(self, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        return super().create(validated_data)


class DiscountSerializer(serializers.ModelSerializer):
    applied_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ['id', 'sale', 'discount_amount', 'applied_by', 'applied_by_name', 'reason', 'created_at']
        read_only_fields = ['id', 'applied_by', 'created_at']

    def get_applied_by_name(self, obj):
        return obj.applied_by.get_full_name() if obj.applied_by else None

    def create(self, validated_data):
        validated_data['applied_by'] = self.context['request'].user
        return super().create(validated_data)
