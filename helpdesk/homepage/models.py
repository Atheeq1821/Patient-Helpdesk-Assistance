from django.contrib.auth.models import User
from django.db import models
import random
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    unique_id = models.CharField(max_length=6, unique=True, editable=False)
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
    claimable_amt=models.DecimalField(max_digits=15, decimal_places=2)
    claims = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        if not self.claimable_amt:
            self.claimable_amt = self.total_amount
        super(Profile, self).save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            unique_id = f"{random.randint(100000, 999999)}"
            if not Profile.objects.filter(unique_id=unique_id).exists():
                return unique_id

    def __str__(self):
        return self.user.username

class Claim(models.Model):
    claim_id = models.AutoField(primary_key=True)
    applied_date = models.DateField(null=True, blank=True)
    claim_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    hospital_name = models.TextField()
    amount_claimed = models.DecimalField(max_digits=10, decimal_places=2)
    treatment_info = models.TextField()

    def save(self, *args, **kwargs):
        profile = self.user.profile
        if self.pk is None:  # Only subtract if this is a new claim
            profile.claimable_amt -= self.amount_claimed
            profile.claims += 1
            profile.save()
        super(Claim, self).save(*args, **kwargs)

    def __str__(self):
        return f"Claim {self.claim_id} by {self.user.username}"