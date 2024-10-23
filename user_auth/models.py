from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    )
    tel = models.CharField(max_length=11, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    doctor_license = models.CharField(max_length=50, blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)

    username = models.CharField(max_length=150, unique=True, default='anonymous')

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.tel
        super().save(*args, **kwargs)

    REQUIRED_FIELDS = ['tel', 'role']

    def __str__(self):
        return self.username
