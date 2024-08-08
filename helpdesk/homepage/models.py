from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    insurer = models.CharField(max_length=255)
    policy_name = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=50)
    policy_start_date = models.DateField()
    duration = models.IntegerField()
    premium_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.user.username

class Claim(models.Model):
    claim_id = models.AutoField(primary_key=True)
    claim_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    amount_claimed = models.DecimalField(max_digits=10, decimal_places=2)
    treatment_info = models.TextField()

    def __str__(self):
        return f"Claim {self.claim_id} by {self.user.username}"