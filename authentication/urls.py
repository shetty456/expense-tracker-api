# authentication/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet

# Initialize the router
router = DefaultRouter()

# Register the ExpenseViewSet to handle the API requests for /api/expenses
router.register(r'expenses', ExpenseViewSet, basename="expense")

# Include the router URLs
urlpatterns = router.urls
from django.urls import path
from authentication.views import RegisterView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/", LoginView.as_view(), name="login"
    ),  # Ensure this matches your API request
]
