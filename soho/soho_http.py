import aiohttp

ukey = '85be376d0670f10bb8a77916bf774e53'

BASE_URL = "https://sapph5api.leqilucky.com/Sale/Task/SoHo"

from . import logging_config

log = logging_config.get_logger(__name__)


async def send_post(token_id, product_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL,
                                params={
                                    'uname': 'h5',
                                    'isFreeCard': 'true',
                                    'isFirst': 'true',
                                    'IsCfmdLimitArea': 'false',
                                    'isFreeCardLimitRemind': 'false',
                                    'ukey': ukey,
                                    'tokenid': token_id,
                                    'productID': product_id,
                                },
                                headers=_get_headers(),
                                timeout=aiohttp.ClientTimeout(total=30),
                                ssl=False) as response:
            if response.ok:
                result = await response.json()
                err_msg = result['ErrMsg']
                if not err_msg:
                    return True
                else:
                    log.warn(f"抢购失败 {err_msg}")
                    return False
            else:
                log.warn(f"抢购失败 {response.reason}")
                return False


def _get_headers():
    return {
        'Host': 'sapph5api.leqilucky.com',
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://sapph5.lqlucky.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307062c)",
        'Content-Type': "application/x-www-form-urlencoded",
    }
