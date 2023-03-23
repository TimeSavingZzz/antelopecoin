import os

import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from app01.views.mining_distribution import distribution
from openpyxl.reader.excel import load_workbook

from app01 import models
from django import forms
import openpyxl
import random

from app01.templates.bootstrap import BootStrapForm
from app01.views.mining import instant_mining
import json
import decimal

from app01.views.opportunity import update_opportunity_from_xlsx


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)
# 引用


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        required=True
    )


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_info = models.UserInfo.objects.filter(**form.cleaned_data).first()
        print(user_info)
        if not user_info:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})
        else:
            j = json.dumps(user_info.coin_account, cls=DecimalEncoder)
            request.session["info"] = {'id': user_info.id, "name": user_info.username, "role" : user_info.role}
            if user_info.role == "1":
                return redirect("http://127.0.0.1:8000/user/")
            elif user_info.role == "0":
                return redirect("http://127.0.0.1:8000/admin/")


def logout(request):
    request.session.clear()
    return redirect('/login/')


@csrf_exempt
def contribute_list(request):
    # 1.获取用户上传的文件对象
    file_object = request.FILES.get("exc")
    time = request.POST.get("date")
    # 校验活动是否存在
    if models.Activity.objects.last().in_progress == 0:
        error_message = "目前不存在进行中的活动，请先创建！"
        return render(request, 'admin.html', {"error_message": error_message})
    # 校验上传文件的类型
    if file_object:
        file_extension = os.path.splitext(file_object.name)[1].lower()
        if file_extension == ".xlsx":
            pass
        else:
            error_message = "请上传一个有效的.xlsx 文件！"
            return render(request, 'admin.html', {"error_message": error_message})

        # 读入活动数据
    activity = pd.read_excel(f'{settings.STATIC_ROOT}activity.xlsx')
    print(time)
    # 检测time是否符合活动范围
    if dict(zip(activity['time'], activity['coin'])).get(time) is None:
        error_message = "输入时间不在活动范围内！"
        return render(request, 'admin.html', {"error_message": error_message})
    else:
        amount_shouldBeSent = dict(zip(activity['time'], activity['coin']))[time]
    print(amount_shouldBeSent)
    js, count = distribution(file_object, time, amount_shouldBeSent)
    if js is not None:
        new_file_name = f'sent_{time}.xlsx'
        new_file_path = f'{settings.STATIC_URL}xlsx/{new_file_name}'
        user_info = request.session.get("info")
        context = {'new_file_path': new_file_path, "tabledata": js, "user_info": user_info, "count": count, "time": time}
        return render(request, 'distri_list.html', context)
    else:
        error_message = "表格格式有误！"
        return render(request, 'admin.html', {"error_message": error_message})



def update_opportunity(request):
    if request.method == 'POST':
        time = request.POST
        time = time['time']

        new_file_name = f'sent_{time}.xlsx'
        new_file_path = f'{settings.STATIC_ROOT}{new_file_name}'
        update_opportunity_from_xlsx(new_file_path)

        return JsonResponse({'status': 'success', 'message': '发放成功！'})
    else:
        return JsonResponse({'status': 'error', 'message': '非法请求！'})


def user(request):
    info_dict = request.session["info"]
    id = info_dict['id']
#    print(info_dict)

    if request.method == 'POST':
        coin_account = models.UserInfo.objects.filter(id=id).first().coin_account
        wight = request.POST.get("sign")
        print(wight)
        flag = False
        #instant_mining(id, coin_account, flag)
        return redirect("http://127.0.0.1:8000/mining/list/")
    user_dict = models.UserInfo.objects.filter(id= id).first()
    print(user_dict)
    return render(request, "user_list.html", {"user_dict": user_dict})


def admin(request):
    info_dict = request.session["info"]
    id = info_dict['id']

    if 'sign' in request.POST:
        coin_account = models.UserInfo.objects.filter(id=id).first().coin_account
        wight = request.POST.get("sign")
        print(wight)
        flag = False
    # instant_mining(id, coin_account, flag)
        return redirect("http://127.0.0.1:8000/mining/list/")

    elif 'mining' in request.POST:
        return


    user_dict = models.UserInfo.objects.filter(id=id).first()
    print(user_dict)
    return render(request, "admin.html", {"user_dict": user_dict})
