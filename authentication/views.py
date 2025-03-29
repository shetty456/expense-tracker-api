from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializer import UserSerializer
from rest_framework.generics import GenericAPIView

User = get_user_model()


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "User registered successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                return Response({"access_token": access_token, "refresh": str(token)})
        except:
            return Response({"Error: user doesn't exist"})
