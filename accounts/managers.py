from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, full_name, id_no, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        if not phone:
            raise ValueError("Phone number is required")
        if not full_name:
            raise ValueError("Full name is required")
        if not id_no:
            raise ValueError("ID number is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone=phone,
            full_name=full_name,
            id_no=id_no,
            **extra_fields
        )

        # 🔒 THIS IS CRITICAL: hash the password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, full_name, id_no, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, phone, full_name, id_no, password, **extra_fields)
