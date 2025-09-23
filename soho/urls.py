from django.urls import path

from . import views

urlpatterns = [
    path("tasks/getList", views.get_tasks, name="get_tasks"),
    path("tasks/<int:task_id>/update", views.update_task, name="update_task"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="delete_task"),
    path("activity/get_all", views.get_free_activity_list, name="get_free_activity_list"),
    path("activity/create_reserve", views.create_reserve, name="create_reserve"),
    path("set_token_id", views.set_token_id, name="set_token_id"),

]
