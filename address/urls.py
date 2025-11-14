from rest_framework.routers import DefaultRouter
from .views import AddressViewSet


router = DefaultRouter()
router.register('address',AddressViewSet, basename="address")

urlpatterns = router.urls