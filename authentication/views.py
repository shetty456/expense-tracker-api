
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from authentication.serializer import UserSerializer, LoginSerializer
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
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                return Response({"access_token": access_token, "refresh": str(token)})
            else:
                return Response({"Error:invalid username or password"})
        except:
            return Response({"Error: user doesn't exists"})
