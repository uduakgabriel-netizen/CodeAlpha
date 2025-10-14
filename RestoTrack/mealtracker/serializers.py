from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal
from .models import MenuItem, Table, Inventory, Order, OrderItem, Reservation

User = get_user_model()

# -----------------------------
# ✅ USER SERIALIZERS
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)


# -----------------------------
# ✅ MENU & TABLE SERIALIZERS
# -----------------------------
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


# -----------------------------
# ✅ INVENTORY SERIALIZER
# -----------------------------
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


# -----------------------------
# ✅ RESERVATION SERIALIZER
# -----------------------------
class ReservationSerializer(serializers.ModelSerializer):
    table_detail = TableSerializer(source='table', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'


# -----------------------------
# ✅ ORDER & ORDER ITEM SERIALIZERS
# -----------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_detail', 'quantity', 'unit_price', 'line_total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table_detail = TableSerializer(source='table', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'table', 'table_detail', 'placed_by', 'status',
            'subtotal', 'tax', 'service_charge', 'total', 'note', 'created_at', 'items'
        ]
        read_only_fields = ['subtotal', 'tax', 'service_charge', 'total', 'created_at']


# -----------------------------
# ✅ ORDER CREATION LOGIC (MAIN ORDERING SYSTEM)
# -----------------------------

class OrderItemCreateSerializer(serializers.Serializer):
    menu_item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)



class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'status', 'items']
        read_only_fields = ['id']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(placed_by=user, **validated_data)
            total = Decimal('0.00')

            for item in items_data:
                menu_item = MenuItem.objects.select_for_update().get(id=item['menu_item_id'])
                qty = item['quantity']
                unit_price = menu_item.price

                # --- Inventory check ---
                try:
                    inventory = Inventory.objects.select_for_update().get(item_name=menu_item.name)
                    if inventory.quantity < qty:
                        raise serializers.ValidationError(
                            f"Not enough stock for {menu_item.name}. Available: {inventory.quantity}"
                        )
                    inventory.quantity -= qty
                    inventory.save()
                except Inventory.DoesNotExist:
                    raise serializers.ValidationError(f"No inventory record found for {menu_item.name}")

                # --- Create OrderItem ---
                line_total = (unit_price * qty).quantize(Decimal('0.01'))
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=qty,
                    unit_price=unit_price,
                    line_total=line_total
                )

                total += line_total

            order.calculate_totals()
            order.save()

        return order
