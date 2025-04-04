# expense/urls.py
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from expense.views import ExpenseViewSet,SortViews

# Initialize the router
router = DefaultRouter()

# Register the ExpenseViewSet to handle the API requests for /api/expenses
router.register(r'', ExpenseViewSet, basename="expense")

# Include the router URLs
urlpatterns = [
    path("", include(router.urls)), 
    path("sort",SortViews.as_view(),name="sorting")
    
]
