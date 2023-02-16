from django.db import models
from django.utils import timezone

from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    price = models.IntegerField(null=False)
    amount = models.PositiveIntegerField(null=False)
    image_path = models.ImageField()
    created_at = models.DateTimeField(default=timezone.now)
    reviews = models.ManyToManyField(User, through='Review')
    
    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vote = models.PositiveSmallIntegerField()
    comment = models.TextField()
