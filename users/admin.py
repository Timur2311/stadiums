from django.contrib import admin
from users.models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        "phone",
        "email",
        "role",
    ]