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
    item_price = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=3) 
    carbon_credits = models.IntegerField()

class Transactions(models.Model):
    item = models.ForeignKey(Items, related_name="db_user",on_delete=models.CASCADE)
    qty = models.IntegerField()
    total_price = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=3)
    rounded_price = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=3)
    green_amount = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=3)
    green_points = models.IntegerField()
    user_profile = models.ForeignKey(UserProfile, related_name="user_profile",on_delete=models.CASCADE) 

class Project(models.Model):
    project_name = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    region = models.CharField(max_length=150)
    amount = models.IntegerField(default=500)


class Bid(models.Model):
    bid_user = models.ForeignKey(UserProfile, related_name="bid_user_profile",on_delete=models.CASCADE)
    bid_qty = models.IntegerField(default=500)
    price = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=2)
    amount = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=2) 
    bidder = models.CharField(max_length=200)
    #accepted =  models.ForeignKey(UserProfile, related_name="accepted_user_profile",on_delete=models.CASCADE,blank=True,null=True)
    accepted_flag = models.CharField(max_length=200)
  
