import datetime
import json
from typing import Optional, List

# Create your views here.
from django.http import JsonResponse

from soho.models import HttpResult, FreeActivity
from soho.models import Task
from soho import my_task
from soho import soho_http

new_task_id = 1

token_id = None


def create_task(request):
    if request.method == 'POST':
        task = Task.from_dict(json.loads(request.body))
        global new_task_id
        task.task_id = new_task_id
        new_task_id += 1
        my_task.tasks.append(task)
        my_task.start_task(task)
    return JsonResponse(HttpResult.ok().to_dict())


def update_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse(HttpResult.error("Method not allowed").to_dict())

    task = find_task_by_id(task_id)
    if task is None:
        return JsonResponse(HttpResult.error("Task not found").to_dict())

    task_dict = json.loads(request.body)
    # 更新任务属性
    task.token_id = task_dict['token_id']
    task.product_id = task_dict['product_id']
    return JsonResponse(HttpResult.ok().to_dict())


def delete_task(request, task_id):
    """
       删除指定ID的任务
       """
    task_index = find_task_index_by_id(task_id)
    if task_index is not None:
        my_task.tasks.pop(task_index)
    return JsonResponse(HttpResult.ok().to_dict())


def find_task_by_id(task_id) -> Optional[Task]:
    """根据ID查找任务"""
    for task in my_task.tasks:
        if task.task_id == task_id:
            return task
    return None


def find_task_index_by_id(task_id) -> Optional[int]:
    """根据ID查找任务索引"""
    for i, task in enumerate(my_task.tasks):
        if task.task_id == task_id:
            return i
    return None


def get_tasks(request):
    tasks_data = [task.to_dict() for task in my_task.tasks]
    return JsonResponse(HttpResult.ok(tasks_data).to_dict(), content_type="application/json", safe=False)


# 获取今天所有活动
async def get_free_activity_list(request):
    if token_id is None:
        return JsonResponse(HttpResult.error("请先设置token_id").to_dict())
    current_time = datetime.datetime.now()
    result: List[FreeActivity] = []
    for hour in range(current_time.hour + 1, 24):
        datas = await soho_http.get_list(token_id, False, f"{hour}:00")
        while len(datas) != 0:
            result.extend(datas)
            datas = await soho_http.get_list(token_id, True, f"{hour}:00")

    # 根据title和product_price进行分组并处理more属性
    grouped_activities = {}
    for activity in result:
        key = (activity.title, activity.product_price)
        if key not in grouped_activities:
            grouped_activities[key] = []
        grouped_activities[key].append(activity)

    # 设置more属性并去重
    final_result = []
    processed = set()

    for activity in result:
        key = (activity.title, activity.product_price)
        activities = grouped_activities[key]

        # 如果有重复项，则设置more属性
        if len(activities) > 1:
            # 如果该组还未处理过
            if key not in processed:
                activity.more = [act for act in activities if act != activity]
                # 只添加第一个活动到结果中，避免重复
                final_result.append(activity)
                processed.add(key)
        else:
            # 没有重复项，直接添加
            final_result.append(activity)
    activity_dict = [activity.to_dict() for activity in final_result]
    return JsonResponse(HttpResult.ok(activity_dict).to_dict(), safe=False)


# 自定义JSON编码器，处理自定义对象
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # 如果是Item对象，转换为字典
        if isinstance(obj, FreeActivity):
            return obj.to_dict()
        if isinstance(obj, HttpResult):
            return obj.to_dict()
        # 其他类型使用默认处理
        return super().default(obj)


def create_reserve(request):
    if request.method == 'POST':
        json_task = json.loads(request.body)
        global new_task_id
        task = Task(new_task_id, token_id, json_task['product_id'], json_task['sale_time'].replace(':00', ''))
        new_task_id += 1
        my_task.tasks.append(task)
        my_task.start_task(task)
    return JsonResponse(HttpResult.ok().to_dict())


def set_token_id(request):
    global token_id
    body = json.loads(request.body)
    token_id = body['token_id']
    return JsonResponse(HttpResult.ok().to_dict())
