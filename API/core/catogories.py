from core.models import Categories
from utils.permission import IsVerfified
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.request import getFieldsOfRequest, getUpdateFieldsOfRequest


@permission_classes([IsAuthenticated, ])
@api_view(['POST', ])
def create_catagory(request):
    user = request.user
    print(user)

    exists, response, fields = getFieldsOfRequest(
        request, ['title', 'color', ])

    if not exists:
        return Response(
            data={'required': response, 'code': 'fields-not-given'}, status=400)

    title, color = fields

    obj, created = Categories.objects.get_or_create(
        user=user, title=title)

    if created:
        obj.color = color
        obj.save()

        return Response(data={
            'code': 'successfull',
            'details': {'id': obj.id, 'title': obj.title, 'color': obj.color, }, },
            status=200)

    return Response(
        data={'code': 'already-exists', 'title': 'Catogory already exists'}, status=400)


@permission_classes([IsVerfified, ])
@api_view(['DELETE', ])
def delete_catagory(request, pk):
    user = request.user
    

    if Categories.objects.filter(id=pk, user=user).exists():

        Categories.objects.filter(id=pk).delete()

        return Response(
            data={'code': 'successfull'}, status=200)

    return Response(
        data={'code': 'not-found', 'id': 'no catagory with this id and user credentials exists'}, status=400)


@permission_classes([IsVerfified, ])
@api_view(['PUT', ])
def update_catagory(request, pk):
    user = request.user
    data = request.data

    if Categories.objects.filter(id=pk, user=user).exists():

        exists, fields = getUpdateFieldsOfRequest(
            request, Categories().get_updatible_fields())

        if exists:
            Categories.objects.get(id=pk, user=user).update_fields(**fields)


        return Response(data={'code':'successfull'},status=200)

    return Response(
        data={'code': 'not-found', 'id': 'no catagory with this id and user credentials exists'}, code=400)
