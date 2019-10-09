from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name="db_user",on_delete=models.CASCADE)
    account_number = models.CharField(max_length=150)
    account_name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    cash_balance = models.IntegerField(default=500)
    credit_balance = models.IntegerField(default=500)


class FlightDetails(models.Model):
    flight_id = models.CharField(max_length=150)
    fuel_burn = models.CharField(max_length=150)
    flight_from = models.CharField(max_length=150)
    flight_to = models.CharField(max_length=150)
    price = models.CharField(max_length=150)
    start_date = models.DateField()
    return_date = models.DateField()

class Items(models.Model):
    item_id = models.CharField(max_length=150)
    item_name = models.CharField(max_length=150)
    item_image = models.ImageField(upload_to='static/image/item')
    item_price = models.IntegerField() 


class Teansactions(models.Model):
    item = models.ForeignKey(Items, related_name="db_user",on_delete=models.CASCADE)
    qty = models.IntegerField()
    total_price = models.IntegerField()
    rounded_price = models.IntegerField()  
    green_amount = models.IntegerField()
    green_points = models.IntegerField() 
    user_profile = models.ForeignKey(UserProfile, related_name="user_profile",on_delete=models.CASCADE)   
