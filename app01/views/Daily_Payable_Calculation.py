import math
from app01 import models
from scipy.stats import norm
import pandas as pd
from workalendar.asia import China

# 通过活动开始时间，活动总时间，活动总发币计算每天发多少，返回一个字典
def calculation(begintime, totaltime, salary):

    totaltime = int(totaltime)
    salary = int(salary)

    # 此处取高斯分布的95%的置信区间
    count = salary / 0.68

    # 设置本次活动的参数，mu，sigma都是通过活动时间计算而来，因为置信度95%所以sigma值取totaltime / 4
    mu, sigma = totaltime / 2, totaltime / 2

    # 设置活动开始时间, begintime是字符串类型
    begindate = pd.Timestamp(begintime)
    nextday = begindate

    # 计算实际的发币总和
    sum1 = 0
    strday = ""
    # 创建中国日历对象
    cal = China()

    day_salary = {}

    # 计算60个工作日内对应日期的发放数量
    for i in range(0, 60):
        # 计算第i天应该发放的币数
        interval = [i, i + 1]
        z1 = (interval[0] - mu) / sigma
        z2 = (interval[1] - mu) / sigma
        p = norm.cdf(z2) - norm.cdf(z1)
        c1 = math.floor(p * count)
        # 判断是否是工作日，只有工作日才发币
        nextday = nextday + pd.Timedelta(days=1)
        # is_working_day = cal.is_working_day(nextday)
        # while not is_working_day:
        #     nextday = nextday + pd.Timedelta(days=1)
        #     is_working_day = cal.is_working_day(nextday)
        strday = nextday.strftime("%Y-%m-%d")
        day_salary[strday] = c1

        sum1 += c1
    models.Activity.objects.create(begin_time=begindate, end_time=strday, stock= salary, in_progress=1)

    # 将字典转换为 DataFrame
    df = pd.DataFrame(list(day_salary.items()), columns=['time', 'coin'])

    # 导出 DataFrame 为 Excel 文件
    df.to_excel('E:/Step1/djangoProject/djangoProject/activity.xlsx', index=False)

    return day_salary
    print(sum1)