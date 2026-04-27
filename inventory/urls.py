from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'waste', views.WasteViewSet, basename='waste')

urlpatterns = [
    path('', include(router.urls)),
]