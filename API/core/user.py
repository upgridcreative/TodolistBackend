from core.models import User
from utils.permission import IsVerfified
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from utils.user import check_email_exists
from django.contrib.auth import authenticate

from utils.request import getFieldsOfRequest, getUpdateFieldsOfRequest


@permission_classes([IsVerfified])
@api_view(['PUT', ])
def update_user(request):

    exists, fields = getUpdateFieldsOfRequest(
        request, User().get_updatible_fields())

    updated_fields = {}

    if not exists:
        # Todo: Validate fields first

        User.objects.filter(email=request.user.email).update(**fields)

        user_object = User.objects.get(email=request.user.email)

        for field in fields:
            updated_fields.update({field: getattr(user_object, field)})

    return Response(data={'code': 'successfull', 'updated_fields': updated_fields}, status=200)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_user(request):

    exists, response, fieldValues = getFieldsOfRequest(
        request, [ 'password'])

    if not exists:
        return Response(data={'required': response, 'code': 'fields-not-given'}, status=400)

    password = fieldValues[0]

 
    user = authenticate(request, email=request.user.email, password=password)

    if user is None:
        return Response(data={'password': 'This field is incorrect', 'code': 'incorrect-password'})

    user.delete()

    # Todo :  status code correction
    return Response(data={'code': 'successful'}, status=200)
