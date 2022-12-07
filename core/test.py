from django.test import TestCase
from .models import *
from django.db.utils import *

from API.sync.v1.utils.task_handler import *


class TaskTest(TestCase):
    def setUp(self) -> None:

        User.objects.create(email='test@test.com',
                            password='jopefasd3111waA', first_name='Farhan')

        user = User.objects.get(id=1)

        actions = [

            {  # Should be sucessfull
                'uuid': 1,
                'temp_id': 't-1',
                'args': {
                    'title': 'Test',
                    'color': 'white',

                },
                'user': user,

            },

            {  # Missing title
                'uuid': 2,
                'temp_id': 't-2',
                'args': {
                    'color': 'white',
                },
                'user': user,

            },

            {  # Missing color
                'uuid': 3,
                'temp_id': 't-3',

                'args': {
                    'title': 'white',

                },
                'user': user,

            },
            {  # title already exists
                'uuid': 11,
                'temp_id': 't-4',

                'args': {
                    'title': 'Test',
                    'color': 'Doenstl matetr can be repeatedl',

                },
                'user': user,

            },
            {  # Reserve this for testing update
                'uuid': 11,
                'temp_id': 't-11',

                'args': {
                    'title': 'Test 1',
                    'color': 'Doenstl matetr can be repeatedl',

                },
                'user': user,

            },

        ]

        updates = [


            {
                'uuid': 5,
                'args': {
                    'title': 'New Title',
                    'catagory_id': 1,  # will update uuid 1
                },
                'user': user,
            },
            {
                'uuid': 6,
                'args': {
                    'color': 'New Color',
                    'title': 'New new title',
                    'catagory_id': 1,  # will update uuid 1
                },
                'user': user,
            },
            {
                'uuid': 7,
                'args': {
                },
                'user': user,
            },
            {
                'uuid': 8,
                'args': {
                    'catagory_id': 1
                },
                'user': user,
            },
            {
                'uuid': 9,
                'args': {
                    'catagory_id': 1,
                    'title': 'New new title',

                },
                'user': user,
            },

            {
                'uuid': 10,
                'args': {
                    'catagory_id': 3,
                    'title': 'New new title',

                },
                'user': user,
            },
        ]

        deletitions = [



            {

                'uuid': 'd-1',
                'args': {
                    'catagory_id': 1,
                }, 'user': user,
            },
            {

                'uuid': 'd-1',
                'args': {
                    'catagory_id': 2,
                }, 'user': user,
            },
            {

                'uuid': 'd-1',
                'args': {
                }, 'user': user,
            },

        ]

        for action in actions:
            response = create_catagory(
                **action
            )
            print(response)

        for update in updates:
            response = update_catagory(
                **update
            )
            print(response)


    

    def testDates(self):
        all_tasks = Categories.objects.all()
        
        dt = all_tasks.first().on_server_creation_time
        dtt = all_tasks.last().on_server_creation_time

        print(dt> dtt)

        # print(all_tasks)

        r = getResorces(Categories,dtt,user=all_tasks.first().user)
        print(r)
