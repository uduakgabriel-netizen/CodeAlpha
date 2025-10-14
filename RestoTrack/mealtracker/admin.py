from django.contrib import admin

from .models import Table, MenuItem, Order, OrderItem, Reservation, Inventory


# ✅ Inline: Allows adding OrderItems directly inside an Order in admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('menu_item', 'quantity', 'unit_price', 'line_total')
    readonly_fields = ('line_total',)


# ✅ Customize Order admin panel
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'status', 'subtotal', 'tax', 'service_charge', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'table__number')
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Auto-recalculate totals after saving
        obj.calculate_totals()
        obj.save()


# ✅ MenuItem admin
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'created_at', 'updated_at')
    list_filter = ('available',)
    search_fields = ('name',)


# ✅ Table admin
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_available', 'created_at')
    list_filter = ('is_available',)
    search_fields = ('number',)


# ✅ Inventory admin
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'min_threshold', 'is_low')
    list_filter = ('item_name',)
    search_fields = ('item_name',)

    def is_low(self, obj):
        return obj.quantity <= obj.min_threshold
    is_low.boolean = True
    
    
# ✅ Reservation admin
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'table', 'reservation_time', 'status')
    list_filter = ('status',)
    search_fields = ('customer_name', 'table__number')
