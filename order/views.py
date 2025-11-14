from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderSerializers, OrderStatusUpdateSerializer
from cart.models import Cart, CartItem
from address.models import Address
from productstore.models import Product
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')  # fixed quotes

    @transaction.atomic
    @action(detail=False, methods=['post'])  # must be lowercase 'post'
    def create_from_cart(self, request):
        user = request.user
        address_id = request.data.get("address_id")

        if not address_id:
            return Response({"error": "Address is required"}, status=400)

        # ✅ validate address
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return Response({"error": "Invalid address"}, status=404)

        # ✅ fetch cart
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart is empty"}, status=400)

        # ✅ note: 'Objects' → 'objects' (case sensitive)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "No items in cart"}, status=400)

        # ✅ create order
        order = Order.objects.create(
            user=user,
            address=address,
            payment_method=request.data.get("payment_method", "COD"),
            status="PENDING"
        )

        total_price = 0

        # ✅ create order items
        for item in cart_items:
            if item.product.stock < item.quantity:
                return Response({"error": f"{item.product.name} is out of stock"}, status=400)

            price = item.product.price
            total_price += price * item.quantity

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=price
            )

            # ✅ reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # ✅ update order total
        order.total_price = total_price
        order.save()

        # ✅ clear cart
        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def pay_now(self, request, pk=None):
            try:
                order = Order.objects.get(id=pk, user=request.user)
            except Order.DoesNotExist:
                return Response({"error": "Order not found"}, status=404)

            if order.status != "PENDING":
                return Response({"error": "Order already paid or cancelled"}, status=400)

            order.status = "PAID"
            order.save()

            return Response({"message": "Payment marked as successful", "order_id": order.id}, status=status.HTTP_200_OK)

class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializers
    permission_classes = [IsAdminUser]

class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]