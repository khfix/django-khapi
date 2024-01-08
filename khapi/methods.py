import os


def exclode_fields_data(data, exclude_fields=[]):
    temp_data = data.copy()
    if type(temp_data) == dict:
        for exclude_field in exclude_fields:
            if exclude_field in temp_data.keys():
                temp_data.pop(exclude_field)
        return temp_data
    else:
        for _temp_data in temp_data:
            for exclude_field in exclude_fields:
                if exclude_field in _temp_data.keys():
                    _temp_data.pop(exclude_field)
        return temp_data


def khapi_upload_path(
    instance,
    filename,
):
    base_upload_to = instance.__class__.__name__
    file_root, file_extension = os.path.splitext(filename)
    file_path = os.path.join(base_upload_to, filename)
    counter = 1
    while os.path.exists(file_path):
        new_filename = f"{file_root}({counter}){file_extension}"
        file_path = os.path.join(base_upload_to, new_filename)
        counter += 1
    return file_path
