from django.contrib import admin

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin

from .models import User, OutstandingTokenAdmin


admin.site.register(User)


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
