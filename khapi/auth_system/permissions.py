from django.http import HttpResponseForbidden
from khapi import api_core

from .auth_core import ApiPermissionCore


class ApiPermission(api_core.APICore):
    def check_permissions(
        self, model_name, class_name, def_name, request, *args, **kwargs
    ):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        api_name = f"{model_name.__name__}:{class_name}"
        token = request.headers.get("Authorization")
        api_key = request.headers.get("API-KEY")
        check = ApiPermissionCore(check=api_name, token=token, api_key=api_key)
        if check.status == True:
            return getattr(self, def_name)(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(check.erorr_message)
