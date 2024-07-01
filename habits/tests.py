from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self):
        """ Подготовка к тестированию """
        self.user = User(
            email="test@gmail.com",
            password="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        self.user.set_password("test")
        self.user.save()

        response = self.client.post(
            reverse('users:token_obtain_pair'),
            {"email": "test@gmail.com", "password": "test"},
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

    def test_create_habit(self):
        """ Тест создания привычки """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "reward": "Попить витаминный смузи",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }

        create_habit = reverse('habits:habits_create')
        response = self.client.post(create_habit, data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())

    def test_get_share_habits(self):
        """ Тест получения информации об общедоступных привычках """
        user = User(
            email="test2@gmail.com",
            password="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        user.set_password("test")
        user.save()

        data = {
            "place": "На стадионе",
            "time": "16:00:00",
            "action": "Подтянуться 10 раз",
            "is_pleasant": False,
            "frequency": "MONDAY",
            "reward": "Выпить воды",
            "duration": 2,
            "is_public": True,
            "user": user.pk
        }

        data2 = {
            "place": "На улице",
            "time": "08:00:00",
            "action": "Утренняя зарядка",
            "is_pleasant": True,
            "frequency": "WEDNESDAY",
            "duration": 1,
            "is_public": False,
            "user": user.pk
        }

        self.client.post(reverse('habits:habits_create'), data)
        self.client.post(reverse('habits:habits_create'), data2)
        response = self.client.get(reverse('habits:public_habits_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_user_habits(self):
        """ Тест получения информации о привычках пользователя """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "reward": "Попить витаминный смузи",
            "duration": 2,
            "is_public": True,
            "user": self.user.pk
        }

        data2 = {
            "place": "На стадионе",
            "time": "16:00:00",
            "action": "Подтянуться 10 раз",
            "is_pleasant": False,
            "frequency": "MONDAY",
            "reward": "Выпить воды",
            "duration": 2,
            "is_public": True,
            "user": self.user.pk
        }

        self.client.post(reverse('habits:habits_create'), data)
        self.client.post(reverse('habits:habits_create'), data2)
        response = self.client.get(reverse('habits:habits_list'), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_full_information_habit(self):
        """ Тест получения полной информации о привычке пользователя """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "reward": "Попить витаминный смузи",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }

        self.client.post(reverse('habits:habits_create'), data)
        habit_pk = Habit.objects.first().pk

        response = self.client.get(reverse('habits:habits_detail', args=[habit_pk]), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        """ Тест обновления привычки пользователя """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "reward": "Попить витаминный смузи",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }
        new_data = {
            "place": "В спортзале",
            "time": "17:00:00",
            "action": "Подтянуться 10 раз",
            "is_pleasant": False,
            "frequency": "MONDAY",
            "reward": "Выпить воды",
            "duration": 2,
            "is_public": True,
            "user": self.user.pk
        }

        self.client.post(reverse('habits:habits_create'), data)
        habit_pk = Habit.objects.first().pk
        response = self.client.put(reverse('habits:habits_update', args=[habit_pk]), new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validate_duration_create_habit(self):
        """ Тест на создание привычки с продолжительностью более 2 минут """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "reward": "Попить витаминный смузи",
            "duration": 3,
            "is_public": True,
            "owner": self.user.pk
        }

        response = self.client.post(reverse('habits:habits_create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_pleasant_create_habit(self):
        """ Тест на создание приятной привычки с наградой """
        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": True,
            "frequency": "SUNDAY",
            "reward": "Попить витаминный смузи",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }

        response = self.client.post(reverse('habits:habits_create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_linked_create_habit(self):
        """ Тест на добавление связанной привычки с признаком is_pleasant = False """

        data_1 = Habit.objects.create(
            place="В парке",
            time="17:00:00",
            action="Пробежать 5 км",
            is_pleasant=False,
            frequency="SUNDAY",
            reward="Попить витаминный смузи",
            duration=1,
            is_public=True,
            user=self.user
        )

        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "linked_habit": data_1.pk,
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }

        response = self.client.post(reverse('habits:habits_create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_reward_and_linked_create_habit(self):
        """ Тест на создание привычки с наградой и связанной привычкой """
        data_1 = Habit.objects.create(
            place="В парке",
            time="17:00:00",
            action="Пробежать 5 км",
            is_pleasant=True,
            frequency="SUNDAY",
            reward="Попить витаминный смузи",
            duration=1,
            is_public=True,
            user=self.user
        )

        data = {
            "place": "В спортзале",
            "time": "14:00:00",
            "action": "Пробежать 5 км",
            "is_pleasant": False,
            "frequency": "SUNDAY",
            "linked_habit": data_1.pk,
            "reward": "Попить витаминный смузи",
            "duration": 1,
            "is_public": True,
            "user": self.user.pk
        }

        response = self.client.post(reverse('habits:habits_create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
