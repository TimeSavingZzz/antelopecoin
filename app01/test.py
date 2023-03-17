"""日期字典"""
# import pandas as pd
#
# # 生成日期范围
# dates = pd.date_range(start='2023-01-01', periods=60)
#
# # 创建字典，将所有值都设置为 1
# salary = {date: 1 for date in dates}
# salary.p
# print(salary)

"""随机生成用户贡献度"""
import random
import pandas as pd

# # 生成随机的 key 和 value
# keys = random.sample(range(1, 3001), 1500)
# values = [round(random.uniform(0.5, 10), 1) for _ in range(1500)]
#
# # 将 key 和 value 组合成字典
# today = dict(zip(keys, values))
#
"""字典转excel"""
# # 将字典转换为 DataFrame
# df = pd.DataFrame(list(today.items()), columns=['key', 'value'])
#
# # 导出 DataFrame 为 Excel 文件
# df.to_excel('C:/Users/dj/Desktop//today.xlsx', index=False)

# 从 Excel 文件中读入 DataFrame
# df = pd.read_excel('C:/Users/dj/Desktop//today.xlsx')
#
# # 将 DataFrame 转换为字典
# today = dict(zip(df['id'], df['contribution']))
# print(today)

"""字符串转日期"""
# import datetime
#
# date_str = '2023-03-16'
# date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
