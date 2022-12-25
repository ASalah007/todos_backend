from celery import shared_task
from .models import RepetitiveTask, RepetitiveTaskInfo
from datetime import datetime, timedelta
from .commons import REPETITION_REGEX
import re


@shared_task
def task_generate_next_task(rep_task_id):
    generate_next_task(RepetitiveTask.objects.get(pk=rep_task_id).repetitive_task_info)


def generate_next_task(rep_task_info: RepetitiveTaskInfo):
    """
    This function will generate the next task for a repetitive task that
    doesn't repeat on specific day(s): e.g. 3 times per week, 5 times per month

    this function assumes it will be called whenver the user finished or skipped the task

    in another words, there is no unfinished task in RepetitiveTask table.
    """
    m = re.search(REPETITION_REGEX, rep_task_info.repetition)
    task_goal = m.group(1)  # \d+
    range = m.group(2)  # [mydw]
    today = datetime.now()
    tommorrow = today + timedelta(days=1)

    def create_task_on(day):
        RepetitiveTask.objects.create(
            repetitive_task_info=rep_task_info,
            start_date=day,
            notes=rep_task_info.notes,
        )

    def prev_tasks_count(**range):
        return RepetitiveTask.objects.filter(
            repetitive_task_info=rep_task_info,
            **range,
        ).count()

    def generate_task(prev_tasks, next_time):
        create_task_on(tommorrow if prev_tasks < task_goal else next_time)

    match (range):
        case "d":
            create_task_on(tommorrow)

        case "w":
            first_day_next_week = (
                today + timedelta(weeks=1) - timedelta(days=today.weekday())
            )
            generate_task(
                prev_tasks=prev_tasks_count(start_date__week=today.isocalender().week),
                next_time=first_day_next_week,
            )

        case "m":
            first_day_next_month = datetime(year=today.year, month=today.month, day=1)
            generate_task(
                prev_tasks=prev_tasks_count(start_date__month=today.month),
                next_time=first_day_next_month,
            )

        case "y":
            first_day_next_year = datetime(year=today.year + 1, month=1, day=1)
            generate_task(
                prev_tasks=prev_tasks_count(start_date__year=today.year),
                next_time=first_day_next_year,
            )

    # if it is super task generate all of it sub tasks
    if rep_task_info.is_super:
        for sub_task in rep_task_info.sub_tasks.all():
            generate_next_task(sub_task)
