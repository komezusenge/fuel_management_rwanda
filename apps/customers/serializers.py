from rest_framework import serializers
from .models import CreditCustomer, CreditTransaction, Payment


class CreditCustomerSerializer(serializers.ModelSerializer):
    total_outstanding = serializers.ReadOnlyField()
    registered_by_name = serializers.SerializerMethodField()

    class Meta:
        model = CreditCustomer
        fields = [
            'id', 'company_name', 'driver_name', 'phone', 'plate_number',
            'branch', 'credit_limit', 'is_active', 'registered_by', 'registered_by_name',
            'notes', 'total_outstanding', 'created_at',
        ]
        read_only_fields = ['id', 'registered_by', 'created_at']

    def get_registered_by_name(self, obj):
        return obj.registered_by.get_full_name() if obj.registered_by else None

    def create(self, validated_data):
        validated_data['registered_by'] = self.context['request'].user
        return super().create(validated_data)


class CreditTransactionSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    recorded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = CreditTransaction
        fields = [
            'id', 'customer', 'customer_name', 'sale', 'fuel_type', 'liters',
            'price_per_liter', 'total_amount', 'status', 'recorded_by',
            'recorded_by_name', 'date', 'notes', 'created_at',
        ]
        read_only_fields = ['id', 'total_amount', 'recorded_by', 'created_at']

    def get_customer_name(self, obj):
        return obj.customer.company_name

    def get_recorded_by_name(self, obj):
        return obj.recorded_by.get_full_name() if obj.recorded_by else None

    def create(self, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        return super().create(validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    received_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'customer', 'customer_name', 'amount_paid', 'received_by',
            'received_by_name', 'date', 'notes', 'created_at',
        ]
        read_only_fields = ['id', 'received_by', 'created_at']

    def get_customer_name(self, obj):
        return obj.customer.company_name

    def get_received_by_name(self, obj):
        return obj.received_by.get_full_name() if obj.received_by else None

    def create(self, validated_data):
        validated_data['received_by'] = self.context['request'].user
        return super().create(validated_data)
