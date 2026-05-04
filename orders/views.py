from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Sum
from .serializers import *
from users.permissions import IsBossOrReadOnly, IsManagerOrReadOnly

# -- -- -- -- -- -- -- -- -- -- 
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class   =  CategorySerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('items')
                        ).select_related('restaurant').order_by('name')
    
    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)

# -- -- -- -- -- -- -- -- -- -- 
class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class   = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        return MenuItem.objects.select_related('category', 'restaurant').order_by('name')
    
    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.profile.restaurant)

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

# -- -- -- -- -- -- -- -- -- -- 
class BossDashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        restaurant = request.user.profile.restaurant

        # 1. All orders daily
        daily_revenue = Order.objects.filter(
            restaurant = restaurant,
            created_at__date = today,
            status = 'completed'
        ).aggregate(total=Sum('total_price'))['total'] or 0

        # 2. All current active orders 
        active_orders_count = Order.objects.filter(
            restaurant = restaurant,
            status__in = ['pending', 'processing']
        ).count()

        # 3. Best seller product in today
        return Response({
            'daily_revenue': daily_revenue,
            'active_orders': active_orders_count,
            'restaurant_name': restaurant.name,
            'date': today
        })

# -- -- -- -- -- -- -- -- -- -- 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk, restaurant=request.user.profile.restaurant)
        new_status = request.data.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return Response({"status": "updated"})
        return Response({"error": "No status provided"}, status=404)
    except Order.DoesNotExist:
        return Response({"status": "not found"}, status=404)
    








