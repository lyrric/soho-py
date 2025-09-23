from typing import List

from django import forms


# Create your models here.


class Task:
    def __init__(self, task_id, token_id, product_id, product_name, free_card_num, start_time, status=0):
        self.task_id = task_id
        self.token_id = token_id
        self.product_name = product_name
        self.free_card_num = free_card_num
        self.product_id = product_id
        self.start_time = start_time
        # 状态 -1:已取消 0:初始状态 1：成功 2：失败
        self.status = 0

    def __str__(self):
        return "task_id: {}, token_id: {}, product_id: {},  product_name: {},free_card_num: {}, start_time: {}, status: {}".format(
            self.task_id,
            self.token_id,
            self.product_id,
            self.product_name,
            self.free_card_num,
            self.start_time,
            self.status)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "token_id": self.token_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "free_card_num": self.free_card_num,
            "start_time": self.start_time,
            "status": self.status,
        }


class HttpResult:
    def __init__(self, code, msg, data):
        self.code = code
        self.data = data
        self.msg = msg

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }

    @classmethod
    def ok(cls, data=None):
        return cls(200, "ok", data)

    @classmethod
    def error(cls, msg):
        return cls(500, msg, None)

    def __str__(self):
        return f"HttpResult(code={self.code}, msg={self.msg}, data={self.data})"


# 免费活动
class FreeActivity:
    """
    product_id: 产品id
    product_price：价格
    shop_type:平台类型 B:天猫，C：淘宝 3：京东 d:抖音
    title: 标题
    pic： 图片地址
    free_card_num： 免单卡数量
    sale_time: 如17:00
    more：更多，结构与自身一致
    """

    def __init__(self, product_id, product_price, shop_type, title, pic, free_card_num, sale_time,
                 more: List['FreeActivity'] = None):
        self.product_id = product_id
        self.product_price = product_price
        self.shop_type = shop_type
        self.title = title
        self.pic = pic
        self.free_card_num = free_card_num
        self.sale_time = sale_time
        self.more = more

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_price": self.product_price,
            "shop_type": self.shop_type,
            "title": self.title,
            "pic": self.pic,
            "free_card_num": self.free_card_num,
            "sale_time": self.sale_time,
            "more": [activity.to_dict() for activity in (self.more or [])]
        }

    def __str__(self):
        return (f"FreeActivity(product_id={self.product_id}, product_price={self.product_price}, "
                f"shop_type={self.shop_type}, title={self.title}, pic={self.pic}, "
                f"free_card_num={self.free_card_num}, sale_time={self.sale_time}, more={self.more})")
