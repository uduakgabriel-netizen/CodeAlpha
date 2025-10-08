from django.db import models
from django.contrib.auth.models import AbstractUser


class menuItem(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    availability = models.BooleanField()


    def __str__(self):
        return self.name


class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()

    status_choices = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ]
    
    status = models.CharField(max_length=10, choices=status_choices, default='available')

    def __str__(self):
        return self.name
    
    
class Inventory(models.model):
    item_name = models.CharField(max_length=50)
    quantiy = models.PositiveIntegerField(max_length=50)
    alert_level = models.PositiveIntegerField(max_length=50)
    
    # def __str__(self):
    #     return self.quantity <= self.alert_level
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_low_stock():
            print(f"ALERT: {self.item_name} is critically low!")
    
    
    
class Order(models.model):
    custormer_name = models.CharField(max_length=100)
    table = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('pending', 'Pending'),
        ('preparing','Preparing'),
        ('served', 'Served'),
        ('completed','Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices,default='preparing')

    def __str__(self):
        return self.Order
    
class Reservertion(models.Model):
    customer_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    table = models.ForeignKey( table = models.ForeignKey("app.Model", verbose_name=(""), on_delete=models.CASCADE))
    reservation_time = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('active','Active'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]
    status = models.CharField(max_length=50, choices = status_choices, default='active')
    
    
    def __str__(self):
        return self.name
    