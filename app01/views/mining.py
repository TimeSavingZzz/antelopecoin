import random

from app01 import models
import datetime
from hashlib import sha256
from django.db.models import F
from app01.views.Daily_Payable_Calculation import calculation

# 通过userid判断用户之前是否有挖矿记录
# 成功的时候插入MiningRecord，有创建时间、hash值、id、Frequency


def instant_mining(userid, dig_time, status):
    user_info = models.UserInfo.objects.filter(id=userid).first()
    js_dict = {}
    success_count = 0
    pow2 = 1
    now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    pow1 = f'{userid}{now_time}{dig_time}'
    if status == 0:

        while dig_time > 0:
            sha = sha256(f'{pow1}{pow2}'.encode()).hexdigest()
            if sha[:1] == "0":
                success_count += 1
                js_dict[success_count] = sha
                now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                models.MiningRecord.objects.create(create_time=now_time, user_id=userid, Frequency=pow2, hash=sha)
                models.UserInfo.objects.filter(id=userid).update(coin_account=F('coin_account') + 1)
                pow1 = f'{userid}{now_time}{dig_time}'
                pow2 = 0
            pow2 += 1
            dig_time -= 1

    else:

        pow2 = int(status) + 1
        while dig_time > 0:
            sha = sha256(f'{pow1}{pow2}{dig_time}'.encode()).hexdigest()
            if sha[:1] == "0":
                success_count += 1
                js_dict[success_count] = sha
                # now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                models.MiningRecord.objects.create(create_time=now_time, user_id=userid, Frequency=pow2, hash=sha)
                models.UserInfo.objects.filter(id=userid).update(coin_account=F('coin_account') + 1)
                pow2 = 0
                pow1 = f'{userid}{now_time}{dig_time}'
            pow2 += 1
            dig_time -= 1

    if pow2 == 1:
        models.UserInfo.objects.filter(id=userid).update(status=0)
    else:
        models.UserInfo.objects.filter(id=userid).update(status=pow2 - 1, pow1=pow1)
    return js_dict

