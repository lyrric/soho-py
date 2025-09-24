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


class UserInfo:
    def __init__(self, nick=None, head_portrait_url=None, is_partner_open=None, amount=None, 
                 sale_amount_back=None, wait_finish_count=None, wait_receive_count=None, 
                 wait_evaluate_count=None, user_level=None, is_get_week_welfare=None, 
                 is_off_week_recommend_rank=None, week_recommend_rank_no1=None, get_qty_no_used=None, 
                 wait_get_qty=None, is_ta_limit=None, limit_day_number=None, ta_limit_remove_date=None, 
                 is_buy_limit=None, buy_limit_day_number=None, buy_limit_remove_date=None, 
                 rebate_price_total=None, need_buy_count=None, need_friend_count=None, 
                 wait_done_record_count=None, un_read_count=None, wait_evaluate_order_count=None):
        self.nick = nick
        self.head_portrait_url = head_portrait_url
        self.is_partner_open = is_partner_open
        self.amount = amount
        self.sale_amount_back = sale_amount_back
        self.wait_finish_count = wait_finish_count
        self.wait_receive_count = wait_receive_count
        self.wait_evaluate_count = wait_evaluate_count
        self.user_level = user_level
        self.is_get_week_welfare = is_get_week_welfare
        self.is_off_week_recommend_rank = is_off_week_recommend_rank
        self.week_recommend_rank_no1 = week_recommend_rank_no1
        self.get_qty_no_used = get_qty_no_used
        self.wait_get_qty = wait_get_qty
        self.is_ta_limit = is_ta_limit
        self.limit_day_number = limit_day_number
        self.ta_limit_remove_date = ta_limit_remove_date
        self.is_buy_limit = is_buy_limit
        self.buy_limit_day_number = buy_limit_day_number
        self.buy_limit_remove_date = buy_limit_remove_date
        self.rebate_price_total = rebate_price_total
        self.need_buy_count = need_buy_count
        self.need_friend_count = need_friend_count
        self.wait_done_record_count = wait_done_record_count
        self.un_read_count = un_read_count
        self.wait_evaluate_order_count = wait_evaluate_order_count

    def to_dict(self):
        return {
            "nick": self.nick,
            "head_portrait_url": self.head_portrait_url,
            "is_partner_open": self.is_partner_open,
            "amount": self.amount,
            "sale_amount_back": self.sale_amount_back,
            "wait_finish_count": self.wait_finish_count,
            "wait_receive_count": self.wait_receive_count,
            "wait_evaluate_count": self.wait_evaluate_count,
            "user_level": self.user_level,
            "is_get_week_welfare": self.is_get_week_welfare,
            "is_off_week_recommend_rank": self.is_off_week_recommend_rank,
            "week_recommend_rank_no1": self.week_recommend_rank_no1,
            "get_qty_no_used": self.get_qty_no_used,
            "wait_get_qty": self.wait_get_qty,
            "is_ta_limit": self.is_ta_limit,
            "limit_day_number": self.limit_day_number,
            "ta_limit_remove_date": self.ta_limit_remove_date,
            "is_buy_limit": self.is_buy_limit,
            "buy_limit_day_number": self.buy_limit_day_number,
            "buy_limit_remove_date": self.buy_limit_remove_date,
            "rebate_price_total": self.rebate_price_total,
            "need_buy_count": self.need_buy_count,
            "need_friend_count": self.need_friend_count,
            "wait_done_record_count": self.wait_done_record_count,
            "un_read_count": self.un_read_count,
            "wait_evaluate_order_count": self.wait_evaluate_order_count
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nick=data.get("Nick"),
            head_portrait_url=data.get("HeadPortraitUrl"),
            is_partner_open=data.get("IsPartnerOpen"),
            amount=data.get("Amount"),
            sale_amount_back=data.get("SaleAmountBack"),
            wait_finish_count=data.get("WaitFinishCount"),
            wait_receive_count=data.get("WaitReceiveCount"),
            wait_evaluate_count=data.get("WaitEvaluateCount"),
            user_level=data.get("UserLevel"),
            is_get_week_welfare=data.get("IsGetWeekWelfare"),
            is_off_week_recommend_rank=data.get("IsOffWeekRecommendRank"),
            week_recommend_rank_no1=data.get("WeekRecommendRankNo1"),
            get_qty_no_used=data.get("GetQtyNoUsed"),
            wait_get_qty=data.get("WaitGetQty"),
            is_ta_limit=data.get("IsTALimit"),
            limit_day_number=data.get("LimitDayNumber"),
            ta_limit_remove_date=data.get("TALimitRemoveDate"),
            is_buy_limit=data.get("IsBuyLimit"),
            buy_limit_day_number=data.get("BuyLimitDayNumber"),
            buy_limit_remove_date=data.get("BuyLimitRemoveDate"),
            rebate_price_total=data.get("RebatePriceTotal"),
            need_buy_count=data.get("NeedBuyCount"),
            need_friend_count=data.get("NeedFriendCount"),
            wait_done_record_count=data.get("WaitDoneRecordCount"),
            un_read_count=data.get("UnReadCount"),
            wait_evaluate_order_count=data.get("WaitEvaluateOrderCount")
        )

    def __str__(self):
        return f"UserInfo(nick={self.nick}, amount={self.amount}, user_level={self.user_level})"
