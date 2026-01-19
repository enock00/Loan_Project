from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone, id_no, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        if not phone:
            raise ValueError("The phone must be set")
        if not id_no:
            raise ValueError("The ID number must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, id_no=id_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, id_no, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, phone, id_no, password, **extra_fields)