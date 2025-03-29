from django.contrib import admin
from authentication.models import User

from .models import Expense
# Register your models here.
admin.site.register(Expense)

# Register your models here.
admin.site.register(User)

