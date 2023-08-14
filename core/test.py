from django.test import TestCase
from .models import *
from django.db.utils import *

from API.sync.v1.utils.task_handler import *
import requests
import json

class TaskTest(TestCase):
	access: str
	json: dict

	def setUp(self) -> None:
		print('je;;l')

		response = requests.post(
			url='http://127.0.0.1:8000/api/auth/login/',
			json={
				'email': 'farhansyedain@gmail.com',
				'password': 'farhan11',
			}
		)
		self.access = response.json()['tokens']['access']
		self.json = response.json()
		self.createTasks()

	def createTasks(self):
		payload = {
			'actions': [
				{
					'uuid': 'f-1',  # For future testing
					'temp_id': 'ft-1',
					'args': {
									"content": "Testting Todo 1",
					},
					'type': 'todo_add',
				},
				{
					'uuid': 'f-2',  # For future testing
					'temp_id': 'ft-2',
					'args': {
									"content": "Testting Todo 2",
					},
					'type': 'todo_add',
				},

				# start form here ===================
				{
					'uuid': '1',  # Simply try adding a todo -> 1:ok
					'temp_id': 't-1',
					'args': {
						"content": "First Todo",
					},
					'type': 'todo_add',
				},
				{
					'uuid': '2',  # Simply try adding a todo with other fields too-> 1:ok
					'temp_id': 't-2',
					'args': {
						"content": "Second Todo",
						"due": '2022-12-8',
						'discription': 'This is the discriptino of the second task',
						'priorty': 1,
						'parent_id': 1,
						'child_order': 1,

					},
					'type': 'todo_add',
				},
				{
					'uuid': '3',  # This should not exicute since we wont pass chidl order this time
					'temp_id': 't-3',
					'args': {
						"content": "Third Todo",
						"due": '2022-12-8',
						'discription': 'This is the discriptino of the second task',
						'priorty': 1,
						'parent_id': 1,
						# 'child_order': 1,
					},
					'type': 'todo_add',
				},
				{
					'uuid': '4',  # Didn't pass the required fields, shoul'd not exicute
					'temp_id': 't-4',
					'args': {

					},
					'type': 'todo_add',
				},
				{
					'uuid': '5',  # The temp_id is confilcting
					'temp_id': 't-3',
					'args': {

					},
					'type': 'todo_add',
				},

				{
					'uuid': '5',  # The content is confilting should still be ok
					'temp_id': 't-5',
					'args': {
						'content': 'First Todo'
					},
					'type': 'todo_add',
				},
				{
					'uuid': '6',  # The parent doens't exist
					'temp_id': 't-6',
					'args': {
						'content': 'First Todo',
						'parent_id': 10,
						'child_order': 1
					},
					'type': 'todo_add',
				},
				{
					'uuid': '8',  # pass temp id of the parent
					'temp_id': 't-7',
					'args': {
						'content': 'First Todo',
						'parent_id': 't-1',
						'child_order': 1
					},
					'type': 'todo_add',
				},
				{
					'uuid': '9',  # Catagory doens't exist , but it should still pas
					'temp_id': 't-8',
					'args': {
						'content': 'First Todo',
						'catagory_id': 1
					},
					'type': 'todo_add',
				},


				# --------------Update releated now------------
				{
					'uuid': '10',  # Catagory doens't exist , but it should still pas and update
					'args': {
						'content': 'First Todo updated',
						'todo_id': 3,
						'catagory_id': 1,
					},
					'type': 'todo_update',
				},

				{
					'uuid': '11',  # missing a require field
					'args': {

					},
					'type': 'todo_update',
				},

				{
					'uuid': '12',  # pass temp_id and uodate other fields too
					'args': {
						'todo_id': 't-2',
						'due': '2002-11-11',  # valid
					},
					'type': 'todo_update',
				},

				# Now deleteing stuff

				{
					'uuid': '13',  # pass temp_id and uodate other fields too
					'args': {
						'todo_id': 1,
					},
					'type': 'todo_delete',
				},
				{
					'uuid': '14',  # pass temp_id and uodate other fields too
					'args': {
						'todo_id': 'ft-2',
					},
					'type': 'todo_delete',
				},

				{
					'uuid': '15',  # pass temp_id and uodate other fields too
					'args': {
					},
					'type': 'todo_delete',
				},


			]
		}

		response = requests.post(
			url='http://127.0.0.1:8000/api/sync/v1/',
			headers={
				'Authorization': f'Bearer {self.access}', }, json=payload,
		)

		
TaskTest().setUp()
