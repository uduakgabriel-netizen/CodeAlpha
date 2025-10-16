from django.db import models

# Create your models here.

class user(models.Model):
    fullname = models.CharField( max_length=100)
    email = models.EmailField( max_length=254)
    
    class admin(models.Model):
        fullname = models.CharField( max_length=100)
        
    