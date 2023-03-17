from django.db import models

# Create your models here.
class User_Info(models.Model):
    """ 用户表 """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    coin_account = models.DecimalField(verbose_name="羚羊币余额", max_digits=10, decimal_places=2, default=0)
    role = models.CharField(max_length=16)

class Mining(models.Model):
    """挖矿"""
    create_time = models.DateTimeField(verbose_name="挖矿创建时间")
    user = models.ForeignKey(to="User_Info", to_field="id", blank=True, null=True, on_delete=models.SET_NULL)
    flag = models.BooleanField(verbose_name="是否执行过", default=False)
    salary = models.DecimalField(verbose_name="本次挖矿收益", max_digits=10, decimal_places=2, default=0)