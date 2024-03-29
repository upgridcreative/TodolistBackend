import threading

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.request import getFieldsOfRequest
from utils.token import get_tokens_for_user
from utils.user import check_email_exists,get_user_data
from utils.validators import is_valid_email, is_valid_password

import utils.otp as otp_utils
from core.models import User


@api_view(['POST', ])
def register_user(request):
    exists, response, fields = getFieldsOfRequest(
        request, ['email', 'password', 'first_name','last_name'])

    if not exists:
        print('error')
        return Response(
            data={'required': response, 'code': 'fields-not-given'}, status=400)

    email, password, f_name, l_name = fields
    # Todo: Check if name is empty
    # Todo:Check if email exists (as in if the email is realy a valid email)

    if not is_valid_email(email):
        print('error 2')

        return Response(
            {'fields': {'email': 'This field is invalid'}, 'code': 'invalid-email'}, status=400)

    is_valid, response = is_valid_password(password)

    # if not is_valid:
    #     print('error 22')

    #     return Response(
    #         {'fields': {'password': response}, 'code': 'weak-password'}, status=400)

    already_exists = check_email_exists(email)

    if already_exists:
        print('error2222')

        return Response(
            {'email': 'user already exists', 'code': 'already-exists'}, status=400)

    instance: User = User(
        email=email, first_name=f_name,last_name=l_name)

    instance.set_password(password)  # Set hashed password
    instance.save()

    threading.Thread(target=otp_utils.send_email_verification, args=(
        instance,)).start()  

    tokens = get_tokens_for_user(instance)
    details = get_user_data(instance)

    return Response(
        data={'code': 'successful', 'tokens': tokens,'details':details}, status=201)


@permission_classes([IsAuthenticated, ])
@api_view(['POST', ])
def verify_email(request):
    exists, response, fields = getFieldsOfRequest(
        request, ['otp'])

    if not exists:
        return Response(
            data={'required': response, 'code': 'fields-not-given'}, status=400)

    otp = fields[0]

    user = request.user

    if not otp_utils.verify_email(user, otp):
        return Response(
            {'fields': {'otp': 'this field is incorrect'},
             'code': 'invalid-otp'})

    user.mark_verified()

    return Response(
        data={'code': 'successful'}, status=200,)
