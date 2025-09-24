import json
import os

import aiohttp

from soho import logging_config

log = logging_config.get_logger(__name__)

spt = None

if not os.environ.get('SPT'):
    log.warn("未配置SPT，不发送消息")
else:
    spt = os.environ.get('SPT')
    log.info(f"获取到SPT {spt}")


async def send_message(summary, content):
    if spt is None:
        log.warn("未配置SPT，不发送消息")
        return
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
