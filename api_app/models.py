from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
