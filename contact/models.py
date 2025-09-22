from django.db import models


class ContactUs(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=30)
    phone=models.BigIntegerField(max_length=10,unique=True)
    subject=models.CharField(max_length=100)
    message=models.TextField()

# Create your models here.
