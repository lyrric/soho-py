from django import forms
from django.db import models


# Create your models here.

class TaskForm(forms.Form):
    pass
    # def __init__(self, task_id, token_id, product_id, start_time):
    #     super().__init__()
    #     self.task_id = task_id
    #     self.token_id = token_id
    #     self.product_id = product_id
    #     self.start_time = start_time


class Task:
    def __init__(self, task_id, token_id, product_id, start_time):
        self.task_id = task_id
        self.token_id = token_id
        self.product_id = product_id
        self.start_time = start_time

    @classmethod
    def from_dict(cls, _dict):
        return Task(_dict.get('task_id'), _dict["token_id"], _dict["product_id"], _dict["start_time"])

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "token_id": self.token_id,
            "product_id": self.product_id,
            "start_time": self.start_time
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
