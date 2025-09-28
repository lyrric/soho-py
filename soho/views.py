import asyncio
import concurrent.futures
import datetime
import json
import threading
from typing import Optional, List

import redis
from django.core.cache import cache
from django.http import JsonResponse

from soho.models import HttpResult, FreeActivity
from soho.models import Task
from soho import my_task
from soho import soho_http
from soho import logging_config
from soho import message
from soho.my_service import SingleThreadCoroutineRunner
from django_redis import get_redis_connection

new_task_id = 1
log = logging_config.get_logger(__name__)

# 额外的线程
thread = SingleThreadCoroutineRunner()

IGNORE_SIMILAR_PRODUCT = "IGNORE_SIMILAR_PRODUCT"


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
    # 生成缓存键
    cache_key = f"FREE_ACTIVITY_LIST"

    # 尝试从缓存中获取结果
    result = cache.get(cache_key)
    if result is None:
        token_id = _get_token_id()
        if token_id is None:
            return JsonResponse(HttpResult.error("请先设置token_id").to_dict())

        hour = datetime.datetime.now().hour
        result: List[FreeActivity] = []
        try:
            for hour in range(hour + 1, 24):
                datas = await soho_http.get_list(token_id, False, f"{hour}:00")
                while len(datas) != 0:
                    result.extend(datas)
                    datas = await soho_http.get_list(token_id, True, f"{hour}:00")
        except Exception as e:
            log.error("get_free_activity_list error", exc_info=True)
            return JsonResponse(HttpResult.error(str(e)).to_dict())
        # 将结果缓存30分钟（1800秒）
        cache.set(cache_key, result, 1800)
    else:
        log.info("从缓存中获取结果")

    result = _filter_result(result)
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
    response_data = HttpResult.ok(activity_dict).to_dict()

    return JsonResponse(response_data, safe=False)


# 过滤返回结果
def _filter_result(result: List[FreeActivity]) -> List[FreeActivity]:
    con = get_redis_connection()
    return [activity for activity in result if not _contain(con, activity)]


def _contain(con, activity: FreeActivity) -> bool:
    result = con.lpos(IGNORE_SIMILAR_PRODUCT,
                      activity.title + '-' + activity.shop_type + '-' + str(activity.product_price))
    return True if result is not None else False


def _get_token_id():
    conn = get_redis_connection()
    token_id = conn.get("TOKEN_ID")
    return token_id.decode(encoding="utf-8")


def _set_token_id(token_id: str):
    conn = get_redis_connection()
    conn.set("TOKEN_ID", str(token_id))


def create_reserve(request):
    if request.method == 'POST':
        json_task = json.loads(request.body)
        global new_task_id
        token_id = _get_token_id()
        task = Task(new_task_id, token_id, json_task['product_id'], json_task['product_name'],
                    json_task['free_card_num'], json_task['sale_time'].replace(':00', ''))
        new_task_id += 1
        my_task.tasks.append(task)
        my_task.start_task(task)
    return JsonResponse(HttpResult.ok().to_dict())


def set_token_id(request):
    body = json.loads(request.body)
    token_id = body['token_id']
    _set_token_id(token_id)
    thread.submit_coroutine(_check_token_id_scheduled, token_id)
    return JsonResponse(HttpResult.ok().to_dict())


# 忽略相似产品
def ignore_similar_product(request):
    req_body = json.loads(request.body)
    title = req_body['title']
    shop_type = req_body['shop_type']
    product_price = req_body['product_price']
    con = get_redis_connection()
    con.lpush(IGNORE_SIMILAR_PRODUCT, title + '-' + shop_type + '-' + str(product_price))
    return JsonResponse(HttpResult.ok().to_dict())


async def _check_token_id_scheduled(_token_id):
    if _token_id is None:
        return

    while True:
        # 检查当前时间是否在0点到早上8点之间
        current_hour = datetime.datetime.now().hour
        if 0 <= current_hour < 8:
            log.info(f"当前时间为{current_hour}点，处于0点到8点之间，停止检查token_id:{_token_id}")
            return

        try:
            token_id = _get_token_id()
            if _token_id != token_id:
                log.info(f"token_id已改变, 停止检查:{_token_id}")
                return
            await soho_http.get_user_info(_token_id)
            await asyncio.sleep(60 * 5)
        except Exception as e:
            log.error(f"检查token_id失败:{e}", exc_info=True)
            await message.send_message("检查token_id失败", f'token_id :{_token_id} error: {e}')
            return
