import os

from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
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
            request.session["info"] = {'id': user_info.id, "name": user_info.username}
            if user_info.role == "1":
                return redirect("http://127.0.0.1:8000/user/")
            elif user_info.role == "0":
                return redirect("http://127.0.0.1:8000/admin/")


def logout(request):
    request.session.clear()
    return redirect('/login/')


def contribute_list(request):
    # 1.获取用户上传的文件对象
    file_object = request.FILES.get("exc")
    time = request.POST.get("time")
    # 2.对象传递给openpyxl，由openpyxl读取文件的内容
    #distribution(file_object, time)

    new_file_name = 'sent_today.xlsx'
    new_file_path = f'{settings.STATIC_URL}xlsx/{new_file_name}'

    context = {'new_file_path': new_file_path}
    return render(request, 'mining_list.html', context)

    # info_dict = request.session["info"]
    # id = info_dict['id']
    # user_dict = models.UserInfo.objects.filter(id=id).first()
    # miningList = models.Mining.objects.all()
    # return render(request, "mining_list.html", {'miningList': miningList, "user_dict": user_dict})


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
