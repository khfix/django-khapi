import secrets

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.db import models
from django.db import models as django_models


class Token(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="token",
        verbose_name="User",
    )
    token = models.CharField(max_length=80, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        abstract = "khapi.auth_system" not in settings.INSTALLED_APPS
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.genrate_token()
        return super().save(*args, **kwargs)

    def genrate_token(self):
        token = secrets.token_urlsafe(80)
        while self.__class__.objects.filter(token=token).exists():
            token = secrets.token_urlsafe(60)
        return token


class ApiGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "API Group"
        verbose_name_plural = "API Groups"
        abstract = "khapi.auth_system" not in settings.INSTALLED_APPS
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


def get_model_choices():
    app_names = settings.KHAPI["CACHE_APPS"]
    model_choices = []
    for app_name in app_names:
        models = apps.get_app_config(app_name).get_models()
        for model in models:
            if model.__bases__[0].__name__ == "ApiUser":
                model_choices.append((model.__name__, model.__name__))
            if django_models.Model in model.__bases__:
                if (
                    model.__name__ != "ApiRole"
                    and model.__name__ != "ApiGroup"
                    and model.__name__ != "Token"
                    and model.__name__ != "ApiClass"
                ):
                    model_choices.append((model.__name__, model.__name__))
    return model_choices


class ApiRole(models.Model):
    name = models.CharField(max_length=255, unique=True)
    model = models.CharField(max_length=255, choices=get_model_choices)
    api_class = models.CharField(
        max_length=255,
        choices=[
            ("ListAPI", "ListAPI"),
            ("ListByValueAPI", "ListByValueAPI"),
            ("GetByIdAPI", "GetByIdAPI"),
            ("SearchAPI", "SearchAPI"),
            ("CreateAPI", "CreateAPI"),
            ("UpdateAPI", "UpdateAPI"),
            ("DeleteAPI", "DeleteAPI"),
            ("ImageSearchAPI", "ImageSearchAPI"),
        ],
    )
    auth_type = models.CharField(
        max_length=25,
        choices=[
            ("AUTHENTICATED", "AUTHENTICATED"),
            ("API-GROUP", "API-GROUP"),
            ("PUBLIC", "PUBLIC"),
        ],
        default="AUTHENTICATED",
    )
    api_groups = models.ManyToManyField(
        ApiGroup,
        verbose_name="API Groups",
        blank=True,
        help_text="API Groups that can access this API Role",
        related_name="api_user_set",
        related_query_name="api_user",
    )
    api_key_status = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    security_check = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "API Role"
        verbose_name_plural = "API Roles"
        abstract = "khapi.auth_system" not in settings.INSTALLED_APPS
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.name = f"{self.model}:{self.api_class if self.api_class else 'None'}"
        if not self.api_key and self.api_key_status:
            self.api_key = secrets.token_urlsafe(40)
        return super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class ApiUser(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(editable=False, null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True, editable=False)
    is_superuser = models.BooleanField(default=False, editable=False)
    user_permissions = models.ManyToManyField(Permission, blank=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        abstract = "khapi.auth_system" not in settings.INSTALLED_APPS
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
