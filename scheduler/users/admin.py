from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "is_staff")
    list_filter = ("is_staff",)
    search_fields = ("username", "name")
    ordering = ("username",)
    filter_horizontal = ()
    list_per_page = 20
    fieldsets = (
        (None, {"fields": ("username","name", "password")}),  
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
