
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
