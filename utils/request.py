
def getFieldsOfRequest(request, fields):

    return_response = {}
    fieldValues = []

    for field in fields:
        value = request.data.get(field, None)
        if value is None:
            return_response.update({field: 'This field is required'})
            continue

        fieldValues.append(value)

    return len(return_response.keys()) == 0, return_response, fieldValues


def getUpdateFieldsOfRequest(request, fields):
    field_values = {}

    for field in fields:
        value = request.data.get(field, None)
        if value is None:
            continue

        field_values.update({field: value})

    return len(field_values.keys()) == 0, field_values
