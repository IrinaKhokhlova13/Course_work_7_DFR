from rest_framework import serializers
from datetime import timedelta


def choose_related_habit_or_reward(value):
    linked_habit = value["linked_habit"]
    reward = value["reward"]
    if linked_habit and reward:
        raise serializers.ValidationError("Нельзя одновременно выбирать связанную привычку и указывать вознаграждение")


def long_execution_time(value):
    time = timedelta(minutes=2)

    duration = value['duration']
    if duration > time:
        raise serializers.ValidationError("Время выполнения должно быть не больше 120 секунд")


def related_is_pleasant(value):
    if value["linked_habit"]:
        if not value["linked_habit"].is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки")


def pleasant_format(value):
    is_pleasant = value["is_pleasant"]
    reward = value["reward"]
    linked_habit = value["linked_habit"]
    if is_pleasant:
        if reward or linked_habit:
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки")


def completion_duration(value):
    frequency = value["frequency"]
    if frequency > 7:
        raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")
