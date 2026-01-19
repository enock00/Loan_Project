from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Correct field names
    list_display = ("email", "phone", "full_name", "id_no", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "phone", "full_name", "id_no", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "full_name", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email", "phone")
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)

