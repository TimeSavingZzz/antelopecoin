import string
from random import random

from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """ 用户表 """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    coin_account = models.DecimalField(verbose_name="羚羊币余额", max_digits=10, decimal_places=2, default=0)
    Opportunity = models.IntegerField(verbose_name="用户现在拥有的挖矿次数", default=100)
    status = models.IntegerField(verbose_name="用户现在的挖矿次数，0表示从头开始，不为0表示接着挖", default=0)
    pow1 = models.CharField(max_length=64, verbose_name="挖矿历史的第一个参数")
    role = models.CharField(max_length=16, default="1")

    @classmethod
    def create(cls):
        username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        return cls(username=username, password=password)


class MiningRecord(models.Model):
    """所有挖矿的记录表"""
    create_time = models.DateTimeField(verbose_name="挖矿创建时间")
    user = models.ForeignKey(to="UserInfo", to_field="id", blank=True, null=True, on_delete=models.SET_NULL)
    hash = models.CharField(max_length=64, verbose_name="本次挖矿的哈希值")
    Frequency = models.IntegerField(verbose_name="本次挖矿成功所使用的次数")


# class MiningUser(models.Model):
#     """用于记录当前每个用户的挖矿状态"""
#     user = models.ForeignKey(to="UserInfo", to_field="id", blank=True, null=True, on_delete=models.SET_NULL)
#     status = models.IntegerField(verbose_name="用户现在的挖矿次数，0表示从头开始，不为0表示接着挖", default=0)
#     create_time = models.DateTimeField(verbose_name="挖矿创建时间")


class Activity(models.Model):
    """管理员发布过的记录"""
    begin_time = models.DateTimeField(verbose_name="活动开始时间")
    end_time = models.DateTimeField(verbose_name="活动结束时间")
    stock = models.IntegerField(verbose_name="本次活动剩余的币")
    in_progress = models.IntegerField(verbose_name="活动是否在进行")
