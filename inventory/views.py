from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from django.db.models import Count
from .serializers import *
from users.permissions import IsBossOrReadOnly, IsManagerOrReadOnly

# -- -- -- -- -- -- -- -- -- -- 
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class   = ProductSerializer
    permission_classes = [IsManagerOrReadOnly]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields   = ['unit'] # kg yoki litr yoki dona boyicha hisoblash
    search_fields      = ['name']
    ordering_fields    = ['quantity', 'price']

    def get_queryset(self):
        return Product.objects.filter(restaurant=self.request.user.profile.restaurant).order_by('name')
    
    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)

# -- -- -- -- -- -- -- -- -- -- 
class WasteViewSet(viewsets.ModelViewSet):
    serializer_class   = WasteSerializer
    permission_classes = [IsManagerOrReadOnly]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields   = ['reason', 'responsible_person', 'product', 'menu_item']

    def get_queryset(self):
        return Waste.objects.filter(
            restaurant=self.request.user.profile.restaurant
        ).select_related(
            'product', 'menu_item', 'responsible_person'
            ).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)
        







