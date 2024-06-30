import os
from django.conf import settings
from datetime import datetime, timedelta

import requests

from habits.models import Habit

DAYS_OF_WEEK = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']


def send_telegram_message(message, chat_id):
    token = settings.TG_BOT_TOKEN
    data = {
        'chat_id': chat_id,
        'text': message
    }

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    response = requests.post(url, data=data)
    return response


def habit_scheduler():
    try:
        current_time = datetime.now().replace(second=0, microsecond=0)
        current_time_plus_5 = current_time + timedelta(minutes=5)

        current_day = DAYS_OF_WEEK[datetime.today().weekday()]

        habits = Habit.objects.filter(is_pleasant=False, frequency__in=[current_day, 'DAILY'],
                                      user__telegram_id__isnull=False)
        for habit in habits:
            if habit.time.strftime('%H:%M') == current_time_plus_5.strftime('%H:%M'):
                chat_id = habit.user.telegram_id
                message = f'Через 5 минут необходимо выполнять вашу привычку! ' \
                          f'Вам необходимо выполнить: {habit.action} \n'
                if habit.reward:
                    message += f'Вознаграждение: {habit.reward}'
                elif habit.linked_habit:
                    message += f'Связанная привычка: {habit.linked_habit.action}'
                else:
                    message += 'Вознаграждение или связанная привычка не указаны!'
                send_telegram_message(message=message, chat_id=chat_id)

    except Exception as e:
        print(f'Error: {e}')
