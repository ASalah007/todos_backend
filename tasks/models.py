from django.db import models

from groups.models import Group
from django.contrib.auth import get_user_model


class List(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TaskAbstract(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True, blank=True)
    is_super = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    assigned_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_%(class)ss")
    super_task = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sub_tasks",
    )

    def __str__(self):
        return self.title

    class Meta: 
        abstract = True


class Task(TaskAbstract, models.Model):
    due_date = models.DateTimeField(null=True, blank=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)


class RepetitiveTaskInfo(TaskAbstract):
    repetition = models.TextField()


class RepetitiveTask(models.Model):
    repetitive_task_info = models.ForeignKey(
        RepetitiveTaskInfo, on_delete=models.CASCADE
    )
    finished_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["repetitive_task_info", "finished_date"],
                name="uq_only_one_unfinished_task",
            )
        ]
