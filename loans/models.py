from django.conf import settings
from django.db import models


class Loan(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    PURPOSE_CHOICES = [
        ("business", "Business"),
        ("education", "Education"),
        ("personal", "Personal"),
        ("medical", "Medical"),
        ("emergency", "Emergency"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=255, choices=PURPOSE_CHOICES)
    duration = models.IntegerField(default=3)  # months

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    fee_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name or self.user.email} - {self.amount}"



