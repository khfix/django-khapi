from .cache_models import *


class ReverseHashTable:
    """
    A class representing a reverse hash table.

    The ReverseHashTable class allows for efficient storage and retrieval of values
    based on their associated keys. It supports inserting values into the table and
    retrieving values based on their keys.

    Attributes:
        table (dict): A dictionary representing the reverse hash table.

    Methods:
        insert(key, value): Inserts a value into the table based on the given key.
        get(key): Retrieves the value associated with the given key from the table.
    """

    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        if key in self.table:
            self.table[key].append(value)
        else:
            self.table[key] = [value]

    def get(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return None


def create_reverse_hash_table(dict_name):
    """
    Create a reverse hash table based on the given dictionary.

    Args:
        dict_name (str): The name of the dictionary to create the reverse hash table from.

    Returns:
        dict: The reverse hash table containing the keys and their corresponding values.
            If the dictionary does not exist, None is returned.
    """
    try:
        reverse_hash_table = ReverseHashTable()
        dict_name = dict_name + "_dict"
        if dict_name in globals():
            dict = globals()[dict_name]
        else:
            return None

        for key, value in dict.items():
            if value is not None:
                for value_key, value_value in value.items():
                    if value_value is not None:
                        if not isinstance(value_value, list):
                            reverse_hash_table.insert(value_value, key)
                        else:
                            if value_value:
                                for item in value_value:
                                    if item:
                                        reverse_hash_table.insert(item, key)

        return reverse_hash_table.table

    except Exception as e:
        print(e)


def dict_hash_tables():
    """
    Update the global hash tables dictionary with reverse hash tables.

    This function iterates over the global variables and checks for names ending with "_reverse_hash_table".
    For each matching variable, it creates a reverse hash table using the corresponding hash table name,
    and updates the global hash tables dictionary with the reverse hash table.

    Returns:
        None: If any error occurs during the process.

    Raises:
        Exception: If any error occurs during the process.
    """
    try:
        hash_tables_names = [
            name[:-19] for name in globals() if name.endswith("_reverse_hash_table")
        ]
        for hash_tables_name in hash_tables_names:
            check = hash_tables_name + "_reverse_hash_table"
            if check in globals():
                if hash_tables_name != "create":
                    reverse_hash_table = create_reverse_hash_table(hash_tables_name)
                    hash_tables_name = hash_tables_name + "_reverse_hash_table"
                    hash_tables_dict = globals()[hash_tables_name]
                    hash_tables_dict.update(reverse_hash_table)
            else:
                return None
    except Exception as e:
        print(e)


def dict_hash_tables_update(model_name):
    """
    Update the hash tables dictionary with the reverse hash table for the given model name.

    Args:
        model_name (str): The name of the model.

    Returns:
        None: If the dictionary name is not found in the global scope.

    Raises:
        Exception: If an error occurs during the update process.
    """
    try:
        dict_name = model_name + "_dict"
        if dict_name in globals():
            reverse_hash_table = create_reverse_hash_table(model_name)
            hash_tables_name = model_name + "_reverse_hash_table"
            if hash_tables_name in globals():
                hash_tables_dict = globals()[hash_tables_name]
                hash_tables_dict.update(reverse_hash_table)
        else:
            return None
    except Exception as e:
        print(e)


def hash_tabel_print(model_name):
    """
    Prints the hash table associated with the given model name.

    Args:
        model_name (str): The name of the model.

    Returns:
        None: If the hash table does not exist.
    """
    try:
        hash_tables_name = model_name + "_reverse_hash_table"
        if hash_tables_name in globals():
            hash_tables_dict = globals()[hash_tables_name]
            print(hash_tables_dict)
        else:
            return None
    except Exception as e:
        print(e)
