from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.db.models import Count
from .serializers import *
from users.permissions import IsBossOrReadOnly, IsManagerOrReadOnly

# -- -- -- -- -- -- -- -- -- -- 
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class   =  CategorySerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('items')
                        ).select_related('restaurant').order_by('name')

# -- -- -- -- -- -- -- -- -- -- 
class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class   = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return MenuItem.objects.select_related('category', 'restaurant').order_by('name')
    
# -- -- -- -- -- -- -- -- -- -- 
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class   = OrderSerializer
    permission_classes = [IsManagerOrReadOnly] 

    def get_queryset(self):
        return Order.objects.select_related('cashier', 'shift').prefetch_related(
            'order_items').order_by('-unique_num')
    
    def perform_create(self, serializer):
        serializer.save(cashier=self.request.user)
        # buyurtma kiritilganda - avtomatik tekshirtirildi

# -- -- -- -- -- -- -- -- -- -- 
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return Transaction.objects.select_related('order').order_by('-paid_at')

