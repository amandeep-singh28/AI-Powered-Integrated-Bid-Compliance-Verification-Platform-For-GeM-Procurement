
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email address is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_profile_complete", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email,
            password,
            **extra_fields
        )


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TENDER_MANAGER = "TENDER_MANAGER", "Tender Manager"
        BIDDER = "BIDDER", "Bidder"
        REVIEWER = "REVIEWER", "Reviewer"

    class RoleRequestStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    username = None

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.BIDDER
    )

    requested_role = models.CharField(
        max_length=20,
        choices=Role.choices,
        blank=True,
        default=""
    )

    role_request_status = models.CharField(
        max_length=20,
        choices=RoleRequestStatus.choices,
        default=RoleRequestStatus.PENDING
    )

    is_profile_complete = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
