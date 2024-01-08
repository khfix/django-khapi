from django.apps import apps
from django.db import models as django_models
from django.db.models.fields.files import FileField, ImageFieldFile

from .cache_models import *
from .check_data_type import check_data_type
from .hash import dict_hash_tables_update


def store_data(app_names):
    """
    Store data from specified app models into dictionaries.

    Args:
        app_names (list): List of app names.

    Raises:
        Exception: If an error occurs during the data storage process.

    """
    try:
        dictionary_names = [name[:-5] for name in globals() if name.endswith("_dict")]
        for app_name in app_names:
            models = apps.get_app_config(app_name).get_models()
            for model in models:
                for dictionary_name in dictionary_names:
                    if model.__name__ == dictionary_name:
                        dict_name = dictionary_name + "_dict"
                        model_dict = globals()[dict_name]
                        objects = model.objects.all()
                        for obj in objects:
                            obj_id = str(obj.id)
                            model_dict[obj_id] = {}

                            for field in model._meta.fields:
                                field_name = field.name
                                related_obj = getattr(obj, field_name)

                                if related_obj is not None:
                                    if field.is_relation:
                                        model_dict[obj_id][
                                            field_name
                                        ] = f"{field.related_model.__name__}:{related_obj.id}"
                                    else:
                                        if isinstance(
                                            related_obj, (FileField, ImageFieldFile)
                                        ):
                                            model_dict[obj_id][
                                                field_name
                                            ] = related_obj.url
                                        else:
                                            model_dict[obj_id][field_name] = related_obj

                            for field in model._meta.many_to_many:
                                field_name = field.name
                                model_dict[obj_id][field_name] = []
                                related_objs = getattr(obj, field_name).all()
                                for related_obj in related_objs:
                                    if related_obj is not None:
                                        model_dict[obj_id][field_name].append(
                                            f"{field.related_model.__name__}:{related_obj.id}"
                                        )
    except Exception as e:
        print(e)


def update_cache(model):
    """
    Update the cache for the given model.

    Args:
        model: The model to update the cache for.

    Raises:
        Exception: If an error occurs during the cache update.

    """
    try:
        dict_name = model.__name__ + "_dict"
        if dict_name in globals():
            model_dict = globals()[dict_name]
        else:
            print("Model not found")
        objects = model.objects.all()
        for obj in objects:
            obj_id = str(obj.id)
            model_dict[obj_id] = {}
            for field in model._meta.fields:
                field_name = field.name
                related_obj = getattr(obj, field_name)
                if related_obj is not None:
                    if field.is_relation:
                        model_dict[obj_id][
                            field_name
                        ] = f"{field.related_model.__name__}:{related_obj.id}"
                    else:
                        if isinstance(related_obj, (FileField, ImageFieldFile)):
                            model_dict[obj_id][field_name] = related_obj.url
                        else:
                            model_dict[obj_id][field_name] = related_obj
            for field in model._meta.many_to_many:
                field_name = field.name
                model_dict[obj_id][field_name] = []
                related_objs = getattr(obj, field_name).all()
                for related_obj in related_objs:
                    if related_obj is not None:
                        model_dict[obj_id][field_name].append(
                            f"{field.related_model.__name__}:{related_obj.id}"
                        )
        dict_hash_tables_update(model.__name__)

    except Exception as e:
        print(e)


def store_model_fields_type(app_names):
    """
    Store the fields and their types for each model in the given app names.

    Args:
        app_names (list): A list of app names.

    Returns:
        None
    """
    try:
        for app_name in app_names:
            models = apps.get_app_config(app_name).get_models()
            for model in models:
                if model.__bases__[0].__name__ == "KhUser":
                    model_name = model.__name__
                    model_dict = {}
                    dict_name = model_name + "_check_dict"
                    model_dict = globals()[dict_name]
                    for field in model._meta.fields:
                        if field.is_relation:
                            field_name = field.name
                            model_dict[field_name] = "int"
                        else:
                            field_name = field.name
                            type = check_data_type(field.get_internal_type())
                            model_dict[field_name] = type
                    for field in model._meta.many_to_many:
                        field_name = field.name
                        model_dict[field_name] = "list"

                if django_models.Model in model.__bases__:
                    model_name = model.__name__
                    model_dict = {}
                    dict_name = model_name + "_check_dict"
                    model_dict = globals()[dict_name]
                    for field in model._meta.fields:
                        if field.is_relation:
                            field_name = field.name
                            model_dict[field_name] = "int"
                        else:
                            field_name = field.name
                            type = check_data_type(field.get_internal_type())
                            model_dict[field_name] = type
                    for field in model._meta.many_to_many:
                        field_name = field.name
                        model_dict[field_name] = "list"

    except Exception as e:
        print(e)
