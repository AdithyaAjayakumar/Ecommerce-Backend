from rest_framework import serializers
from .models import Order, OrderItem
from address.serializers import AddressSerializer #optional if we want nexted address view


class OrderItemSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(source="Product.name", read_only=True)
    product_price = serializers.DecimalField(source="price", read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['id','product','product_name','product_price', 'quantity','price']

class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True,read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'total_price', 'status', 'payment_method', 'items', 'created_at']
        read_only_fields = ['user', 'total_price', 'status', 'created_at']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']