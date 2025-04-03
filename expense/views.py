from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta, date,timezone
from expense.models import Expense
from expense.serializers import ExpenseSerializer
from django.utils.timezone import now
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema,OpenApiParameter


class ExpenseViewSet(viewsets.ModelViewSet):
    """Expense API for authenticated users to manage expenses."""

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """Return expenses belonging to the authenticated user."""
        return Expense.objects.filter(user=self.request.user)
    

   

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
    
class SortViews(GenericAPIView):
    """
    View to filter expenses by a predefined time range for the authenticated user.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """Return expenses belonging to the authenticated user."""
        return Expense.objects.filter(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="range",
                description=(
                    "Time range to filter expenses. "
                    "Accepted values: 'past_week', 'past_month', 'last_3_months'."
                ),
                required=True,
                type=str
            ),
        ],
        responses={200: ExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        """
        Filter and return the authenticated user's expenses based on a predefined time range.
        Expected query parameter: `range`.
        """
        time_range = request.query_params.get("range")

        if not time_range:
            return Response(
                {"error": "The 'range' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        today = date.today()
 
        date_ranges = {
            "past_week": today - timedelta(days=7),
            "past_month": today - timedelta(days=30),
            "last_3_months": today - timedelta(days=90),
        }

        if time_range not in date_ranges:
            return Response(
                {
                    "error": "Invalid 'range' value.",
                    "allowed_values": list(date_ranges.keys())
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        date_from = date_ranges[time_range]

       
        queryset = self.get_queryset().filter(date__range=[date_from, today])
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
