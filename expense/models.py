# my_app/models_expenses.py
from django.db import models
from authentication.models import User  # Import the User model from the same app

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Groceries', 'Groceries'),
        ('Leisure', 'Leisure'),
        ('Utilities', 'Utilities'),
        ('Transport', 'Transport'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")  # Foreign key to User
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - ${self.amount} by {self.user.email}"
