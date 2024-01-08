from .cache_models import *


def get_all(model_name):
    """
    Retrieve all objects of a given model from the cache system.

    Args:
        model_name (str): The name of the model.

    Returns:
        list: A list of all objects of the given model in the cache system.

    Raises:
        None
    """
    try:
        dict_name = model_name + "_dict"
        if dict_name in globals():
            data = []
            dict = globals()[dict_name]
            for dict in dict.values():
                data.append(dict)
            return data
        else:
            print(f"{model_name} not found in cache system")
    except Exception as e:
        print(e)


def get_by_id(model_name, id):
    """
    Retrieve an object from the cache system by its ID.

    Args:
        model_name (str): The name of the model.
        id (int or str): The ID of the object.

    Returns:
        object: The object with the specified ID, if found in the cache system.

    Raises:
        None.

    """
    try:
        dict_name = model_name + "_dict"
        if dict_name in globals():
            dict = globals()[dict_name]
            id = str(id)
            if id in dict:
                return dict[id]
            else:
                print(f"{id} not found in model {model_name} in cache system")
        else:
            print(f"{model_name} not found in cache system")
    except Exception as e:
        print(e)


def get_by_field_value(model_name, *args):
    """
    Retrieve data from the cache system based on the field value(s) provided.

    Args:
        model_name (str): The name of the model.
        *args: Variable number of field values to search for.

    Returns:
        list: A list of data matching the provided field value(s).

    Raises:
        None.

    """
    try:
        dict_name = model_name + "_dict"
        hash_table_name = model_name + "_reverse_hash_table"
        if dict_name in globals():
            dict = globals()[dict_name]
        if hash_table_name in globals():
            hash_table = globals()[hash_table_name]
            data = []
            for arg in args:
                matching_ids = hash_table.get(arg)
                if matching_ids is not None:
                    for id in matching_ids:
                        data.append(dict[id])
                else:
                    print(f"{arg} not found in model {model_name} in cache system")
            return data
        else:
            print(f"{model_name} not found in cache system")
    except Exception as e:
        print(e)


def filter_by_fields(model_name, **kwargs):
    """
    Filters the data dictionary by the specified fields and their corresponding values.

    Args:
        model_name (str): The name of the model.
        **kwargs: Keyword arguments representing the fields and their values to filter by.

    Returns:
        dict or None: The first data item that matches all the specified fields and values,
        or None if no match is found.

    Raises:
        Exception: If an error occurs during the filtering process.
    """
    try:
        dict_name = model_name + "_dict"
        if dict_name in globals():
            data_dict = globals()[dict_name]
            result = None
            for data in data_dict.values():
                all_match = True
                for key, value in kwargs.items():
                    if data.get(key) != value:
                        all_match = False
                        break
                if all_match:
                    result = data
                    break
            return result
        else:
            print(f"{model_name} not found in cache system")
            return None
    except Exception as e:
        print(e)


def data_validate(post_dict, model, exclude_fields=[]):
    """
    Validates the data in the `post_dict` against the specified `model`.

    Args:
        post_dict (dict): The dictionary containing the data to be validated.
        model (str): The name of the model to validate against.
        exclude_fields (list, optional): List of fields to exclude from validation. Defaults to [].

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    dict_name = model + "_dict"
    dict = globals()[dict_name]
    model_dict = {}
    model_dict.update(dict)
    model_dict = model_dict[list(model_dict.keys())[0]]
    for exclude_field in exclude_fields:
        if exclude_field in model_dict.keys():
            model_dict.pop(exclude_field)

    if set(post_dict.keys()) != set(model_dict.keys()):
        return False

    for key in post_dict.keys():
        if type(post_dict[key]) != type(model_dict[key]):
            return False

    return True


def create_data_validate(post_dict, model, exclude_fields=[]):
    """
    Validates the data in the post_dict against the model dictionary.

    Args:
        post_dict (dict): The dictionary containing the data to be validated.
        model (str): The name of the model.
        exclude_fields (list, optional): List of fields to be excluded from validation. Defaults to [].

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    dict_name = model + "_check_dict"
    dict = globals()[dict_name]
    model_dict = {}
    model_dict.update(dict)
    for exclude_field in exclude_fields:
        if exclude_field in model_dict.keys():
            model_dict.pop(exclude_field)

    if set(post_dict.keys()) != set(model_dict.keys()):
        return False
    else:
        for key in post_dict.keys():
            if f"{type(post_dict[key])}" != f"<class '{model_dict[key]}'>":
                return False
        return True
