import time

from django.conf import settings
from khapi.auth_system.auth_core import ApiPermissionCore
from khapi.cache_system.hash import dict_hash_tables
from khapi.cache_system.store_update import store_data, store_model_fields_type
from khapi.cache_system.token_permission import store_token_by_permission


def khapi_cache_start():
    """
    Starts the caching process for the KH API.

    This function retrieves the list of app names from the settings and performs the following tasks:
    1. Stores the data for the specified app names.
    2. Creates hash tables for efficient data retrieval.
    3. Stores the model fields and their types for the specified app names.
    4. Initializes the API permission core.

    If any exception occurs during the process, it will be printed.

    Note: This function assumes that the settings module contains the necessary configurations.

    """
    try:
        if settings.KHAPI:
            if settings.KHAPI["CACHE_APPS"]:
                app_names = settings.KHAPI["CACHE_APPS"]
            else:
                print("CACHE_APPS not found in settings")
        else:
            print("khapi app is not found in settings")

        store_data(app_names)
        dict_hash_tables()

        store_model_fields_type(app_names)

        # store_token_by_permission()
        ApiPermissionCore(store=True)

    except Exception as e:
        print(e)
