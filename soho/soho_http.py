from typing import List

import aiohttp

ukey = '85be376d0670f10bb8a77916bf774e53'

BASE_URL = "https://sapph5api.leqilucky.com/Sale/Task/SoHo"

from . import logging_config
from .models import FreeActivity
from .models import UserInfo

log = logging_config.get_logger(__name__)


# 抢购
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


# 获取免费活动列表
async def get_list(token_id, drop_down, remain_node):
    """

    :param token_id: token_id
    :param drop_down:  是否翻页，第二页传true
    :param remain_node:  时间 格式为19:00
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.post("https://sapph5api.leqilucky.com/Sale/Sale/ZeroYuanFutureNodeBuyingPage",
                                params={
                                    'uname': 'h5',
                                    'ukey': ukey,
                                    'tokenid': token_id,
                                    'DropDown': str(drop_down),
                                    'RemindNode': remain_node,
                                    'Gapday': "0",
                                    'IsNewPerson': str(False),
                                    'ShopType': '',
                                    'SAPPHomeSortType': '0',
                                },
                                headers=_get_headers(),
                                timeout=aiohttp.ClientTimeout(total=30),
                                ssl=False) as response:
            if response.ok:
                result = await response.json()
                err_msg = result['ErrMsg']
                if not err_msg:
                    return _parse_list(result['DataList'], remain_node)
                else:
                    log.warn(f"获取失败 {err_msg}")
                    raise Exception(f"获取失败 {err_msg}")
            else:
                log.warn(f"获取失败 {response.reason}")
                raise Exception(f"获取失败 {response.reason}")


async def get_user_info(token_id):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://sapph5api.leqilucky.com/Member/SApp/SaleMiniAppMyInfoGet",
                               params={
                                   'uname': 'h5',
                                   'ukey': ukey,
                                   'tokenid': token_id,
                               },
                               headers=_get_headers(),
                               timeout=aiohttp.ClientTimeout(total=30),
                               ssl=False) as response:
            result = await _check_result(response)
            info_dict = result['SaleMiniAppMyInfo']
            return UserInfo.from_dict(info_dict)


async def _check_result(response):
    if response.ok:
        result = await response.json()
        err_msg = result.get('ErrMsg')
        if err_msg:
            log.warn(f"获取失败 {err_msg}")
            raise Exception(f"获取失败 {err_msg}")
        return result
    else:
        log.warn(f"获取失败 {response.reason}")
        raise Exception(f"获取失败 {response.reason}")


def _parse_list(data_list, remain_node) -> List[FreeActivity]:
    result: List[FreeActivity] = []
    for data in data_list:
        item = FreeActivity(data['ProductID'], data['ProductPrice'], data['ShopType'],
                            data['TitleShort'], data['ShowPicUrl'], data['FreeCardNum'], remain_node)
        result.append(item)
    return result


def _get_headers():
    return {
        'Host': 'sapph5api.leqilucky.com',
        'Accept': "application/json, text/plain, */*",
        'Origin': "https://sapph5.lqlucky.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307062c)",
        'Content-Type': "application/x-www-form-urlencoded",
    }
