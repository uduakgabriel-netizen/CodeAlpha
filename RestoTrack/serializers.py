from rest_framework import serializers
from .models import Order, Table, Orderitems, Reservertion, Inventory, menuItem

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
class TableSerialization(serializers.ModelSerialiser):
    class Meta:
        model = Table
        fields = '__all__'



class OrderItemsSerializer(serializers.ModelSerializer):
    class meta:
        model = Orderitems
        fields = '__all__'
        

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservertion
        fields = '__all__'
        
        
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = menuItem
        fields = '__all__'
        

