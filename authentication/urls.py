from django.urls import path
from .views import register,display_users,login

urlpatterns = [
            path('register/', register, name='register'),
            path('display/',display_users , name='register'),
            path('register/', login, name='register'),  # Ensure this matches your API request
]
