from rest_framework.permissions import IsAuthenticated


class IsVerfified(IsAuthenticated):
    """
    Return `True` if token is valid and email is verified
    """

    def has_permission(self, request, view):
        print('working  yes i am working for sure why not')
        if super().has_permission(request, view):
            print(super().has_permission())
            return request.user.is_verified()

        return False
