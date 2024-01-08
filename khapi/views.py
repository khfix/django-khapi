from khapi import api_core
from khapi.auth_system.permissions import ApiPermission


class ListAPI(api_core.APICore):
    def __init_subclass__(cls):
        if cls.model is None:
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def get(self, request, *args, **kwargs):
        if self.security_check:
            return ApiPermission.check_permissions(
                self, self.model, "ListAPI", "get_all", request, *args, **kwargs
            )
        else:
            return getattr(self, "get_all")(request, *args, **kwargs)


class ListByValueAPI(api_core.APICore):
    def __init_subclass__(cls):
        if cls.model is None:
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def get(self, request, *args, **kwargs):
        return ApiPermission.check_permissions(
            self,
            self.model,
            "ListByValueAPI",
            "get_by_field_value",
            request,
            *args,
            **kwargs,
        )


class GetByIdAPI(api_core.APICore):
    def __init_subclass__(cls):
        if cls.model is None:
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def get(self, request, *args, **kwargs):
        return ApiPermission.check_permissions(
            self, self.model, "GetByIdAPI", "get_by_id", request, *args, **kwargs
        )


class SearchAPI(api_core.APICore):
    def __init_subclass__(cls):
        if cls.model is None:
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def post(self, request, *args, **kwargs):
        return ApiPermission.check_permissions(
            self, self.model, "SearchAPI", "search_by_value", request, *args, **kwargs
        )


class CreateAPI(api_core.APICore):
    def __init_subclass__(cls):
        if cls.model is None:
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def post(self, request, *args, **kwargs):
        return ApiPermission.check_permissions(
            self, self.model, "CreateAPI", "create", request, *args, **kwargs
        )


class UpdateAPI(api_core.APICore):
    def __init_subclass__(cls):
        if cls.model is None:
            raise ValueError(f"{cls.__name__} must define model class attribute")

    def put(self, request, *args, **kwargs):
        return ApiPermission.check_permissions(
            self, self.model, "UpdateAPI", "update", request, *args, **kwargs
        )

    def patch(self, request, *args, **kwargs):
        return ApiPermission.check_permissions(
            self, self.model, "UpdateAPI", "update", request, *args, **kwargs
        )

    def delete(self, request, *args, **kwargs):
        return ApiPermission.check_permissions(
            self, self.model, "UpdateAPI", "delete_data", request, *args, **kwargs
        )
