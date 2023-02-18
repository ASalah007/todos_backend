# Generated by Django 4.1.3 on 2023-02-03 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0006_repetitivetaskinfo_assigned_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repetitivetaskinfo",
            name="assigned_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_tasks_%(class)s_related",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="assigned_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_tasks_%(class)s_related",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
