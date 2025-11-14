from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'products',ProductViewSet)
router.register('categories',CategoryViewSet)
router.register('tags',TagViewSet)
urlpatterns = router.urls