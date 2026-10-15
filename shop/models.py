from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    items_json = models.JSONField(default=list)
    total_paise = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_rupees(self):
        return self.total_paise / 100

    def __str__(self):
        return f"Order #{self.pk} — {self.customer_name}"
