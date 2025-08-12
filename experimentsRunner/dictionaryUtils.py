def filterClassAttributes(data: dict, cls: type) -> dict:
    return {k: v for k, v in data.items() if k in cls.__dataclass_fields__}

def listToTuples(data: dict, cls: type):
    for field_name, value in data.items():
        field_type = cls.__dataclass_fields__[field_name].type
        
        if field_type == tuple and isinstance(value, list):
            data[field_name] = tuple(value)

    return data