from rest_framework import serializers
from .models import MenuItem, Table, Inventory, Order, OrderItem, Reservation
from django.contrib.auth import get_user_model
from rest_framework import serializers



User = get_user_model()

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



class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    is_low = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_detail', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    table_detail = TableSerializer(source='table', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'table', 'table_detail', 'items', 'total_price', 'status', 'timestamp']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        total = 0
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
            total += menu_item.price * quantity

        order.total_price = total
        order.save()
        return order


class ReservationSerializer(serializers.ModelSerializer):
    table_detail = TableSerializer(source='table', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
