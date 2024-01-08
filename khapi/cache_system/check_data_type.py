def check_data_type(data):
    if data == "CharField":
        return "str"
    elif data == "TextField":
        return "str"
    elif data == "BigAutoField":
        return "int"
    elif data == "IntegerField":
        return "int"
    elif data == "BooleanField":
        return "bool"
    elif data == "DateTimeField":
        return "datetime"
    elif data == "DateField":
        return "date"
    elif data == "TimeField":
        return "time"
    elif data == "FloatField":
        return "float"
    elif data == "DecimalField":
        return "decimal"
    elif data == "EmailField":
        return "email"
    elif data == "FileField":
        return "django.core.files.uploadedfile.InMemoryUploadedFile"
    elif data == "ImageField":
        return "image"
    elif data == "URLField":
        return "url"
    elif data == "UUIDField":
        return "uuid"
    elif data == "ForeignKey":
        return "foreignkey"
    elif data == "ManyToManyField":
        return "manytomany"
    elif data == "OneToOneField":
        return "onetoone"
    elif data == "GenericForeignKey":
        return "genericforeignkey"
    elif data == "GenericRelation":
        return "genericrelation"
    elif data == "AutoField":
        return "autofield"
    elif data == "BigIntegerField":
        return "biginteger"
    elif data == "BinaryField":
        return "binary"
    else:
        return "unknown"
