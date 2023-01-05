from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _



class Group(models.Model):
    title = models.CharField(max_length=32)
    users = models.ManyToManyField(User, through="Membership", through_fields=("group", "user")) 

    def __str__(self):
        return self.title
  


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Role(models.IntegerChoices):
        LEADER = 1, _("Leader")
        MEMBER = 2, _("Member")
        GUEST  = 3, _("Guest")

    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.MEMBER, blank=True, null=True)
    can_assign_tasks = models.BooleanField(default=False, blank=True, null=True)
    can_add_members = models.BooleanField(default=False, blank=True, null=True)
    can_edit_group = models.BooleanField(default=False, blank=True, null=True)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['group', 'user'], name="unique member")
        ]