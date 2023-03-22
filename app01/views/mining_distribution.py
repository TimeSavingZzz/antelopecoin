import math
import pandas as pd
import datetime


def distribution(file, time):
    active_teachers_recent = 2000
    today_add = 0

    begin1 = (datetime.datetime.strptime(time, '%Y-%m-%d') - pd.Timedelta(days=1)).strftime('%Y-%m-%d')

    # 读入活动数据
    activity = pd.read_excel('E:/Step1/djangoProject/app01/static/xlsx/activity.xlsx')
    amount_shouldBeSent = today_add + dict(zip(activity['time'], activity['coin']))[time]

    # 从 Excel 文件中读入 今日数据
    df = pd.read_excel(file)
    today = dict(zip(df['id'], df['contribution']))
    active_teachers_today = len(today)
    total = sum(today.values())

    if active_teachers_recent > active_teachers_today:
        amount_actualSent = (active_teachers_today / active_teachers_recent) * amount_shouldBeSent
        today_add = amount_shouldBeSent - amount_actualSent
    else:
        amount_actualSent = amount_shouldBeSent
        today_add = 0

    sent_today = {}
    mining_actualSent = amount_actualSent * 16
    for id, personal in today.items():
        mining_Sent = math.floor(mining_actualSent * (personal / total))
        if mining_Sent == 0: mining_Sent += 1
        sent_today[id] = mining_Sent

    df = pd.DataFrame(list(sent_today.items()), columns=['id', 'sent'])
    df.to_excel('C:/Users/dj/Desktop//sent_today.xlsx', index=False)