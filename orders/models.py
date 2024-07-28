# orders/models.py
from django.db import models

class Order(models.Model):
    user_email = models.EmailField()
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} ({self.user_email})"
