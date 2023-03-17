from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms

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



# Create your views here.


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


def mining_list(request):
    info_dict = request.session["info"]
    id = info_dict['id']
    user_dict = models.User_Info.objects.filter(id=id).first()
    miningList = models.Mining.objects.all()
    return render(request, "mining_list.html", {'miningList': miningList, "user_dict": user_dict})


def user(request):
    info_dict = request.session["info"]
    id = info_dict['id']
#    print(info_dict)

    if request.method == 'POST':
        coin_account = models.User_Info.objects.filter(id=id).first().coin_account
        wight = request.POST.get("sign")
        print(wight)
        flag = False
        #instant_mining(id, coin_account, flag)
        return redirect("http://127.0.0.1:8000/mining/list/")
    user_dict = models.User_Info.objects.filter(id= id).first()
    print(user_dict)
    return render(request, "user_list.html", {"user_dict": user_dict})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_info = models.User_Info.objects.filter(**form.cleaned_data).first()
        print(user_info)
        if not user_info:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})
        else:
            j = json.dumps(user_info.coin_account, cls=DecimalEncoder)
            request.session["info"] = {'id': user_info.id, "name": user_info.username
                                      }
            return redirect("http://127.0.0.1:8000/user/")

def logout(request):
    request.session.clear()
    return redirect('/login/')