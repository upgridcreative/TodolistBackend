
# Todo : Comment the whole code
from . import errors, constansts


def parse_actions_and_requests(request):
    _actions = request.data.get('actions', None)
    _resources = request.data.get('resources', None)
    _sync_token = request.data.get('sync_token', None)

    exiculable_actions = []
    returnable_resources = []

    # ! Important todo
    # Todo: Verify all uuid are different

    if _actions is not None:

        if type(_actions) != list:
            return {
                'type': errors.ServerErrorCodes.invalid_argument_type,
                'expected': 'list',
                'argument': 'actions',
            }, None, None, None

        # ? In this step verify fields are given and their types are correct and they are indentified
        # ? Then identify the action type and store for later exicutuon

        for action in _actions:
            if type(action) != dict:
                return {
                    'type': errors.ServerErrorCodes.invalid_action_field_type,
                    'expected': 'dict',
                    'argument': 'action',
                }, None, None, None

            keys = action.keys()

            expected_fields_with_types = {
                'uuid': str,
                'type': str,
                'args': dict,
                # 'temp_id': str, #%Todo implement on create actions
            }

            for field_key, _type in expected_fields_with_types.items():
                if field_key not in keys:
                    return {
                        'type': errors.ServerErrorCodes.missing_action_arg,
                        'required': field_key,
                    }, None, None, None

                if type(action[field_key]) is not _type:
                    return {
                        'type': errors.ServerErrorCodes.invalid_action_field_type,
                        'field': field_key,
                        'expected': _type.__name__
                    }, None, None, None

                if field_key == 'type':
                    # Check if the action is valid ie if there is something that can be done with it
                    if (action['type']) not in constansts.valid_actions:
                        return {
                            'type': errors.ServerErrorCodes.invalid_action_type,
                            'field': 'type',
                        }, None, None, None

            # ? add command to actions -- later to be exicuted
            exiculable_actions.append({
                'type': action['type'],
                'args': action['args'],
                'uuid': action['uuid'],
                'temp_id':action.get('temp_id',None)
            })

    if _resources is not None:

        if type(_resources) != list:
            return {
                'type': errors.ServerErrorCodes.invalid_argument_type,
                'expected': 'list',
                'argument': 'resources',
            }, None, None, None

        for resource in _resources:
            if resource not in constansts.valid_resources:
                return {
                    'type': errors.ServerErrorCodes.invalid_action_type,
                    'field': 'resource',
                }, None, None, None

            returnable_resources.append(resource)

    # Now check if the sync token is valid

    return None, _sync_token, exiculable_actions, returnable_resources
