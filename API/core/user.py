from core.models import Categories
from utils.permission import IsVerfified
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.request import getFieldsOfRequest, getUpdateFieldsOfRequest

@permission_classes([IsVerfified])
@api_view(['PUT'])
def update_user(request):
	pass


@permission_classes([IsVerfified])
@api_view(['DELETE'])
def delete(request):
	pass