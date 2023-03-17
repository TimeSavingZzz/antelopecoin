import math

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
from workalendar.asia import China

# 置信水平	分位数z值（双尾）	置信区间（双尾）	对应标准差范围
# 50%	0.674	(-0.674, 0.674)	1
# 60%	0.841	(-0.841, 0.841)	0.833
# 70%	1.036	(-1.036, 1.036)	0.524
# 75%	1.150	(-1.150, 1.150)	0.433
# 80%	1.282	(-1.282, 1.282)	0.375
# 85%	1.440	(-1.440, 1.440)	0.317
# 90%	1.645	(-1.645, 1.645)	0.253
# 95%	1.960	(-1.960, 1.960)	0.200
# 98%	2.326	(-2.326, 2.326)	0.127
# 99%	2.576	(-2.576, 2.576)	0.100
# 设置本次活动的参数，mu，sigma都是通过活动时间计算而来，此处例子为活动时间共60天
#mu, sigma = 30, 30
mu, sigma = 30,  30 / 1.282
# 总发放币数量
salary = 30000
# 此处取高斯分布的95%的置信区间
#count = salary / 0.68
count = salary / 0.8
# 设置活动开始时间,时间是
begindate = pd.Timestamp('2023-03-15')
nextday = begindate
#测试用，计算实际的发币总和
sum1 = 0

# 创建中国日历对象
cal = China()
day_salary = {}
#
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
    print(strday, day_salary[strday])
    sum1 += c1

print(sum1)
xlist = list(day_salary.keys())
plt.plot(xlist, day_salary.values(), label='count_payable')
plt.xlabel('day')
plt.ylabel('coin')
plt.xticks(xlist[::15])
plt.legend()
plt.show()







#print("{} 是休息日：{}".format(date.date(), is_holiday))

#print("{} 是工作日：{}".format(date.date(), is_working_day))



"""
# 生成一组随机数
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)

# 计算正态分布在 x 处的概率密度值
pdf = norm.pdf(x, mu, sigma)
# 绘制正态分布的概率密度函数图像

"""
#print("置信度为：{:.2%}".format(p))