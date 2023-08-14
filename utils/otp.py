from datetime import datetime
from random import randint

from django.core.mail import send_mail
from core.models import User, VerifyEmailKey


def send_otp(email, otp) -> bool:
    try:
        send_mail(
            'OTP for email verification',
            f'The OTP for email varification  for your email {email} is {otp}',
            'flutterwavelance@outlook.com',
            [email],
            fail_silently=False,
        )
        return True

    except Exception as e:
        print('failed to send otp for email verification')
        print(e)
        return False


def send_email_verification(user: User) -> str:
    otp = generate_otp_email_verify(user)
    print(otp)
    send_otp(user.email, otp)


def generate_otp_email_verify(user: User) -> str:
    otp = ''.join([str(randint(0, 9)) for _ in range(6)])
    reset_key, created = VerifyEmailKey.objects.get_or_create(user=user)

    reset_key.key = otp
    reset_key.generated_at = datetime.now()
    reset_key.save()

    return otp


def verify_email(user: User, otp: str) -> bool:
    reset_key, created = VerifyEmailKey.objects.get_or_create(user=user)
    if created:
        reset_key.delete()
        return False

    if reset_key.key == otp:
        reset_key.delete()
        return True

    return False
