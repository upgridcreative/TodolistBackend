from django.contrib.auth import authenticate
from utils.user import check_email_exists, get_user_data
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utils.request import getFieldsOfRequest
from utils.token import get_tokens_for_user

@api_view(['POST', ])
def login(request):

    exists, response, fieldValues = getFieldsOfRequest(
        request, ['email', 'password'])

    if not exists:
        return Response(data={'required': response, 'code': 'fields-not-given'}, status=400)

    email, password = fieldValues

    # TODO: pass user class to be authenticated #Dont know what that todo was all about

    if not check_email_exists(email):
        return Response(data={'email': 'No user exists with this email adress', 'code': 'no-user-exists'})

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response(data={'password': 'This field is incorrect', 'code': 'incorrect-password'})

    tokens = get_tokens_for_user(user)

    details = get_user_data(user)

    return Response(
		{'code': 'successful', 'tokens': tokens, 'details':details})
