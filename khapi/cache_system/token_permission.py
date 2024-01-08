from khapi.auth_system.models import ApiRole, Token
from khapi.cache_system.cache_models import *


def store_token_by_permission():
    try:
        model_dict = globals()["Token_permission_dict"]
        api_key_dict = globals()["Api_key_permission_dict"]
        token_objects = Token.objects.all()
        api_role_objects = ApiRole.objects.filter(is_active=True)
        for api_role_object in api_role_objects:
            key = f"{api_role_object.model}:{api_role_object.api_class.name}"
            model_dict.setdefault(key, [])
            if api_role_object.is_authenticated == True:
                for token_object in token_objects:
                    if token_object.user.is_authenticated:
                        model_dict[key].append(token_object.token)
                if api_role_object.is_public == False:
                    if api_role_object.api_key:
                        api_key_dict.setdefault(key, [])
                        api_key_dict[key].append(api_role_object.api_key)
            else:
                for api_group in api_role_object.api_groups.all():
                    for token_object in token_objects:
                        if token_object.user in api_group.user.all():
                            model_dict[key].append(token_object.token)
                if api_role_object.is_public == False:
                    if api_role_object.api_key:
                        api_key_dict.setdefault(key, [])
                        api_key_dict[key].append(api_role_object.api_key)
    except Exception as e:
        print(e)


def update_token_by_permission(key):
    try:
        model_dict = globals()["Token_permission_dict"]
        api_key_dict = globals()["Api_key_permission_dict"]
        token_objects = Token.objects.all()
        api_role_objects = ApiRole.objects.filter(is_active=True)
        for api_role_object in api_role_objects:
            api_key = f"{api_role_object.model}:{api_role_object.api_class.name}"
            if api_key == key:
                model_dict[key] = []
                if api_role_object.is_authenticated == True:
                    for token_object in token_objects:
                        if token_object.user.is_authenticated:
                            model_dict[key].append(token_object.token)
                    if api_role_object.is_public == False:
                        if api_role_object.api_key:
                            api_key_dict[key] = []
                            api_key_dict[key].append(api_role_object.api_key)
                    else:
                        if api_role_object.api_key:
                            api_key_dict[key] = []
                        elif key in api_key_dict:
                            del api_key_dict[key]
                else:
                    for api_group in api_role_object.api_groups.all():
                        for token_object in token_objects:
                            if token_object.user in api_group.user.all():
                                model_dict[key].append(token_object.token)
                    if api_role_object.is_public == False:
                        if api_role_object.api_key:
                            api_key_dict[key] = []
                            api_key_dict[key].append(api_role_object.api_key)
                    else:
                        if api_role_object.api_key:
                            api_key_dict[key] = []
                        elif key in api_key_dict:
                            del api_key_dict[key]
    except Exception as e:
        print(e)
