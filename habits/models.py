from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Habit(models.Model):
    class HabitFrequency(models.TextChoices):
        Daily = 'DAILY'
        monday = 'MONDAY'
        tuesday = 'TUESDAY'
        wednesday = 'WEDNESDAY'
        thursday = 'THURSDAY'
        friday = 'FRIDAY'
        saturday = 'SATURDAY'
        sunday = 'SUNDAY'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    place = models.CharField(max_length=100, verbose_name='место выполнения', **NULLABLE)
    time = models.TimeField(default='12:00:00', verbose_name='время выполнения')
    action = models.CharField(max_length=250, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    frequency = models.CharField(choices=HabitFrequency.choices,
                                 default=HabitFrequency.Daily, verbose_name='периодичность выполнения')
    reward = models.CharField(max_length=250, verbose_name='вознаграждение', **NULLABLE)
    duration = models.PositiveIntegerField(default=2, verbose_name='продолжительность выполнения')
    is_public = models.BooleanField(default=True, verbose_name='признак публичности')

    def __str__(self):
        return f"{self.user} в {self.time}, будет {self.action} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = 'Привычки'
