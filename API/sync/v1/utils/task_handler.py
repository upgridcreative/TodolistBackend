from core.models import Task, User, Categories
import API.sync.v1.utils.errors as errors
from django.db.models import Model
# django.core.exceptions.ValidationError
# django.db.utils.IntegrityError


def create_todo(uuid: str, args: dict, temp_id: str, user: User) -> list:

    # Todo : Verify field data type.

    paylod_fields: list = args.keys()

    if 'content' not in paylod_fields:
        status = errors.ServerErrorCodes.missing_required_fields,

        # Eg. {'1121-jjj02-021':'missing_required_fields'}
        return [uuid, status], None

    _createdObject, isCreated = Task.objects.get_or_create(
        temp_id=temp_id, user=user)

    if not isCreated:  # existed already
        status = errors.ServerErrorCodes.conflicting_temp_id

        # Eg. {'1121-jjj02-021':'conflicting_temp_id'}
        return [uuid, status], None

    if 'parent_id' in paylod_fields:
        if 'child_order' not in paylod_fields:
            # Need both child order and parent_id to create a subtask
            _createdObject.delete()
            status = errors.ServerErrorCodes.missing_required_fields,
            return [uuid, status], None

        child_order = args['child_order']
        parent_id = args['parent_id']

        parent_task_object = Task.objects.filter(
            temp_id=parent_id, user=user).first() or Task.objects.filter(id=getIntObjectId(parent_id), user=user).first()

        if parent_task_object is None:
            _createdObject.delete()

            status = errors.ServerErrorCodes.parent_item_not_found,
            return [uuid, status], None

        _createdObject.setParent(parent_task_object, child_order)

    set_model_fields(args, _createdObject, writableFields=[
        'content', 'discription', 'priorty', 'is_checked', ])

    if 'due' in paylod_fields:

        _createdObject.due = args['due']

    if 'catagory_id' in paylod_fields:
        catagory_id = args['catagory_id']
        catagory_object = Categories.objects.filter(user=user, temp_id=catagory_id).first() or \
            Categories.objects.filter(user=user, id=getIntObjectId(catagory_id)).first()

        if catagory_object is not None:
            _createdObject.catagory = catagory_object

    _createdObject.save()

    temp_id_map = {
        temp_id: _createdObject.id
    }

    status = 'ok'
    return [uuid, status], temp_id_map


def update_todo(uuid: str, args: dict,  user: User) -> list:
    paylod_fields: list = args.keys()

    status, todo_object = get_object_from_payload(
        args=args, user=user, model=Task, object_key='todo_id')

    if status is not None:
        return [uuid, status]

    if 'catagory_id' in paylod_fields:
        catagory_id = args['catagory_id']
        catagory_object = Categories.objects.filter(user=user, temp_id=catagory_id).first() or \
            Categories.objects.filter(user=user, id=getIntObjectId(catagory_id)).first()

        if catagory_object is not None:
            todo_object.catagory = catagory_object

    # Todo: If due provided, validate its format

    set_model_fields(args, todo_object, writableFields=[
        'content', 'discription', 'priorty', 'due',
    ])

    todo_object.save()

    status = 'ok'
    return [uuid, status]


def delete_todo(uuid: str, args: dict,  user: User) -> list:
    paylod_fields: list = args.keys()

    status, todo_object = get_object_from_payload(
        args=args, user=user, model=Task, object_key='todo_id')

    if status is not None:
        return [uuid, status]

    todo_object.delete_task()

    status = 'ok'
    return [uuid, status]


def set_todo_completion_status(uuid: str, args: dict,  user: User, isComplete: bool):

    status, todo_object = get_object_from_payload(
        args=args, user=user, model=Task, object_key='todo_id')

    if status is not None:
        return [uuid, status]

    todo_object.is_checked = isComplete
    todo_object.save()

    status = 'ok'
    return [uuid, status]

#! Task Object Handlers End here
# ----------------------------------------------------------------------------------
#! Catagory Object Handelers Start Here


def create_catagory(uuid: str, args: dict,  user: User, temp_id) -> list:
    paylod_fields: list = args.keys()
    required_fields = ['title', 'color']

    for field in required_fields:
        if field not in paylod_fields:
            status = errors.ServerErrorCodes.missing_required_fields,

            return [uuid, status], None

    _createdObject, isCreated = Categories.objects.get_or_create(
        temp_id=temp_id, user=user)

    if not isCreated:  # existed already
        status = errors.ServerErrorCodes.conflicting_temp_id

        # Eg. {'1121-jjj02-021':'conflicting_temp_id'}
        return [uuid, status], None

    if Categories.objects.filter(user=user, title=args['title']).exists():
        _createdObject.delete()

        status = errors.ServerErrorCodes.already_exists
        return [uuid, status], None

    set_model_fields(payload=args, model=_createdObject,
                     writableFields=['title', 'color'])

    _createdObject.save()

    temp_id_map = {
        temp_id: _createdObject.id
    }

    status = 'ok'
    return [uuid, status], temp_id_map


def update_catagory(uuid: str, args: dict,  user: User) -> list:
    paylod_fields: list = args.keys()

    status, catagory_object = get_object_from_payload(
        args=args, user=user, model=Categories, object_key='catagory_id')

    if status is not None:
        return [uuid, status]

    if 'title' in paylod_fields:
        obj_with_same_title = Categories.objects.filter(
            user=user, title=args['title']).first()

        # If object exists with same title and said object is not being updated
        if obj_with_same_title is not None and (obj_with_same_title.id or None) != args['catagory_id']:
            status = errors.ServerErrorCodes.already_exists
            return [uuid, status]

    set_model_fields(args, catagory_object, writableFields=[
        'title', 'color'
    ])

    catagory_object.save()

    status = 'ok'
    return [uuid, status]


def delete_catagory(uuid: str, args: dict,  user: User) -> list:
    paylod_fields: list = args.keys()

    status, catagory_object = get_object_from_payload(
        args=args, user=user, model=Categories, object_key='catagory_id')

    if status is not None:
        return [uuid, status]

    catagory_object.delete_catagory()

    status = 'ok'
    return [uuid, status]

#! Catagory Object Handlers End Here
# ------------------------------------------------------------------


def getResorces(model: Model, sync_token: str, user: User):
    sync_date = None if sync_token is None else sync_token

    filter_options = {
        'user': user,
    }

    if sync_date is not None:
        filter_options.update({
            'on_server_creation_time__gt': sync_token
        })

    return model.objects.filter(**filter_options)


def set_model_fields(payload: dict, model: Model, writableFields: list):
    """
    Writes field values , if provided in the payload, to the model.
    """

    for writableField in writableFields:
        if writableField in payload.keys():
            setattr(model, writableField, payload[writableField])


def get_object_from_payload(args: dict, user: User, object_key: str, model: Model):

    if object_key not in args.keys():
        status = errors.ServerErrorCodes.missing_required_fields,

        return status, None

    object_id = args[object_key]
    object_id_int = getIntObjectId(object_id)
    object = model.objects.filter(temp_id=object_id, user=user).first(
    ) or model.objects.filter(id=object_id_int, user=user).first()

    if object is None:
        status = errors.ServerErrorCodes.item_not_found,
        return status, None

    return None, object


def getIntObjectId(object_id):
    try:
        return int(object_id)
    except:
        return -1
