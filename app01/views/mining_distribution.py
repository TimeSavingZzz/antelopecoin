import math
import pandas as pd
import datetime

from django.conf import settings
from django.http import JsonResponse


def distribution(file, time, amount_shouldBeSent):
    active_teachers_recent = 2000
    today_add = 0

    begin1 = (datetime.datetime.strptime(time, '%Y-%m-%d') - pd.Timedelta(days=1)).strftime('%Y-%m-%d')

    # 从 Excel 文件中读入 今日数据
    df = pd.read_excel(file)
    if "id" not in df.columns or "contribution" not in df.columns:
        return None
    today = dict(zip(df['id'], df['contribution']))
    active_teachers_today = len(today)
    total = sum(today.values())
    amount_shouldBeSent += today_add

    # 发不满币的情况
    if active_teachers_recent > active_teachers_today:
        amount_actualSent = (active_teachers_today / active_teachers_recent) * amount_shouldBeSent
        today_add = amount_shouldBeSent - amount_actualSent
    else:
        amount_actualSent = amount_shouldBeSent
        today_add = 0

    sent_today = {}
    sum_distri = 0
    mining_actualSent = amount_actualSent * 16
    for id, personal in today.items():
        mining_Sent = round(mining_actualSent * (personal / total))
        if mining_Sent == 0: mining_Sent += 1
        sent_today[id] = mining_Sent
        sum_distri += mining_Sent

    df = pd.DataFrame(list(sent_today.items()), columns=['id', 'sent'])
    df.to_excel(f'{settings.STATIC_ROOT}sent_{time}.xlsx', index=False)
    # 将 DataFrame 转换为 JSON
    data = df.to_json(orient='records')

    return data, sum_distri

