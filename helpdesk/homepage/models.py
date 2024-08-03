from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True) 
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    policy_name = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=50)
    policy_start_date = models.DateField()
    duration = models.IntegerField()
    premium_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username