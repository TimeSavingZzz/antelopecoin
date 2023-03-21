import random

from app01 import models
import datetime
from hashlib import sha256
from app01.views.Daily_Payable_Calculation import calculation


def instant_mining(userid, coin_account, flag):
    now_time = datetime.datetime.now()
    now_time = now_time.strftime("%Y-%m-%d-%H:%M:%S")

    active_user = 1000
    pow1 = models.Mining.objects.count() + 1
    pow2 = 0
    if flag == True:
        return
    if pow1 < 1000:
        while True:
            sha = sha256(f'{pow1 * pow2}'.encode()).hexdigest()
            if sha[:2] == "00":
                break
            pow2 += 1
    elif pow1 < 2000:
        while True:
            sha = sha256(f'{pow1 * pow2}'.encode()).hexdigest()
            if sha[:3] == "000":
                break
            pow2 += 1
    else:
        while True:
            sha = sha256(f'{pow1 * pow2}'.encode()).hexdigest()
            if sha[:4] == "0000":
                break
            pow2 += 1
    salary = 10000 / pow2

    if salary >= 30:
        salary -= random.randint(20, 30)
    elif salary <= 2:
        salary += random.randint(1, 5)
    print(salary)

    flag = True
    coin_account = float(coin_account)

    models.UserInfo.objects.filter(id=userid).update(coin_account= coin_account + salary)
    models.Mining.objects.create(create_time=now_time, flag=flag, user_id=userid, salary= salary)


def regular_mining():
    begin1 = "2023-3-16"
    begin1 = datetime.datetime.strptime(begin1, '%Y-%m-%d') - pd.Timedelta(days=1)
    begin1 = begin1.strftime('%Y-%m-%d')
    # print(begin1)
    daliypayable_cal = calculation(begin1, 60, 30000)

"""
已完成：
## 挖矿形式增加，增加工作难度系数
## 学生管理员不作为统计范围，统计近期活跃老师人数：增加了用户角色

两个前缀0时， 1-1000：261 1000-2001：262 两万次 252 100000次 253
平均253次挖到一个币 方差极大
1个前缀0， 10万次平均15 100万次平均 16 给予16个挖矿次数挖到一个币，并生成独特的hash值

## 考虑怎么控制总发币时间,

"""
## 考虑系统总人数，考虑活跃人数（近期）尽量活跃人数均摊。
## 锦标赛性质

## 补充交易记录，回收算法
## 部署

## 计算所有用户总时间的总工作量，然后根据总工作量计算单人当天的挖矿次数分配
## 把工作量转化为挖矿次数，然后再挖
#  统计花销