import pandas as pd
from django.db.models import F
from app01.models import UserInfo
import os

def update_opportunity_from_xlsx(file_path):
    # 读取xlsx文件并将其转换为字典列表
    df = pd.read_excel(file_path)
    data = df.to_dict(orient='records')

    # 获取所有用户的 ID
    user_ids = [d['id'] for d in data]

    # 从数据库中获取这些 ID 对应的用户
    users = UserInfo.objects.filter(id__in=user_ids)

    # 根据 xlsx 文件中的数据更新用户的 Opportunity
    for user in users:
        for d in data:
            if user.id == d['id']:
                user.Opportunity += d['sent']
                break

    # 使用 bulk_update() 批量更新数据库中的数据
    UserInfo.objects.bulk_update(users, ['Opportunity'])
