import json
import os

from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from khapi.auth_system.models import ApiGroup, Token
from khapi.cache_system.core import (
    create_data_validate,
    get_all,
    get_by_field_value,
    get_by_id,
)
from khapi.cache_system.store_update import update_cache
from khapi.methods import exclode_fields_data

from .cache_system.cache_models import *
from .cache_system.dict_manager import DictManager


class APICore(View, Group):
    model = None
    exclude_fields = []
    security_check = True
    """register_exclude_fields = [
        "id",
        "created_at",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "user_permissions",
        "groups",
        "apiuser_ptr",
    ]"""
    auto_token_create = True
    register_group = None

    @classmethod
    def as_api(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs

        return csrf_exempt(view)

    def get_all(self, request, *args, **kwargs):
        if self.exclude_fields:
            get_data = get_all(self.model.__name__)
            if get_data:
                excloded_data = exclode_fields_data(get_data, self.exclude_fields)
            else:
                return HttpResponseForbidden("Data not found")
            return JsonResponse(excloded_data, safe=False)
        else:
            data = get_all(self.model.__name__)
            return JsonResponse(data, safe=False)

    def get_by_field_value(self, request, *args, **kwargs):
        if self.exclude_fields:
            data = get_by_field_value(self.model.__name__, kwargs["value"])
            if data:
                excloded_data = exclode_fields_data(data, self.exclude_fields)
            else:
                return HttpResponseForbidden("Value not found")
            return JsonResponse(excloded_data, safe=False)
        else:
            data = get_by_field_value(self.model.__name__, kwargs["value"])
            return JsonResponse(data, safe=False)

    def get_by_id(self, request, *args, **kwargs):
        if self.exclude_fields:
            data = get_by_id(self.model.__name__, kwargs["pk"])
            if data:
                excloded_data = exclode_fields_data(data, self.exclude_fields)
            else:
                return HttpResponseForbidden("ID not found")
            return JsonResponse(excloded_data, safe=False)

        else:
            data = get_by_id(self.model.__name__, kwargs["id"])
            return JsonResponse(data, safe=False)

    def search_by_value(self, request, *args, **kwargs):
        body_data = request.body.decode("utf-8")
        body_data = json.loads(body_data)
        if body_data["value"]:
            if self.exclude_fields:
                data = get_by_field_value(self.model.__name__, body_data["value"])
                if data:
                    excloded_data = exclode_fields_data(data, self.exclude_fields)
                    return JsonResponse(excloded_data, safe=False)
                else:
                    return HttpResponseForbidden("Value not found")
            else:
                data = get_by_field_value(self.model.__name__, body_data["value"])
                return JsonResponse(data, safe=False)
        else:
            return HttpResponseForbidden("Send value to search ")

    def create(self, request, *args, **kwargs):
        content_type = request.META.get("CONTENT_TYPE")
        if content_type and "multipart/form-data" in content_type:
            data = request.POST.dict()
            data.update(request.FILES.dict())
            check = create_data_validate(data, self.model.__name__, self.exclude_fields)
            if check:
                list_data = []
                model = self.model
                keys = []
                for key, value in data.items():
                    if type(value) == list:
                        list_data = value
                        keys.append(key)
                if list_data:
                    for key in keys:
                        data.pop(key)
                    obj = model.objects.create(**data)
                    for item in list_data:
                        for key in keys:
                            getattr(obj, key).add(item)
                    fields_and_values = {
                        field.name: getattr(obj, field.name)
                        for field in obj._meta.fields
                    }
                    my_model_manager = DictManager(self.model.__name__)
                    my_model_manager.create(obj.id, fields_and_values)
                    data = get_by_id(self.model.__name__, obj.id)
                    return JsonResponse({"status": "success", "data": data})
                else:
                    obj = model.objects.create(**data)
                    fields_and_values = {
                        field.name: getattr(obj, field.name)
                        for field in obj._meta.fields
                    }
                    my_model_manager = DictManager(self.model.__name__)
                    my_model_manager.create(obj.id, fields_and_values)
                    data = get_by_id(self.model.__name__, obj.id)
                    return JsonResponse({"status": "success", "data": data})
            else:
                return HttpResponseForbidden("Data is not valid")
        elif content_type and "application/json" in content_type:
            body_data = request.body.decode("utf-8")
            if body_data:
                data = json.loads(body_data)
                check = create_data_validate(
                    data, self.model.__name__, self.exclude_fields
                )
                if check:
                    list_data = []
                    model = self.model
                    keys = []
                    for key, value in data.items():
                        if type(value) == list:
                            list_data = value
                            keys.append(key)
                    if list_data:
                        for key in keys:
                            data.pop(key)
                        obj = model.objects.create(**data)
                        for item in list_data:
                            for key in keys:
                                getattr(obj, key).add(item)
                        fields_and_values = {
                            field.name: getattr(obj, field.name)
                            for field in obj._meta.fields
                        }
                        my_model_manager = DictManager(self.model.__name__)
                        my_model_manager.create(obj.id, fields_and_values)
                        data = get_by_id(self.model.__name__, obj.id)
                        return JsonResponse({"status": "success", "data": data})
                    else:
                        obj = model.objects.create(**data)
                        fields_and_values = {
                            field.name: getattr(obj, field.name)
                            for field in obj._meta.fields
                        }
                        my_model_manager = DictManager(self.model.__name__)
                        my_model_manager.create(obj.id, fields_and_values)
                        data = get_by_id(self.model.__name__, obj.id)
                        return JsonResponse({"status": "success", "data": data})
                else:
                    return HttpResponseForbidden("Data is not valid")
            else:
                return HttpResponseForbidden("Send data to create ")

        else:
            return HttpResponseForbidden("Send data as json or form-data")

    def update(self, request, *args, **kwargs):
        body_data = request.body.decode("utf-8")
        if body_data:
            data = json.loads(body_data)
            check = create_data_validate(data, self.model.__name__, self.exclude_fields)
            if not check:
                return HttpResponseForbidden("Data is not valid")
            model = self.model
            list_data = []
            keys = []
            for key, value in data.items():
                if type(value) == list:
                    list_data = value
                    keys.append(key)
            if list_data:
                for key in keys:
                    data.pop(key)
                try:
                    obj = model.objects.get(id=kwargs["pk"])
                except:
                    return HttpResponseForbidden("ID not found")
                for key, value in data.items():
                    setattr(obj, key, value)
                obj.save()
                for key in keys:
                    getattr(obj, key).set(list_data)
                my_model_manager = DictManager(self.model.__name__)
                fields_and_values = {
                    field.name: getattr(obj, field.name) for field in obj._meta.fields
                }
                my_model_manager.update(kwargs["pk"], fields_and_values)
                new_data = get_by_id(self.model.__name__, kwargs["pk"])
                return JsonResponse({"status": "success", "data": new_data})
            else:
                try:
                    obj = model.objects.get(id=kwargs["pk"])
                except:
                    return HttpResponseForbidden("ID not found")
                for key, value in data.items():
                    setattr(obj, key, value)
                obj.save()
                my_model_manager = DictManager(self.model.__name__)
                fields_and_values = {
                    field.name: getattr(obj, field.name) for field in obj._meta.fields
                }
                my_model_manager.update(kwargs["pk"], fields_and_values)
                new_data = get_by_id(self.model.__name__, kwargs["pk"])
                return JsonResponse({"status": "success", "data": new_data})
        else:
            return HttpResponseForbidden("Send data to update ")

    def delete_data(self, request, *args, **kwargs):
        model = self.model
        try:
            obj = model.objects.get(id=kwargs["pk"])
            obj.delete()
            my_model_manager = DictManager(self.model.__name__)
            my_model_manager.delete(kwargs["pk"])
            return JsonResponse({"status": "success"})
        except:
            return HttpResponseForbidden("ID not found")

    def image_search(self, request, *args, **kwargs):
        if "image" in request.FILES:
            model = self.model.__name__
            uploaded_image = request.FILES["image"]
            folder_name = "cache"
            image_name = uploaded_image.name
            file_path = f"{folder_name}/{image_name}"
            fs = FileSystemStorage()
            fs.save(file_path, uploaded_image)
            temp_path = os.path.join("media/cache", image_name)
            model_images_path = os.path.join("media", model)
            try:
                from khapitools.core import find_best_similar_photo

                result_image_path = find_best_similar_photo(
                    temp_path, model_images_path
                )
            except:
                return HttpResponseForbidden("install khapitools package")
            fs.delete(temp_path)
            if result_image_path:
                image_name = os.path.basename(result_image_path)
                search_path = f"/media/{model}/{image_name}"
                search_data = get_by_field_value(model, search_path)
                data = search_data[0]
                return JsonResponse({"status": "success", "data": data})
            else:
                return HttpResponseForbidden("Image not found")

    def user_register(self, request, *args, **kwargs):
        content_type = request.META.get("CONTENT_TYPE")
        if content_type and "multipart/form-data" in content_type:
            data = request.POST.dict()
            data.update(request.FILES.dict())
        elif content_type and "application/json" in content_type:
            body_data = request.body.decode("utf-8")
            data = json.loads(body_data)
        else:
            return HttpResponseForbidden("Send data as json or form-data")
        if "email" and "password" in data:
            email_check = get_by_field_value(self.model.__name__, data["email"])
            if email_check:
                return HttpResponseForbidden("Email already exists")
            for field in self.model._meta.fields:
                if (
                    not field.blank
                    and not field.null
                    and not field.default
                    and not field.auto_created
                    and not field.primary_key
                    and field.editable
                ):
                    # if field.name not in self.register_exclude_fields:
                    if field.name in data:
                        pass
                    else:
                        return HttpResponseForbidden(f"Send {field.name} to register")
            self.model.objects.create_user(**data)
            if self.auto_token_create:
                transaction.on_commit(
                    lambda: Token.objects.create(
                        user=self.model.objects.get(email=data["email"])
                    )
                )
            if self.register_group:
                group = ApiGroup.objects.get(name=self.register_group)
                user = self.model.objects.get(email=data["email"])
                transaction.on_commit(lambda: group.user.add(user))

            transaction.on_commit(lambda: update_cache(self.model))
            return JsonResponse({"status": "success"})
        else:
            return HttpResponseForbidden("Send email and password to register")

    def user_login(self, request, *args, **kwargs):
        content_type = request.META.get("CONTENT_TYPE")
        if content_type and "multipart/form-data" in content_type:
            data = request.POST.dict()
        elif content_type and "application/json" in content_type:
            body_data = request.body.decode("utf-8")
            data = json.loads(body_data)
        else:
            return HttpResponseForbidden("Send data as json or form-data")
        if "email" and "password" in data:
            email = data["email"]
            password = data["password"]
            user = self.model.objects.get(email=email)
            if user.check_password(password):
                token = Token.objects.get(user=user)
                return JsonResponse({"status": "success", "token": token.token})
            else:
                return HttpResponseForbidden("Password or email is wrong")
        else:
            return HttpResponseForbidden("Send email and password to login")
