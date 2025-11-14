from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    AdminOrderListView,
    AdminOrderStatusUpdateView
)

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path("admin/orders/", AdminOrderListView.as_view(), name="admin-orders"),
    path("admin/orders/<int:pk>/status/", AdminOrderStatusUpdateView.as_view(), name="admin-order-status"),
]

urlpatterns += router.urls