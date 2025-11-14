from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer
from productstore.models import Product


class CartViewSet(viewsets.ViewSet):  # ✅ using ViewSet instead of ModelViewSet
    permission_classes = [permissions.IsAuthenticated]

    # GET /api/cart/cart/
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)

    # POST /api/cart/cart/add/
    @action(detail=False, methods=['post'])
    def add(self, request):
        product_id = request.data.get("product_id")
        qty = int(request.data.get("quantity", 1))

        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += qty
        cart_item.save()

        return Response({"message": "Added to cart"})

    # POST /api/cart/cart/remove/
    @action(detail=False, methods=['post'])
    def remove(self, request):
        product_id = request.data.get("product_id")
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"message": "Removed from cart"})
