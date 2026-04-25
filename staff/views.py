from rest_framework import status, viewsets, filters
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
class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class   = ShiftSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return Shift.objects.filter(restaurant=self.request.user.profile.restaurant)
            # faqat o'zini restoraninigina smenasini ko'ra oladi !
    
    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)
            # Smena ochilayatganda avtomatik restoranni biriktiramiz

# -- -- -- -- -- -- -- -- -- -- 
class OrderAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = OrderAuditLogSerializer
    permission_classes = [IsManagerOrReadOnly] 

    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['situation', 'order', 'editor']
    search_fields    = ['description', 'new_data']
    ordering_fields  = ['created_at']

    def get_queryset(self):
        # faqat o'z restoranni log'larini ko'rsatish
        return OrderAuditLog.objects.filter(
            restaurant=self.request.user.profile.restaurant
        ).select_related('order', 'editor').order_by('-id')
    
# -- -- -- -- -- -- -- -- -- -- 
class EmployeeKPIViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = EmployeeKPISerializer 
    permission_classes = [IsBossOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['user__username']
    ordering_fields = ['salary', 'bonus_kpi']

    def get_queryset(self):
        return EmployeeKPI.objects.filter(
            restaurant=self.request.user.profile.restaurant
        ).select_related('user').order_by('user__username')

