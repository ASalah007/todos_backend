from rest_framework import serializers
from .models import *
from attachments.models import Attachment


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


class TaskCreateSerializer(serializers.ModelSerializer):
    sub_tasks = TaskSerializer(many=True, required=False)
    files = serializers.ListField(child=serializers.FileField(), required=False)
    assign_to = serializers.EmailField(required=False)
    class Meta:
        model = Task
        fields = [
            "title",
            "list", 
            "group", 
            "notes", 
            "due_date", 
            "start_date", 
            "sub_tasks", 
            "assign_to", 
            "files",
        ]
    
    def create(self, validated_data):
        request = self.context.get("request")
        assign_to = validated_data.pop("assign_to", None)
        group = validated_data.pop("group", None)
        if assign_to:
            try: 
                user = User.objects.get(email=assign_to)
                validated_data["user"] = user
                validated_data["assigned_by"] = request.user
            except User.DoesNotExist: 
                validated_data["user"] = request.user
        else:
            validated_data["user"] = request.user

        sub_tasks = validated_data.pop("sub_tasks", [])
        files = validated_data.pop("files", [])

        task = super().create(validated_data)
        for file in files:
            file["task"] = task 
            file["group"] = group
            file["owner"] = request.user
            Attachment.objects.create(file)

        for sub_task in sub_tasks:
            sub_task["super_task"] = task
            Task.objects.create(sub_task)

        print(task)
        return task
