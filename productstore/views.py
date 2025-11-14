from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
# Create your views here.
from .models import Category, Tag, Product
from .serializers import CategorySerializer, TagSerializer, ProductSerializer
from .pagination import Pagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny] 
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny] 
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = Pagination

    #Only logged in users can create/edit/delete
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny] 

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter, filters.SearchFilter]

    #used for filtering fields
    filterset_fields =['category', 'tags','is_active','stock']

    #filter used for ordering
    ordering_fields = ['price','created_at', 'stock']

    #default ordeing(optional)
    ordering = ['-created_at']

    #search on name+description
    search_fields = ['name','description']

    def get_queryset(self):
        queryset = Product.objects.all()

        #price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
    
        return queryset
        
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)