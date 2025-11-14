from django.shortcuts import render
from .serializers import AddressSerializer
from rest_framework import viewsets, permissions
from .models import Address
# Create your views here.



class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)