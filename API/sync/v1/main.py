from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from utils.permission import IsAuthenticated
from .utils.parse import *
from .utils.serializers import *
from .utils.task_handler import (
    create_todo, getResorces, update_todo, delete_todo, set_todo_completion_status, create_catagory, update_catagory, delete_catagory)

from core.models import Task, Categories


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def sync_api_main_v1(request):
    user = request.user

    _errors, sync_token, actions, resources = parse_actions_and_requests(
        request)

    if (_errors or {}).keys().__len__() > 0:
        status_code = _errors['type'].value['status_code']
        _errors['type'] = _errors['type'].value['name']

        return Response(data=_errors, status=status_code)

    temp_id_mapping = {}
    action_statuses = []
    requested_resources = {}
    new_sync_token = None

    for action in actions:

        uuid = action['uuid']
        args = action['args']
        action_status = None

        if action['type'] == 'todo_add':
            temp_id = action['temp_id']

            action_status, indie_temp_id_mapping = create_todo(
                uuid=uuid, args=args, user=user, temp_id=temp_id)

            if indie_temp_id_mapping is not None:
                temp_id_mapping.update(indie_temp_id_mapping)

        elif action['type'] == 'todo_update':
            action_status = update_todo(uuid=uuid, args=args, user=user)

        elif action['type'] == 'todo_delete':
            action_status = delete_todo(uuid=uuid, args=args, user=user)

        elif action['type'] == 'todo_check':
            action_status = set_todo_completion_status(
                uuid=uuid, args=args, user=user, isComplete=True)

        elif action['type'] == 'todo_uncheck':
            action_status = set_todo_completion_status(
                uuid=uuid, args=args, user=user, isComplete=False)

        elif action['type'] == 'catagory_add':
            temp_id = action['temp_id']

            action_status, indie_temp_id_mapping = create_catagory(
                uuid=uuid, args=args, user=user, temp_id=temp_id)
            if indie_temp_id_mapping is not None:
                temp_id_mapping.update(indie_temp_id_mapping)

        elif action['type'] == 'catagory_update':
            action_status = update_catagory(
                uuid=uuid, args=args, user=user,
            )

        elif action['type'] == 'catagory_delete':
            action_status = delete_catagory(
                uuid=uuid, args=args, user=user,
            )

        status_value = 'ok'
        if action_status[1] != 'ok':
            if type(action_status[1]) is not tuple:
                status_value = action_status[1].name

            else:
                status_value = action_status[1][0].name

        action_statuses.append({action_status[0]: status_value})

    cat_last_creation_date = Categories.objects.all().order_by('on_server_creation_time'
                                                               ).last().on_server_creation_time if Categories.objects.all().exists() else None

    task_last_creation_date = Task.objects.all().order_by('on_server_creation_time'
                                                          ).last().on_server_creation_time if Task.objects.all().exists() else None

    if task_last_creation_date is None and cat_last_creation_date is None:
        new_sync_token = ''

    elif task_last_creation_date is None or cat_last_creation_date is None:
        new_sync_token = task_last_creation_date or cat_last_creation_date

    else:
        new_sync_token = cat_last_creation_date if cat_last_creation_date > task_last_creation_date else task_last_creation_date

    # Done with the actions #MubrakMe

    if 'all' in resources:
        resources = ['catagories', 'todos']  # This includes everything

    for resource in resources:
        print(resource);
        if resource == 'todos':
            obtained = getResorces(Task, sync_token, user=user)
            all_tasks = []
            for item in obtained:
                serialized = TaskSerializer(item)

                all_tasks.append(serialized.data)

            requested_resources.update({'tasks': all_tasks})

        if resource == 'catagories':
            obtained = getResorces(Categories, sync_token, user=user)
            all_catagory = []
            for item in obtained:
                serialized = CatagorySerializer(item)

                all_catagory.append(serialized.data)

            requested_resources.update({'catagories': all_catagory})

    return Response(data={
        # 'full_sync':sync_token  #todo add later

        **requested_resources,
        'sync_token': '' if new_sync_token is None else new_sync_token,
        'temp_id_mapping': temp_id_mapping,
        'sync_status': action_statuses,

    })
