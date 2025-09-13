from django import forms


# Create your models here.


class Task:
    def __init__(self, task_id, token_id, product_id, start_time, status=0):
        self.task_id = task_id
        self.token_id = token_id
        self.product_id = product_id
        self.start_time = start_time
        # 状态 -1:已取消 0:初始状态 1：成功 2：失败
        self.status = 0

    def __str__(self):
        return "task_id: {}, token_id: {}, product_id: {}, start_time: {}, status: {}".format(self.task_id,
                                                                                              self.token_id,
                                                                                              self.product_id,
                                                                                              self.start_time,
                                                                                              self.status)

    @classmethod
    def from_dict(cls, _dict):
        return Task(_dict.get('task_id'), _dict["token_id"], _dict["product_id"], _dict["start_time"])

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "token_id": self.token_id,
            "product_id": self.product_id,
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
