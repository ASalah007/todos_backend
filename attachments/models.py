from django.db import models
from tasks.models import Task
from groups.models import Group
from django.contrib.auth import get_user_model


class Attachment(models.Model):
    file = models.FileField(upload_to="attachment/%Y/%m")
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    

