import asyncio
import datetime
from threading import Thread

from . import logging_config
from typing import List

from soho.models import Task
from soho.soho_http import send_post
from soho.message import send_message
from .my_service import SingleThreadCoroutineRunner

log = logging_config.get_logger(__name__)

tasks: List[Task] = []

# 额外的线程
__thread = SingleThreadCoroutineRunner()


async def _do_task(task: Task):
    log.info(f"准备执行任务, task_id:{task.task_id}")
    start_time = _get_start_time(task)
    now = datetime.datetime.now()
    if now < start_time:
        sleep_time = start_time - now
        log.info(f"task_id:{task.task_id} 任务未开始，等待{sleep_time.seconds}秒")
        await asyncio.sleep(sleep_time.seconds)
    log.info(f"开始执行任务：{task}")
    end_time = _get_end_time(task)

    while datetime.datetime.now() < end_time:
        result = await send_post(task.token_id, task.product_id)
        if result:
            return True
    return False


def _get_end_time(task: Task):
    now = datetime.datetime.now()
    # 将小时设置为指定值，分钟、秒、毫秒设为0
    return now.replace(hour=int(task.start_time), minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=2)


def _get_start_time(task: Task):
    end_time = _get_end_time(task)
    # 减去5秒钟
    return end_time - datetime.timedelta(seconds=5)


def start_task(task: Task):
    __thread.submit_coroutine(_start_task, task)


async def _start_task(task: Task):
    result = await _do_task(task)
    log.info(f"task_id:  {task.product_name} 任务执行{'成功' if result else '失败'}")
    task.status = 1 if result else 2
    log.info(f" {task.product_name} 开始发送消息")
    await send_post(task.token_id, task.product_id)
    await send_message(f' {task.product_name} 抢购成功', f'{task.product_name} 抢购成功')
