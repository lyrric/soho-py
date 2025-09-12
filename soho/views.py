import json
from typing import List, Optional

# Create your views here.
from django.http import JsonResponse

from .models import HttpResult
from .models import Task

tasks: List[Task] = []
new_task_id = 1


def create_task(request):
    if request.method == 'POST':
        task = Task.from_dict(json.loads(request.body))
        global new_task_id, tasks
        task.task_id = new_task_id
        new_task_id += 1
        tasks.append(task)

    return JsonResponse(HttpResult.ok().to_dict())


def update_task(request, task_id):
    global tasks
    if request.method != 'POST':
        return JsonResponse(HttpResult.error("Method not allowed").to_dict())

    task = find_task_by_id(task_id)
    if task is None:
        return JsonResponse(HttpResult.error("Task not found").to_dict())

    task_dict = json.loads(request.body)
    # 更新任务属性
    task.token_id = task_dict['token_id']
    task.product_id = task_dict['product_id']
    task.start_time = task_dict['start_time']
    return JsonResponse(HttpResult.ok().to_dict())


def delete_task(request, task_id):
    """
       删除指定ID的任务
       """
    global tasks
    task_index = find_task_index_by_id(task_id)
    if task_index is not None:
        tasks.pop(task_index)
    return JsonResponse(HttpResult.ok().to_dict())


def find_task_by_id(task_id) -> Optional[Task]:
    """根据ID查找任务"""
    for task in tasks:
        if task.task_id == task_id:
            return task
    return None


def find_task_index_by_id(task_id) -> Optional[int]:
    """根据ID查找任务索引"""
    for i, task in enumerate(tasks):
        if task.task_id == task_id:
            return i
    return None


def get_tasks(request):
    tasks_data = [task.to_dict() for task in tasks]
    return JsonResponse(HttpResult.ok(tasks_data).to_dict(), content_type="application/json", safe=False)
