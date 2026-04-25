from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'waste', views.WasteViewSet, basename='waste')

urlpatterns = [
    path('', include(router.urls)),
]