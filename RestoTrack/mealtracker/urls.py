
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    MenuItemViewSet,
    TableViewSet,
    InventoryViewSet,
    OrderViewSet,
    ReservationViewSet,
    RegisterView,
    LoginView,
)

# ------------------------------------------------------------
# ✅ DRF Router for ViewSets
# ------------------------------------------------------------
router = DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'reservations', ReservationViewSet, basename='reservations')

# ------------------------------------------------------------
# ✅ URL Patterns
# ------------------------------------------------------------
urlpatterns = [
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # JWT Token endpoints (optional but useful for mobile apps / frontend)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
