from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import user_logged_in,user_logged_out,authenticate
from .models import User
from .serializer import UserSerializer

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def display_users(request):
       if user_logged_in:
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
       elif user_logged_out:
           return Response({"User logged out"})
       
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            return Response({
                'access_token':access_token,
                'refresh': str(token)
            })   
    except:
        return Response({"Error: user doesn't exist"})        
