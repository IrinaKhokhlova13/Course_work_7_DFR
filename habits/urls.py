from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListApiView, HabitRetrieveApiView, HabitCreateApiView, HabitUpdateApiView, \
    HabitDestroyApiView, PublicHabitListApiView, OwnerHabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', HabitListApiView.as_view(), name='habits_list'),
    path('habits/create/', HabitCreateApiView.as_view(), name='habits_create'),
    path('habits/<int:pk>/', HabitRetrieveApiView.as_view(), name='habits_detail'),
    path('habits/update/<int:pk>/', HabitUpdateApiView.as_view(), name='habits_update'),
    path('habits/delete/<int:pk>/', HabitDestroyApiView.as_view(), name='habits_delete'),
    path('habit/list/owner/', OwnerHabitListAPIView.as_view(), name='owner_habits-list'),
    path('public_habits/', PublicHabitListApiView.as_view(), name='public_habits_list'),
]
