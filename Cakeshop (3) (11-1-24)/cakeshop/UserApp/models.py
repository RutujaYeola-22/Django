from django.db import models
from AdminApp.models import Cake
from datetime import datetime
# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20,primary_key = True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "UserInfo"


class Status(models.Model):
    status_name = models.CharField(max_length=20)

    class Meta:
        db_table = "Status"

class MyCart(models.Model):
    user = models.ForeignKey(UserInfo,on_delete = models.CASCADE)
    cake = models.ForeignKey(Cake,on_delete = models.CASCADE)
    qty = models.IntegerField()    
    status  = models.ForeignKey(Status,on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "MyCart"

class Payment(models.Model):
    user = models.ForeignKey(UserInfo,on_delete = models.CASCADE)
    cardno = models.CharField(max_length=4)
    cvv = models.CharField(max_length=4)
    expiry = models.CharField(max_length=10)
    balance = models.FloatField(default=10000)

    class Meta:
        db_table = "Payment"

class OrderMaster(models.Model):
    user = models.ForeignKey(UserInfo,on_delete = models.CASCADE)
    date_of_order = models.DateField(default =datetime.now() )
    amount = models.FloatField(default=1000)

    class Meta:
        db_table = "OrderMaster"