from rest_framework import permissions
from django.urls import path, re_path
from .views import ExpenseViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view for API documentation using drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Expense API",
        default_version="v1",
        description="API documentation for Expense CRUD operations",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Allow public access to API documentation
)

urlpatterns = [
    # Expense CRUD Endpoints
    path("api/expenses/", ExpenseViewSet.as_view({"get": "list"}), name="expense-list"),  # Get all expenses
    path("api/expenses/create/", ExpenseViewSet.as_view({"post": "create"}), name="expense-create"),  # Create a new expense
    path("api/expenses/<int:pk>/", ExpenseViewSet.as_view({"get": "retrieve"}), name="expense-detail"),  # Retrieve a specific expense
    path("api/expenses/<int:pk>/update/", ExpenseViewSet.as_view({"put": "update"}), name="expense-update"),  # Update an expense
    path("api/expenses/<int:pk>/delete/", ExpenseViewSet.as_view({"delete": "destroy"}), name="expense-delete"),  # Delete an expense

    # API Documentation Endpoints (Swagger & Redoc)
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"),  # Swagger UI for API documentation
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-docs"),  # ReDoc UI for API documentation
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),  # Raw API schema in JSON/YAML format
]
