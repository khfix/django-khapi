import os

from django.apps import apps
from django.db import models as django_models
from khapi.auth_system.models import Token

from .cache_models import *


def generate_cache_files(app_names):
    all_model_dicts = {}

    for app_name in app_names:
        models = apps.get_app_config(app_name).get_models()

        for model in models:
            if model.__bases__[0].__name__ == "ApiUser":
                model_name = model.__name__
                model_dict = {}
                all_model_dicts[model_name] = model_dict
            if django_models.Model in model.__bases__:
                model_name = model.__name__
                model_dict = {}
                all_model_dicts[model_name] = model_dict

    code = "# chache dictionaries\n"
    for model_name, model_dict in all_model_dicts.items():
        code += f"{model_name}_dict = {{}}\n"

    for model_name, model_dict in all_model_dicts.items():
        code += f"{model_name}_reverse_hash_table = {{}}\n"

    for model_name, model_dict in all_model_dicts.items():
        code += f"{model_name}_check_dict = {{}}\n"

    code += f"Tokens_dict = {{}}\n"
    code += f"Api_keys_dict = {{}}\n"
    code += f"Api_Groups_dict = {{}}\n"
    code += f"Api_Roles_dict = {{}}\n"

    khapi_dir = os.path.join(apps.get_app_config("khapi").path)
    cache_files = os.path.join(khapi_dir, "cache_system/cache_models.py")

    with open(cache_files, "w") as f:
        f.write(code)
