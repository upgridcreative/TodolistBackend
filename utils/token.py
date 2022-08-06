from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from core.models import User


def get_tokens_for_user(user: User):
    outstanding_tokens = OutstandingToken.objects.filter(
        user=user)

    for out_token in outstanding_tokens:
        if hasattr(out_token, 'blacklistedtoken'):
            # Token already blacklisted. Skip
            continue

        BlacklistedToken.objects.create(token=out_token)

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
