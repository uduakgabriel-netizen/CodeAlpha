from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from decimal import Decimal


# ✅ BASE MODEL

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ✅ MENU MODEL

class MenuItem(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ✅ TABLE MODEL

class Table(TimeStampedModel):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number}"


# ✅ ORDER MODEL

class Order(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('served', 'Served'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    placed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    service_charge = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    note = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def calculate_totals(self, tax_rate=Decimal('0.075'), service_rate=Decimal('0.10')):
        items = self.items.all()
        subtotal = sum((item.line_total for item in items), Decimal('0.00'))
        tax = (subtotal * tax_rate).quantize(Decimal('0.01'))
        service_charge = (subtotal * service_rate).quantize(Decimal('0.01'))
        total = (subtotal + tax + service_charge).quantize(Decimal('0.01'))

        self.subtotal = subtotal
        self.tax = tax
        self.service_charge = service_charge
        self.total = total
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically recalculate totals after saving
        self.calculate_totals()
        super().save(update_fields=['subtotal', 'tax', 'service_charge', 'total'])


# ✅ ORDER ITEM MODEL

class OrderItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        indexes = [models.Index(fields=['order', 'menu_item'])]

    def save(self, *args, **kwargs):
        # Auto update line_total when saving
        self.unit_price = self.unit_price or self.menu_item.price
        self.line_total = (self.unit_price * self.quantity).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
        # Update order totals after saving item
        self.order.calculate_totals()
        self.order.save(update_fields=['subtotal', 'tax', 'service_charge', 'total'])

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity} (Order {self.order_id})"


# ✅ RESERVATION MODEL

class Reservation(TimeStampedModel):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    reservation_time = models.DateTimeField()
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Reservation for {self.customer_name} at {self.reservation_time}"


# ✅ INVENTORY MODEL

class Inventory(TimeStampedModel):
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    min_threshold = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.item_name
