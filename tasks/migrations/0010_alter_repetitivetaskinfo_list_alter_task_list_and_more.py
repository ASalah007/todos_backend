# Generated by Django 4.1.3 on 2023-02-20 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0009_alter_repetitivetaskinfo_assigned_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repetitivetaskinfo",
            name="list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tasks.list",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tasks.list",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
