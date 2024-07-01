from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitListApiView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitCreateApiView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class HabitRetrieveApiView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]


class HabitUpdateApiView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyApiView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PublicHabitListApiView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination
