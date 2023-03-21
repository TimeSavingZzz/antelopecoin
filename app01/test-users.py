import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

from app01.models import UserInfo
import openpyxl
import random

# 创建Excel表格
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['id', 'username', 'password', 'coin_account', 'Opportunity', 'role'])

# 向数据库中插入数据并添加到Excel表格中
for i in range(1, 3001):
    username = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(8))
    password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8))
    user = UserInfo.objects.create(username=username, password=password, coin_account=0, Opportunity=100, role="1")
    ws.append([user.id, user.username, user.password, user.coin_account, user.Opportunity, user.role])

# 保存Excel表格
wb.save('users.xlsx')