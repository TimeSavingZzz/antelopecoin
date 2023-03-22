import math

import pandas as pd
import datetime
from views.Daily_Payable_Calculation import calculation

# activeteachers_recent = 2000
# today_add = 0
#
# begin1 = "2023-3-16"
# begin1 = datetime.datetime.strptime(begin1, '%Y-%m-%d') - pd.Timedelta(days=1)
# begin1 = begin1.strftime('%Y-%m-%d')
# #print(begin1)
# daliypayable_cal = calculation(begin1, 60, 30000)
#
#
#
#
# # 从 Excel 文件中读入 今日数据
# df = pd.read_excel('C:/Users/dj/Desktop//today.xlsx')
# today = dict(zip(df['id'], df['contribution']))
# activeteachers_today = len(today)
# total = sum(today.values())
#
#
# #
# # now_time = datetime.datetime.now()
# # now_time = now_time.strftime("%Y-%m-%d")
# now_time = "2023-04-28"
# amount_shouldBeSent = today_add + daliypayable_cal[now_time]
#
# if activeteachers_recent > activeteachers_today:
#     amount_actualSent = (activeteachers_today / activeteachers_recent) * amount_shouldBeSent
#     today_add = amount_shouldBeSent - amount_actualSent
# else:
#     amount_actualSent = amount_shouldBeSent
#     today_add = 0
#
# sent_today = {}
# mining_actualSent = amount_actualSent * 16
# for id, personal in today.items():
#     mining_Sent = math.floor(mining_actualSent * (personal / total))
#     if mining_Sent == 0: mining_Sent += 1
#     sent_today[id] = mining_Sent
#
# df = pd.DataFrame(list(sent_today.items()), columns=['id', 'sent'])
# df.to_excel('C:/Users/dj/Desktop//sent_today.xlsx', index=False)