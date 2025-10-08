from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import MenuItem, Table, Inventory, Order, Reservation
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    MenuItemSerializer,
    TableSerializer,
    InventorySerializer,
    OrderSerializer,
    ReservationSerializer,
)
from .permissions import IsStaffOrAdmin, IsAdmin


User = get_user_model()


# -------------------------------------------
# ✅ USER REGISTRATION
# -------------------------------------------
class RegisterView(CreateAPIView):
    """
    Public endpoint to register new customers.
    Staff/Admin should be created via admin panel or protected endpoint.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------------------
# ✅ MENU ITEMS (Public read, Staff/Admin modify)
# -------------------------------------------
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            return Response({'error': 'Only staff can add menu items'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


# -------------------------------------------
# ✅ TABLES (Staff/Admin only)
# -------------------------------------------
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


# -------------------------------------------
# ✅ INVENTORY (Staff/Admin only)
# -------------------------------------------
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]


# -------------------------------------------
# ✅ ORDERS (Customers create, Staff/Admin manage)
# -------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-timestamp')
    serializer_class = OrderSerializer

    def get_permissions(self):
        """
        - Customers: create orders
        - Staff/Admin: view, update, delete, change status
        """
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'update', 'partial_update', 'destroy', 'update_status']:
            permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsStaffOrAdmin])
    def update_status(self, request, pk=None):
        """
        Update order status (Staff/Admin only)
        """
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({'success': f'Order status updated to {new_status}'})


# -------------------------------------------
# ✅ RESERVATIONS (Customers can book, Staff/Admin manage)
# -------------------------------------------
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        """
        - Customers can create reservations
        - Staff/Admin can list, update, and delete
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsStaffOrAdmin]
        return [perm() for perm in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Create reservation only if table is free
        """
        table_id = request.data.get('table')
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return Response({'error': 'Table not found'}, status=status.HTTP_404_NOT_FOUND)

        if table.status != 'free':
            return Response({'error': 'Table not available'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark table as reserved
        table.status = 'reserved'
        table.save()

        return super().create(request, *args, **kwargs)
