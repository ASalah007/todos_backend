# Generated by Django 4.1.3 on 2022-12-29 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="can_add_members",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="membership",
            name="can_assign_tasks",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="membership",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, "Leader"), (2, "Member"), (3, "Guest")],
                default=2,
            ),
        ),
    ]