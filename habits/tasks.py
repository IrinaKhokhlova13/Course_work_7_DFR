from celery import shared_task

from habits.services import habit_scheduler


@shared_task
def habit_reminders():
    habit_scheduler()

