from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'shift', views.ShiftViewSet, basename='shift')
router.register(r'order-audit-log', views.OrderAuditLogViewSet, basename='orderauditlog')
router.register(r'employee-kpi', views.EmployeeKPIViewSet, basename='employeekpi')

urlpatterns = [
    path('', include(router.urls)),
]
