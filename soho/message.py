import json

import aiohttp

from soho import logging_config

log = logging_config.get_logger(__name__)


async def send_message(spt, content, summary):
    """
    异步发送消息

    :param spt: 接收者标识
    :param content: 消息内容
    :param summary: 消息摘要
    """
    body_map = {
        "content": content,
        "summary": summary,
        "contentType": 2,
        "spt": spt
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://wxpusher.zjiecode.com/api/send/message/simple-push",
                    json=body_map,
                    timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                res_body = await response.text()
                result = json.loads(res_body)
                if result.get("code") != 1000:
                    log.error(f"发送消息失败: {res_body}")
    except Exception as e:
        log.error(f"发送消息失败: {e}")
