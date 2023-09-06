from rest_framework import serializers
from core.models import *



class CatagoryIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'temp_id'
                  ]
class TaskSerializer(serializers.ModelSerializer):
    catagory = CatagoryIdSerializer()
    class Meta:
        model = Task
        fields = ['id', 'temp_id', 'parent_temp_id',
                  'parent', 'child_order', 'catagory', 'content',
                  'discription', 'due', 'priorty', 'is_checked', 'is_deleted', ]



class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'temp_id', 'title', 'color','is_deleted']
