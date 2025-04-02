from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta, date
from expense.models import Expense
from expense.serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    """Expense API for authenticated users to manage expenses."""

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """Return expenses belonging to the authenticated user."""
        return Expense.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """List expenses with optional filters (past week, month, etc.)."""
        queryset = self.get_queryset()
        filter_type = request.query_params.get("filter", None)
        today = date.today()

        if filter_type == "past_week":
            queryset = queryset.filter(date__gte=today - timedelta(days=7))
        elif filter_type == "past_month":
            queryset = queryset.filter(date__gte=today - timedelta(days=30))
        elif filter_type == "last_3_months":
            queryset = queryset.filter(date__gte=today - timedelta(days=90))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a new expense linked to the authenticated user."""
        data = request.data.copy()
        data["user"] = request.user.id  

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve a specific expense owned by the authenticated user."""
        expense = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(expense)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update an expense owned by the authenticated user."""
        expense = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer = self.get_serializer(expense, data=request.data, partial=request.method == "PATCH")

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete an expense owned by the authenticated user."""
        expense = get_object_or_404(self.get_queryset(), pk=pk)
        expense.delete()
        return Response({"message": "Expense deleted"}, status=status.HTTP_204_NO_CONTENT)
