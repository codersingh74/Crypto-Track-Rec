
from django.conf import settings

from django.db import models 
from django.contrib.auth.models import AbstractUser
import uuid

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    coin_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    amount = models.FloatField()

    def __str__(self): 
        return f"{self.user.username} - {self.coin_name} - {self.amount}" 
    



class Coin(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=20, decimal_places=10)
    market_cap = models.DecimalField(max_digits=30, decimal_places=10)
    price_change_percentage_24h = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.URLField()
    
    def __str__(self): 
        return self.name
    


   

