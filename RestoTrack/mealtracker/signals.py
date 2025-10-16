# apps/orders/signals.py
from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem, Order
from .models import Inventory  # adjust import to your inventory app

@receiver(post_save, sender=OrderItem)
def on_order_item_saved(sender, instance: OrderItem, created, **kwargs):
    """
    Recalculate the parent order totals whenever an OrderItem is created/updated.
    Also attempt to deduct inventory (select_for_update done elsewhere, typically in create flow).
    """
    order = instance.order
    order.calculate_totals()
    order.save()

    # Optional: deduct inventory immediately when an item is added (danger: race conditions)
    # Safer approach: deduct in serializer create() within a transaction using select_for_update()
    try:
        inv = InventoryItem.objects.get(branch=order.branch, sku=instance.menu_item.sku)
        # Note: this does not handle concurrency -- handle in serializer/service with select_for_update
        if inv.quantity >= instance.quantity:
            inv.quantity -= instance.quantity
            inv.save()
        else:
            # Depending on your policy, raise or flag low stock (we won't raise in signal)
            pass
    except InventoryItem.DoesNotExist:
        pass

@receiver(post_delete, sender=OrderItem)
def on_order_item_deleted(sender, instance: OrderItem, **kwargs):
    # Recalculate totals when an item is removed
    order = instance.order
    order.calculate_totals()
    order.save()
