from django.shortcuts import render
from khapi import api_core
from khapi.auth_system.permissions import ApiPermission

from .models import ApiUser


class RegisterAPI(api_core.APICore):
    """
    API endpoint for user registration.
    """

    def __init_subclass__(cls):
        if not issubclass(cls.model, ApiUser):
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def post(self, request, *args, **kwargs):
        return getattr(self, "user_register")(request, *args, **kwargs)


class LoginAPI(api_core.APICore):
    """
    API view for user login.
    """

    def __init_subclass__(cls):
        if not issubclass(cls.model, ApiUser):
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def post(self, request, *args, **kwargs):
        return getattr(self, "user_login")(request, *args, **kwargs)
