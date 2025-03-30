from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from expense.models import Expense
from expense.serializers import ExpenseSerializer
from datetime import timedelta, date

# Create your views here.

class ExpenseViewSet(viewsets.ModelViewSet):
    """Manages Expense CRUD operations."""
    
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    
    def list(self, request, *args, **kwargs):
        """List expenses with optional filters."""
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
        """Create a new expense."""
        data = request.data
        serializer = ExpenseSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Get a specific expense."""
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Handle partial updates."""
        expense = self.get_object()
        serializer = self.get_serializer(
            expense, data=request.data, partial=request.method == 'PATCH'
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete an expense."""
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return Response({"message": "Expense deleted"}, status=status.HTTP_204_NO_CONTENT)
