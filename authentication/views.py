from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from datetime import timedelta, date
# Create your views here.



class ExpenseViewSet(viewsets.ViewSet):
    """Manages Expense CRUD operations."""

    def list(self, request):
        """List expenses with optional filters."""
        queryset = Expense.objects.all()
        filter_type = request.query_params.get("filter", None)
        today = date.today()

        if filter_type == "past_week":
            queryset = queryset.filter(date__gte=today - timedelta(days=7))
        elif filter_type == "past_month":
            queryset = queryset.filter(date__gte=today - timedelta(days=30))
        elif filter_type == "last_3_months":
            queryset = queryset.filter(date__gte=today - timedelta(days=90))

        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a new expense."""
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Get a specific expense."""
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Update an existing expense."""
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete an expense."""
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return Response({"message": "Expense deleted"}, status=status.HTTP_204_NO_CONTENT)