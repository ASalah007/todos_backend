from django.db import models
from users.models import User
from django.core.mail.backends.smtp import EmailBackend


class List(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=64)
    due_date = models.DateTimeField(null=True, blank=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    is_super = models.BooleanField(default=False)
    super_task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class RepetitiveTaskInfo(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    repetition = models.TextField()
    is_super = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    super_task = models.ForeignKey(
        "RepetitiveTaskInfo",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sub_tasks",
    )

    def __str__(self):
        return self.title


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
