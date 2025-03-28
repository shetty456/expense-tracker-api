from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model,authenticate
from authentication.serializer import UserSerializer
from rest_framework.generics import GenericAPIView




User = get_user_model()

   


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer  # Explicitly define serializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)  # Use self.get_serializer()
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "User registered successfully!", "data": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(GenericAPIView):
    serializer_class = UserSerializer 
          

    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = authenticate(username=username,password =password)
            if user:
                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                return Response({
                    'access_token':access_token,
                    'refresh': str(token)
                })   
        except:
            return Response({"Error: user doesn't exist"})        
