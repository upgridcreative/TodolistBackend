from core.models import User


def check_email_exists(email: str) -> bool:
    return User.objects.filter(email=email).exists()


def get_user_with_email(email: str) -> User:
    return User.objects.get(email=email)


def set_new_password(user_email: str, new_password: str) -> User:
    """
    Sets new password (`new_password`) for `User` with email (`user_email`) \n
    Raises error if `User` object doens't exist
    """
    user: User = User.objects.get(email=user_email)
    user.set_password(new_password)
    user.save()

    return user


def get_user_data(user: User) -> dict:
    return {
        'first_name': user.first_name,
    }
