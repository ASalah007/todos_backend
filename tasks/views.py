from collections import defaultdict
from datetime import datetime

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .tasks import task_generate_next_task


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class RepetitiveTaskInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepetitiveTaskInfo.objects.all()
    serializer_class = RepetitiveTaskInfoSerializer
    permission_classes = [IsAuthenticated]


class RepetitiveTaskInfoCreateView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = RepetitiveTaskInfoSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, *args, **kwargs):
        rep_task_info = self.create(*args, **kwargs)
        RepetitiveTask.objects.create(
            repetitive_task_info_id=rep_task_info.data["id"],
            start_date=datetime.now(),
            notes=rep_task_info.data["notes"],
        )
        return Response(rep_task_info, status=status.HTTP_201_CREATED)


class RepetitiveTaskEditView(generics.RetrieveUpdateAPIView):
    queryset = RepetitiveTask.objects.all()
    serializer_class = RepetitiveTaskSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        task = get_object_or_404(RepetitiveTask, pk=kwargs["pk"])

        # if the user finished the a non-subtask task then generate a new task
        if (
            request.data.get("finished_date")
            and not task.repetitive_task_info.super_task
        ):
            task_generate_next_task.delay(task.id)

        # the user undid the finish action then delete the generated task that
        # got generated when he finished the task, this undo the above if condition
        elif request.data.get("finished_date") == "":
            new_task = RepetitiveTask.objects.filter(start_date__gt=task.start_date)
            if new_task.count() == 1:
                new_task.delete()

        return self.partial_update(request, *args, **kwargs)


class ListCreateView(generics.CreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]


class UserAllTaskslView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        lists = list(List.objects.filter(user_id=user_id))
        lists_dict = {}
        for l in lists:
            lists_dict[l.id] = {
                "title": l.title,
                "tasks": [],
                "super_tasks": [],
                "repetitive_tasks": [],
                "repetitive_super_tasks": [],
            }

        # get all unfinished tasks
        tasks = list(Task.objects.filter(user_id=user_id, finished_date__isnull=True))

        # this dict will hold super tasks' sub tasks: super -> [sub, sub, ...]
        sub_tasks_dict = defaultdict(list)

        for task in tasks:
            task_data = TaskInfoSerializer(task).data

            # normal tasks
            if not (task.is_super or task.super_task):
                lists_dict[task.list_id]["tasks"].append(task_data)

            # store the sub tasks in a temp dict
            elif not task.is_super:
                sub_tasks_dict[task.super_task_id].append(task_data)

            # super tasks
            else:
                lists_dict[task.list_id]["super_tasks"].append(task_data)

        # add all sub tasks to their super tasks
        for id, lst in lists_dict.items():
            for super_task in lst["super_tasks"]:
                super_task["sub_tasks"] = sub_tasks_dict[super_task["id"]]

        # get all repetitive tasks
        rep_tasks = list(
            RepetitiveTask.objects.select_related("repetitive_task_info")
            .filter(finished_date__isnull=True, repetitive_task_info__user=user_id)
            .annotate(
                title=F("repetitive_task_info__title"),
                super_note=F("repetitive_task_info__notes"),
                is_super=F("repetitive_task_info__is_super"),
                super_task=F("repetitive_task_info__super_task"),
                list_id=F("repetitive_task_info__list_id"),
            )
        )

        # this dict will hold repetitive super tasks' sub tasks: super -> [sub, sub]
        sub_tasks_dict = defaultdict(list)

        for rep_task in rep_tasks:
            rep_task_data = RepTaskInfoSerializer(rep_task).data

            # normal tasks
            if not (rep_task.is_super or rep_task.super_task):
                lists_dict[rep_task.list_id]["repetitive_tasks"].append(rep_task_data)

            # store the sub tasks in a temp dict
            elif not rep_task.is_super:
                sub_tasks_dict[rep_task.super_task].append(rep_task_data)

            # super tasks
            else:
                lists_dict[rep_task.list_id]["repetitive_super_tasks"].append(
                    rep_task_data
                )

        # add sub tasks to their super task
        for id, lst in lists_dict.items():
            for super_task in lst["repetitive_super_tasks"]:
                super_task["sub_tasks"] = sub_tasks_dict[super_task["id"]]

        result = []
        for id, lst in lists_dict.items():
            lst['id'] = id
            result.append(lst)

        print(result)
        return Response(result)

