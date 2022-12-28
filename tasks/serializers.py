from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {
            'user': {'read_only': True}
        }

    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class RepetitiveTaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepetitiveTaskInfo
        fields = "__all__"
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)
    
        


class RepetitiveTaskSerializer(serializers.ModelSerializer):
    # def update(self, instance, validated_data):
    #     instance.finished_date = validated_data.get(
    #         "finished_date", instance.finished_date
    #     )
    #     instance.notes = validated_data.get("notes", instance.notes)
    #     instance.save()
    #     return instance

    class Meta:
        model = RepetitiveTask
        fields = "__all__"


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"
        extra_kwargs ={
            'user': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = request.user
        return super().create(validated_data)
        


class TaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "due_date", "start_date", "notes"]


class RepTaskInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=64)
    notes = serializers.CharField(max_length=2048)
