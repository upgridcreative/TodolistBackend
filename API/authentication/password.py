from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.request import getFieldsOfRequest

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])

def reset_password(request):

    exists, response, fieldValues = getFieldsOfRequest(
        request, ['password'])

    if not exists:
        return Response(data={'required': response, 'code': 'fields-not-given'}, status=400)

    password = fieldValues[0]

    user = request.user
    try:
        user.set_password(password)  # Set hashed password
        user.save()
    except Exception as e:
        print(e)
        return Response({'code':'unexpected-error'})

    return Response(
		{'code': 'successful', },)
