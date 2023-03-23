from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.views.Daily_Payable_Calculation import calculation
from django.http import JsonResponse


@csrf_exempt
def add_activity(request):
    dict = request.POST
    last_record = models.Activity.objects.last()

    if last_record is None or last_record.in_progress == 0:
        calculation(dict["begintime"], dict["totaltime"], dict["salary"])
    else:
        response_data = {
            'status': 'duplicate',
            'message': '有活动正在进行，请关闭之前的活动再试。'
        }
        return JsonResponse(response_data, status=200)
    response_data = {
        'status': 'completed',
        'message': '活动创建成功。'
    }
    return JsonResponse(response_data, status=200)
