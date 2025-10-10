from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MenuItemViewSet, TableViewSet, InventoryViewSet,
    OrderViewSet, ReservationViewSet, RegisterView,LoginView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('menu', MenuItemViewSet)
router.register('tables', TableViewSet)
router.register('inventory', InventoryViewSet)
router.register('orders', OrderViewSet)
router.register('reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/',LoginView.as_view(),name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
