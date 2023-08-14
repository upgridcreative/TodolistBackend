from enum import Enum


class ServerErrorCodes(Enum):

    invalid_argument_type = {
        'status_code': 400,
        'name': 'invalid_argument_type',
    }
    invalid_action_field_type = {
        'status_code': 400,
        'name': 'invalid_action_field_type',
    }
    invalid_action_arg = {
        'status_code': 400,
        'name': 'invalid_action_arg',
    }
    missing_action_arg = {
        'status_code': 400,
        'name': 'missing_action_arg',
    }
    invalid_action_type = {
        'status_code': 400,
        'name': 'invalid_action_type',
    }
    missing_required_fields = {
        'status_code': 400,
        'name': 'missing_required_fields',
    }
    conflicting_temp_id = {
        'status_code': 400,
        'name': 'conflicting_temp_id',
    }
    parent_item_not_found = {
        'status_code': 400,
        'name': 'parent_item_not_found',
    }

    item_not_found = {
        'status_code': 400,
        'name': 'item_not_found',
    }

    already_exists = {
        'status_code': 400,
        'name': 'already_exists',
    }