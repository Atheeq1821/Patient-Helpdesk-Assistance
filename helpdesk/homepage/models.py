from django.db import models

class Member(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    policy_name = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=255)
    policy_start_date = models.DateField()
    duration=models.IntegerField()
    premium_monthly = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
