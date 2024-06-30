from rest_framework import serializers
from habits.validators import completion_duration, choose_related_habit_or_reward, long_execution_time, \
    pleasant_format, related_is_pleasant
from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        habit = self.Meta.model.objects.create(**validated_data)
        habit.user = self.context['request'].user
        habit.save()
        return habit

    class Meta:
        model = Habit
        fields = (
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'linked_habit',
            'frequency',
            'reward',
            'duration',
            'is_public',
        )

        """
            Дополнительная валидация для сериализатора
        """
        validators = [
            choose_related_habit_or_reward,
            long_execution_time,
            related_is_pleasant,
            pleasant_format,
            completion_duration,
        ]
