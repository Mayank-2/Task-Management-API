from django.urls import path
from .views import Tasks, GetTask,FilterTask,SortTask,SearchTask

urlpatterns = [
    path('task/',Tasks.as_view(), name='task'),
    path('task/delete/<uuid:id>',Tasks.as_view(), name='task'),
    path('task/<uuid:id>', GetTask.as_view(), name='get_task'),
    path('task/filter/<str:filter>/<str:query>',FilterTask.as_view(),name="taskFilter"),
    path('task/sort/<str:filter>',SortTask.as_view(),name="taskSort"),
    path('task/search/<str:query>',SearchTask.as_view(),name="taskSort"),

]

