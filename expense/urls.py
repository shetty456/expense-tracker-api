# expense/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from expense.views import ExpenseViewSet

# Initialize the router
router = DefaultRouter()

# Register the ExpenseViewSet to handle the API requests for /api/expenses
router.register(r'expenses', ExpenseViewSet, basename="expense")

# Include the router URLs
urlpatterns = router.urls
