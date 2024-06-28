# Generated by Django 4.2.13 on 2024-06-28 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="место выполнения",
                    ),
                ),
                (
                    "time",
                    models.TimeField(
                        default="12:00:00", verbose_name="время выполнения"
                    ),
                ),
                ("action", models.CharField(max_length=250, verbose_name="действие")),
                (
                    "is_pleasant",
                    models.BooleanField(
                        default=False, verbose_name="признак приятной привычки"
                    ),
                ),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("DAILY", "Daily"),
                            ("MONDAY", "Monday"),
                            ("TUESDAY", "Tuesday"),
                            ("WEDNESDAY", "Wednesday"),
                            ("THURSDAY", "Thursday"),
                            ("FRIDAY", "Friday"),
                            ("SATURDAY", "Saturday"),
                            ("SUNDAY", "Sunday"),
                        ],
                        default="DAILY",
                        verbose_name="периодичность выполнения",
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="вознаграждение",
                    ),
                ),
                (
                    "duration",
                    models.PositiveIntegerField(
                        default=2, verbose_name="продолжительность выполнения"
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(
                        default=True, verbose_name="признак публичности"
                    ),
                ),
                (
                    "linked_habit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="habits.habit",
                        verbose_name="связанная привычка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Привычка",
                "verbose_name_plural": "Привычки",
            },
        ),
    ]
