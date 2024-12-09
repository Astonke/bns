
# Create your models here.
from django.db import models
from django.contrib import admin

"""
class User(models.Model):
    mobile_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Hash passwords securely (see previous responses)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.mobile_no} - {self.name}"
"""
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=50, unique=True)
    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals'
    )
    referral_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

from django.db import models


#withdraw log
from django.utils import timezone

class Withdrawal(models.Model):
    mobile = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # pending, success, or failed
    timestamp = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.mobile} - {self.amount} - {self.status}'

admin.site.register(Withdrawal)
