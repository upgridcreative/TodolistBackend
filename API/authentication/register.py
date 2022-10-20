import threading

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.request import getFieldsOfRequest
from utils.token import get_tokens_for_user
from utils.user import check_email_exists
from utils.validators import is_valid_email, is_valid_password

import utils.otp as otp_utils
from core.models import User


@api_view(['POST', ])
def register_user(request):
    exists, response, fields = getFieldsOfRequest(
        request, ['email', 'password', 'name'])

    if not exists:
        return Response(
            data={'required': response, 'code': 'fields-not-given'}, status=400)

    email, password, name = fields
    #Todo: Check if name is empty
    #Todo:Check if email exists (as in if the email is realy a valid email)

    if not is_valid_email(email):
        return Response(
            {'fields': {'email': 'This field is invalid'}, 'code': 'invalid-email'})

    is_valid, response = is_valid_password(password)

    if not is_valid:
        return Response(
            {'fields': {'password': response}, 'code': 'weak-password'})

    already_exists = check_email_exists(email)

    if already_exists:
        return Response(
            {'email': 'user already exists', 'code': 'already-exists'})

    instance: User = User(
        email=email, name=name)

    instance.set_password(password)  # Set hashed password
    instance.save()

    threading.Thread(target =otp_utils.send_email_verification,args=(instance,)).start() #Resort to this method of verification better UI experice 
    tokens = get_tokens_for_user(instance)

    return Response(
        data={'code': 'successful', 'tokens': tokens}, status=200)


@permission_classes([IsAuthenticated, ])
@api_view(['POST',])
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
        data={'code': 'successful'}, status=200)
