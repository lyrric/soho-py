from django.urls import path

from . import views

urlpatterns = [
    path("tasks/getList", views.get_tasks, name="get_tasks"),
    path("tasks/create", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/update", views.update_task, name="update_task"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="delete_task"),

]
