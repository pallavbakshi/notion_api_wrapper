from potion.utilities.constants import ID_LENGTH_WITH_DASH


def all_object_types_are_page(results):
    for row in results:
        if row["object"] != "page":
            return False
    return True


def all_id_of_appropriate_length(ids):
    for id_ in ids:
        if len(id_) != ID_LENGTH_WITH_DASH:
            return False
    return True


def contains_desired_fields(data, desired_fields):
    if isinstance(data, list):
        for row in data:
            if set(row.keys()) - set(desired_fields) != set():
                return False
        return True
    return set(data.keys()) - set(desired_fields) == set()
