from khapi.cache_system.hash import dict_hash_tables_update

from .cache_models import *


class DictManager:
    def __init__(self, model_name):
        self.model_name = model_name
        self.dict_name = model_name + "_dict"
        self.global_dict = globals().get(self.dict_name, {})
        self.model_dict = self.global_dict

    def create(self, obj_id, data):
        self.model_dict[f"{obj_id}"] = data
        self.global_dict[f"{obj_id}"] = data
        dict_hash_tables_update(self.model_name)

    def update(self, obj_id, data):
        if f"{obj_id}" in self.model_dict:
            self.model_dict[f"{obj_id}"].update(data)
            self.global_dict[f"{obj_id}"].update(data)
            dict_hash_tables_update(self.model_name)
        else:
            self.create(obj_id, data)
            dict_hash_tables_update(self.model_name)

    def delete(self, obj_id):
        if f"{obj_id}" in self.model_dict:
            del self.model_dict[f"{obj_id}"]
            # del self.global_dict[f"{obj_id}"]
            dict_hash_tables_update(self.model_name)

    def get(self, obj_id):
        return self.model_dict.get(f"{obj_id}", None)
